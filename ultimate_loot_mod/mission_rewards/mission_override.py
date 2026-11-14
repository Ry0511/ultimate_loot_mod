from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from enum import Enum
from importlib import resources
from pathlib import Path
from typing import override

from unrealsdk import find_class, logging
from unrealsdk.unreal import UObject

from ultimate_loot_mod.utils import dynamic_load_object

__all__ = [
    "INV_BAL_DEF",
    "ITEM_POOL_DEF",
    "spawned_items",
    "MissionRewardOverride",
    "ZippyType",
    "MissionDefinition",
    "InventoryBalanceDefinition",
    "ItemPoolDefinition",
    "load_mission_reward_overrides",
]

INV_BAL_DEF: str = "InventoryBalanceDefinition"
ITEM_POOL_DEF: str = "ItemPoolDefinition"

# List of all items we have spawned which will not get garbage collected
spawned_items: list[UObject] = list()


# This doesn't need to be an enum as it also makes things harder if there are custom zippy types
# which are not captured here.
class ZippyType(Enum):
    All = "All"
    ClassMod = "Comm"
    Revolver = "Revolver"
    AssaultRifle = "ar"
    Shield = "Shield"
    Shotgun = "ShotGun"
    GrenadeMod = "mod"
    Launcher = "rocket"
    Sniper = "Sniper"
    Repeater = "Repeater"
    SMG = "SMG"
    Eridian = "Eridian"
    EWOGrenadeMod = "eridian_grenade"
    EWOShield = "eridian_shield"
    Artifact = "elemental"

    @override
    def __repr__(self) -> str:
        return self.name


type MissionDefinition = UObject
type InventoryBalanceDefinition = UObject
type ItemPoolDefinition = UObject


def create_zippy(zippy_str: str, use_name: bool = True) -> ZippyType | None:
    for zippy in ZippyType:
        if use_name:
            if zippy.name.lower() == zippy_str:
                return zippy
        else:
            if zippy.value.lower() == zippy_str:
                return zippy
    return None


def load_mission_reward_overrides(file: Path | None = None) -> list[MissionRewardOverride]:
    res: list["MissionRewardOverride"] = list()

    def _read_stream(handle: Iterable[str]) -> None:
        nonlocal res
        line_number = 0

        for line in handle:
            trimmed_line = line.strip()
            line_number += 1

            # Skip comments and empty lines
            if trimmed_line.startswith("#") or len(trimmed_line) == 0:
                continue

            try:
                res.append(
                    MissionRewardOverride.create([s.strip() for s in trimmed_line.split(",")])
                )
            except ValueError as ex:
                logging.error(f"Failed to parse line {line_number} with error {ex}")

    # Open and read the default file ( even if said default file is inside a .sdkmod )
    if file is None:
        pth = resources.files("ultimate_loot_mod.mission_rewards") / "custom_rewards.txt"
        with pth.open(encoding="utf-8") as handle:
            _read_stream(handle)
    else:
        if not file.is_file():
            logging.error(f'File not found "{file}"')
            return res

        logging.info(f'Loading mission reward override file: "{file.resolve().name}"')

        with open(file.resolve()) as handle:
            _read_stream(handle)

    return res


@dataclass
class MissionRewardOverride:
    override_path: str
    """The path of the object to override. Either the reward path or the mission path"""

    reward_path: str
    """The path to the reward loot pool or item to return"""

    is_loot_pool_reward: bool | None = field(default=None)
    """Whether this reward is returning a loot pool or an item definition"""

    is_mission_override: bool | None = field(default=None)
    """Whether this reward is overriding the mission or the reward"""

    zippy: Sequence[ZippyType] | None = field(default=None)
    """The flash item/s type produced by this reward; None means any/all, Revolver, ClassMod, etc"""

    @staticmethod
    def create(args: list[str], auto_detect: bool = True) -> MissionRewardOverride:
        if len(args) < 2:
            raise ValueError(f"A minimum of 2 arguments is required got {args}")

        override_path = args.pop(0)
        reward_path = args.pop(0)
        res = MissionRewardOverride(override_path.lower(), reward_path.lower())

        is_mission_override: bool | None = None
        is_loot_pool_reward: bool | None = None
        zippy_set: set[ZippyType] = set()

        for arg in args:
            lower_arg = arg.lower()

            if (bool_val := lower_arg == "true") or lower_arg == "false":
                if is_loot_pool_reward is None:
                    is_loot_pool_reward = bool_val

                elif is_mission_override is None:
                    is_mission_override = bool_val

                else:
                    logging.error("Unexpected bool argument provided, ignoring it")
            else:
                if (zippy := create_zippy(lower_arg)) is not None:
                    zippy_set.add(zippy)
                else:
                    logging.error(f'Unknown zippy value: "{arg}", ignoring it')

        # Only setting after everything has been processed
        res.is_mission_override = is_mission_override
        res.is_loot_pool_reward = is_loot_pool_reward

        # Set the zippy if needed
        if len(zippy_set) > 0:
            if ZippyType.All in zippy_set:
                res.zippy = None
            else:
                res.zippy = tuple(zippy_set)

        # if auto detection is enabled and fails then we have no idea what this reward overrides
        # nor what the reward is. It is simpler to just fail here than to try to figure it out
        if auto_detect and res.needs_auto_detection() and not res.auto_detect():
            raise ValueError(f'Failed to auto detect override type for "{override_path}"')

        return res

    def auto_detect_override_type(self) -> bool:
        MISSION_DEF = "MissionDefinition"

        if self.is_mission_override is not None:
            return True

        if dynamic_load_object(MISSION_DEF, self.override_path, no_throw=True):
            self.is_mission_override = True
            return True

        elif dynamic_load_object(INV_BAL_DEF, self.override_path, no_throw=True):
            self.is_mission_override = False
            return True

        return False

    def auto_detect_reward_type(self) -> bool:

        if self.is_loot_pool_reward is not None:
            return True

        if dynamic_load_object(INV_BAL_DEF, self.reward_path, no_throw=True):
            self.is_loot_pool_reward = False
            return True

        elif dynamic_load_object(ITEM_POOL_DEF, self.reward_path, no_throw=True):
            self.is_loot_pool_reward = True
            return True

        return False

    def auto_detect(self) -> bool:
        res = True

        if not self.auto_detect_override_type():
            logging.error(f'Failed to auto detect override type for "{self.override_path}"')
            res = False

        if not self.auto_detect_reward_type():
            logging.error(f'Failed to auto detect reward type for "{self.reward_path}"')
            res = False

        if res:
            logging.info(
                f'Auto detection reward="{self.reward_path}", '
                + f'loot_pool="{self.is_loot_pool_reward}", '
                + f'mission_override="{self.is_mission_override}"'
            )

        return res

    def needs_auto_detection(self) -> bool:
        return self.is_mission_override is None or self.is_loot_pool_reward is None

    def compare_zippy(self, zippy: ZippyType) -> bool:
        return self.zippy is None or zippy in self.zippy

    def reward_uobject(self) -> UObject | None:

        # Try to auto detect internal types if needed
        if self.needs_auto_detection() and not self.auto_detect():
            return None

        if not self.is_loot_pool_reward:
            return dynamic_load_object(INV_BAL_DEF, self.reward_path, no_throw=True)
        else:
            return dynamic_load_object(ITEM_POOL_DEF, self.reward_path, no_throw=True)

    def get_reward(self, wpc: UObject) -> InventoryBalanceDefinition | None:

        if not (reward := self.reward_uobject()):
            logging.error(f'Failed to load reward object from "{self.reward_path}"')
            return None

        if self.is_loot_pool_reward:
            return self._get_item_from_loot_pool(reward, wpc)
        else:
            return reward

    def _get_item_from_loot_pool(
        self, pool: ItemPoolDefinition, wpc: UObject
    ) -> InventoryBalanceDefinition | None:

        global spawned_items

        cdo: UObject = find_class("WillowGame.ItemPool").ClassDefaultObject

        # Bit of an odd choice but if we are given a loot pool that can spawn multiple item
        # types then we are not guaranteed to get the right type of item.

        gamestage: int = wpc.Pawn.GetGamestage()
        awesome_level: int = wpc.Pawn.GetAwesomeLevel()
        logging.misc(f"Gamestage={gamestage}, AwesomeLevel={awesome_level}")

        for _ in range(20):
            _, items = cdo.SpawnBalancedInventoryFromPool(pool, gamestage, awesome_level, wpc, [])

            for item in items:
                spawned_items.append(item)
                item_zippy = create_zippy(str(item.ZippyFrame).strip().lower(), use_name=False)

                if item_zippy is None:
                    logging.error(f'Unknown item zippy: "{item.ZippyFrame}"')
                    return None

                if self.compare_zippy(item_zippy):
                    return item.DefinitionData.BalanceDefinition

        logging.error(f"Failed to find '{self.zippy}' item in pool '{self.reward_path}'")
        return None
