from enum import Enum
from typing import Set, List, Tuple, Dict, LiteralString, cast
from functools import cache

from mods_base import (
    NestedOption,
    BoolOption,
    SpinnerOption,
    hook,
    get_pc,
    ObjectFlags,  # noqa
)
from unrealsdk import logging, make_struct, find_class
from unrealsdk.unreal import UObject, WeakPointer, WrappedArray, WrappedStruct

from ultimate_loot_mod.utils import dynamic_load_object
from ultimate_loot_mod.mission_rewards.mission_override import create_zippy, ZippyType

all_character_starter_equipment: Set["CharacterStarterEquipment"] = set()

WEAPON_MAPPING: Dict[str, Tuple[LiteralString, Tuple[ZippyType, ...] | None]] = {
    'Any': ('UltimateLoot_Pools_TEST.ChestPools.WhiteChest.WhiteChest_Weapons_All', None),
    'Sniper': ('UltimateLoot_Pools_TEST.ChestPools.WhiteChest.WhiteChest_Weapons_Snipers_All', (ZippyType.Sniper, ZippyType.Eridian)),
    'SMG': ('UltimateLoot_Pools_TEST.ChestPools.WhiteChest.WhiteChest_Weapons_SMGs_All', (ZippyType.SMG, ZippyType.Eridian)),
    'Shotgun': ('UltimateLoot_Pools_TEST.ChestPools.WhiteChest.WhiteChest_Weapons_Shotguns_All', (ZippyType.Shotgun, ZippyType.Eridian)),
    'Assault Rifle': ('UltimateLoot_Pools_TEST.ChestPools.WhiteChest.WhiteChest_Weapons_Rifles_All', (ZippyType.AssaultRifle, ZippyType.Eridian)),
    'Repeater': ('UltimateLoot_Pools_TEST.ChestPools.WhiteChest.WhiteChest_Weapons_Pistols_All', (ZippyType.Repeater, ZippyType.Eridian)),
    'Revolver': ('UltimateLoot_Pools_TEST.ChestPools.WhiteChest.WhiteChest_Weapons_Pistols_All', (ZippyType.Revolver, ZippyType.Eridian)),
    'Rocket Launcher': ('UltimateLoot_Pools_TEST.ChestPools.WhiteChest.WhiteChest_Weapons_Launchers_All', (ZippyType.Launcher, ZippyType.Eridian)),
}

ITEM_MAPPING: Dict[str, Tuple[LiteralString, Tuple[ZippyType, ...] | None]] = {
    'Shield': ('UltimateLoot_Pools_TEST.ChestPools.RedChest.RedChest_Items_Shields', (ZippyType.Shield, ZippyType.Eridian)),
    'Grenade Mod': ('UltimateLoot_Pools_TEST.ChestPools.RedChest.RedChest_GrenadeMods_All', (ZippyType.GrenadeMod, ZippyType.EWOGrenadeMod)),
    # 'Class Mod': ('UltimateLoot_Pools_TEST.ChestPools.RedChest.RedChest_Items_Classmods', (ZippyType.ClassMod,)),
}

RESOURCE_POOLS: List[Tuple[LiteralString, LiteralString, int, int]] = [
    ('d_resources.AmmoResources.Ammo_Combat_Rifle', 'd_resourcepools.AmmoPools.Ammo_Combat_Rifle_Pool', 108, 0),
    ('d_resources.AmmoResources.Ammo_Combat_Shotgun', 'd_resourcepools.AmmoPools.Ammo_Combat_Shotgun_Pool', 18, 0),
    ('d_resources.AmmoResources.Ammo_Patrol_SMG', 'd_resourcepools.AmmoPools.Ammo_Patrol_SMG_Pool', 108, 0),
    ('d_resources.AmmoResources.Ammo_Repeater_Pistol', 'd_resourcepools.AmmoPools.Ammo_Repeater_Pistol_Pool', 30, 0),
    ('d_resources.AmmoResources.Ammo_Revolver_Pistol', 'd_resourcepools.AmmoPools.Ammo_Revolver_Pistol_Pool', 12, 0),
    ('d_resources.AmmoResources.Ammo_Rocket_Launcher', 'd_resourcepools.AmmoPools.Ammo_Rocket_Launcher_Pool', 8, 0),
    ('d_resources.AmmoResources.Ammo_Sniper_Rifle', 'd_resourcepools.AmmoPools.Ammo_Sniper_Rifle_Pool', 16, 0),
]


class DefaultProfile(Enum):
    Brick = 'gd_profiles.default_profile_Brick'
    Lilith = 'gd_profiles.default_profile_Lilith'
    Mordecai = 'gd_profiles.default_profile_Mordecai'
    Roland = 'gd_profiles.default_profile_Roland'


DEFAULT_WEAPON: Dict[DefaultProfile, str] = {
    DefaultProfile.Brick: 'Shotgun',
    DefaultProfile.Lilith: 'SMG',
    DefaultProfile.Mordecai: 'Sniper',
    DefaultProfile.Roland: 'Assault Rifle',
}


class EQuickWeaponSlot(Enum):
    QuickSelectNone = 0
    QuickSelectUp = 1
    QuickSelectDown = 2
    QuickSelectLeft = 3
    QuickSelectRight = 4
    EQuickWeaponSlot_MAX = 5


def _get_item_from_loot_pool(pool: UObject, expected_zippy: Tuple[ZippyType] | None = None, game_stage: int = 1) -> UObject | None:
    cdo: UObject = find_class('WillowGame.ItemPool').ClassDefaultObject

    # Bit of an odd choice but if we are given a loot pool that can spawn multiple item
    # types then we are not guaranteed to get the right type of item.
    for i in range(0, 20):

        # Bias towards smaller numbers, unsure if this actually does anything since the normal loot
        # pool spawning process has been changed by Ultimate Loot Mod.
        #   Can see a range of values with:
        #   Haskell Snippet: `map (\x -> (x, 5.0 + 65.0 * (x ** 2.8))) [0, 0.1 .. 1.0]`
        from random import random
        awesome_level = int(round(5.0 + (65 * (random() ** 2.8)), 2))
        _, items = cdo.SpawnBalancedInventoryFromPool(pool, game_stage, awesome_level, get_pc(), [])

        for item in items:
            item_zippy = create_zippy(str(item.ZippyFrame).strip().lower(), use_name=False)

            if item_zippy is None:
                logging.error(f'Unknown item zippy: "{item.ZippyFrame}"')
                continue

            if expected_zippy is None or item_zippy in expected_zippy:
                return item.DefinitionData

    return None


class ItemEnabler(BoolOption):

    # noinspection PyArgumentList
    def __init__(self, item_name: str):
        super().__init__(item_name, value=False)

    def create_item_def(self) -> WrappedStruct | None:

        if not self.value:
            return None

        loot_pool_path, zippy = ITEM_MAPPING[self.identifier]
        loot_pool: UObject | None = dynamic_load_object('ItemPoolDefinition', loot_pool_path, no_throw=True)

        if loot_pool is None:
            logging.error(f'Failed to load loot pool "{loot_pool_path}"')
            return None

        item = _get_item_from_loot_pool(loot_pool, zippy, 3 if self.identifier == 'Shield' else 8)

        if item is None:
            logging.error(f'Failed to find \'{self.identifier}\' item in pool \'{loot_pool_path}\'')
            return None

        return make_struct(
            'InventoryProfileData',
            DefinitionData=item,
            Quantity=1,
            bEquipped=True,
        )


class WeaponSpinner(SpinnerOption):
    quick_slot: EQuickWeaponSlot

    # noinspection PyArgumentList
    def __init__(self, indentifier: str, quick_slot: EQuickWeaponSlot, value: str | None = None) -> None:
        self.quick_slot = quick_slot
        super().__init__(
            indentifier,
            value='None' if value is None else value,
            choices=[
                'None',
                *WEAPON_MAPPING.keys()
            ]
        )

    def create_weapon_def(self) -> WrappedStruct | None:

        if self.value == 'None':
            return None

        loot_pool_path, zippy = WEAPON_MAPPING[self.value]
        loot_pool: UObject | None = dynamic_load_object('ItemPoolDefinition', loot_pool_path, no_throw=True)

        if loot_pool is None:
            logging.error(f'Failed to load loot pool "{loot_pool_path}"')
            return None

        return make_struct(
            'WeaponProfileData',
            StoredAmmo=0,
            QuickSlot=int(self.quick_slot.value),
            WeaponDefinitionData=_get_item_from_loot_pool(loot_pool, zippy),
        )


class CharacterStarterEquipment(NestedOption):
    profile: DefaultProfile
    _profile_object: WeakPointer[UObject]

    def __hash__(self) -> int:
        return hash(self.profile)

    # noinspection PyArgumentList
    def __init__(self, profile: DefaultProfile):
        global DEFAULT_WEAPON

        super().__init__(profile.name, children=(
            WeaponSpinner('Weapon Primary', quick_slot=EQuickWeaponSlot.QuickSelectUp, value=DEFAULT_WEAPON.get(profile)),
            WeaponSpinner('Weapon Secondary', quick_slot=EQuickWeaponSlot.QuickSelectDown),
            *(
                ItemEnabler(item)
                for item in ITEM_MAPPING.keys()
            )
        ))

        self.profile = profile
        self._profile_object = WeakPointer()

        all_character_starter_equipment.discard(self)
        all_character_starter_equipment.add(self)

    def get_profile(self) -> UObject | None:
        if (obj := self._profile_object()) is None:
            loaded = dynamic_load_object('PlayerProfile', self.profile.value, no_throw=True)

            if loaded is None:
                return None

            # Possibly redundant
            loaded.ObjectFlags |= ObjectFlags.KEEP_ALIVE  # noqa
            self._profile_object.replace(loaded)

            return loaded

        else:
            return obj

    def apply_to_game(self) -> None:
        if (obj := self.get_profile()) is None:
            logging.error(f'Failed to load profile "{self.profile.value}"')
            return

        resource_data: WrappedArray[WrappedStruct] = obj.ResourceData
        resource_data.clear()

        for resource_path, pool_path, amount, level in RESOURCE_POOLS:
            resource_data.append(make_struct(
                'ResourceProfileData',
                ResourceDefinition=dynamic_load_object('ResourceDefinition', resource_path),
                ResourcePoolDefinition=dynamic_load_object('ResourcePoolDefinition', pool_path),
                Amount=amount,
                UpgradeLevel=level,
            ))

        weapon_data: WrappedArray[WrappedStruct] = obj.WeaponData
        item_data: WrappedArray[WrappedStruct] = obj.ItemData

        weapon_data.clear()
        item_data.clear()

        for opt in self.children:

            if isinstance(opt, WeaponSpinner):
                weap = opt.create_weapon_def()
                if weap is not None:
                    weapon_data.append(weap)

            elif isinstance(opt, ItemEnabler):
                item = opt.create_item_def()
                if item is not None:
                    item_data.append(item)


# noinspection PyArgumentList
@cache
def create_starter_equipment_options() -> NestedOption:
    return NestedOption(
        "Starter Equipment",
        children=[
            BoolOption('Enabled', value=False),
            *(
                CharacterStarterEquipment(profile)
                for profile in DefaultProfile
            )
        ],
    )


@hook('WillowGame.CharacterSelectionGFxMovie:Start', immediately_enable=True)
def hook_on_character_selection(*_) -> None:
    if not cast(BoolOption, create_starter_equipment_options().children[0]).value:
        return

    logging.info('Refreshing starter equipment!')
    for starter_equipment in all_character_starter_equipment:
        starter_equipment.apply_to_game()


@hook('Engine.Console:InputKey', immediately_enable=True)
def hook_on_console_input(_0, args, *_) -> None:
    from mods_base import EInputEvent, get_pc

    key = args.Key
    event = args.Event

    if event != EInputEvent.IE_Released:
        return

    if (
        (wpc := get_pc()) is not None
        and key in ('LeftMouseButton', 'Enter', 'Space', 'Escape')
        and wpc.GFxUIManager.GetPlayingMovie() is None
    ):
        wpc.ConsoleCommand('StopMovie')
