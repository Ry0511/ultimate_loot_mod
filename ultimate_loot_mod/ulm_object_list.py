from typing import List
from enum import Enum, auto

from unrealsdk import logging
from unrealsdk.unreal import UObject
from unrealsdk import find_object

type AttributeDefinition = UObject
type AttributeDataType = int | float | bool

type EAttributeDataType = int
ADT_Float: EAttributeDataType = 0
ADT_Int: EAttributeDataType = 1
ADT_Bool: EAttributeDataType = 2

__all__: List[str] = [
    "ObjectTag",
    "TagObject",
    "AttributeDefinition",
    "AttributeDataType",
    "EAttributeDataType",
    "ADT_Float",
    "ADT_Int",
    "ADT_Bool",
    "TAG_OBJ_LIST",
    "TAG_PATH_LIST",
    "TAG_STATIC_DEFAULTS",
]


class ObjectTag(Enum):

    # Why the fuck is this not zero based?
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return count

    VHC_Vladof_Expanded_Enabler = auto()
    Arsenal_Enabler = auto()
    BetterHealth_Enabler = auto()
    EWO_Enabler = auto()
    PearlescentSDUs_Enabler = auto()
    VHC_Atlas_Enabler = auto()
    VHC_Atlas_Expanded_Enabler = auto()
    VHC_Dahl_Enabler = auto()
    VHC_Dahl_Expanded_Enabler = auto()
    VHC_Enabler = auto()
    VHC_Expanded_Enabler = auto()
    VHC_Gearbox_Enabler = auto()
    VHC_Hyperion_Enabler = auto()
    VHC_Hyperion_Expanded_Enabler = auto()
    VHC_Jakobs_Enabler = auto()
    VHC_Jakobs_Expanded_Enabler = auto()
    VHC_Maliwan_Enabler = auto()
    VHC_Maliwan_Expanded_Enabler = auto()
    VHC_Randomizer_Enabler = auto()
    VHC_SandS_Enabler = auto()
    VHC_SandS_Expanded_Enabler = auto()
    VHC_Tediore_Enabler = auto()
    VHC_Tediore_Expanded_Enabler = auto()
    VHC_Torgue_Enabler = auto()
    VHC_Torgue_Expanded_Enabler = auto()
    VHC_Vladof_Enabler = auto()
    DropChance_EWO = auto()
    DropChance_Common = auto()
    DropChance_Legendary = auto()
    DropChance_Lootable = auto()
    DropChance_Pearlescent = auto()
    Multiplier_CrimsonChest_Legendary = auto()
    Multiplier_CrimsonChest_Pearlescent = auto()
    Multiplier_RedChest_Legendary = auto()
    Multiplier_RedChest_Pearlescent = auto()
    Multiplier_WhiteChest_Legendary = auto()
    Multiplier_WhiteChest_Pearlescent = auto()


TAG_PATH_LIST: List[str] = [
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Vladof_Expanded_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.Arsenal_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.BetterHealth_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.EWO_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.PearlescentSDUs_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Atlas_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Atlas_Expanded_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Dahl_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Dahl_Expanded_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Expanded_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Gearbox_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Hyperion_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Hyperion_Expanded_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Jakobs_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Jakobs_Expanded_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Maliwan_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Maliwan_Expanded_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Randomizer_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_SandS_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_SandS_Expanded_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Tediore_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Tediore_Expanded_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Torgue_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Torgue_Expanded_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Vladof_Enabler",
    "UltimateLoot_Attributes_TEST.Attributes.EWO.DropChance.DropChance_EWO",
    "UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Common",
    "UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Legendary",
    "UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Lootable",
    "UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Pearlescent",
    "UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_CrimsonChest_Legendary",
    "UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_CrimsonChest_Pearlescent",
    "UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_RedChest_Legendary",
    "UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_RedChest_Pearlescent",
    "UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_WhiteChest_Legendary",
    "UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_WhiteChest_Pearlescent",
]

TAG_STATIC_DEFAULTS: List[int | float | bool] = [
    False,
    True,
    True,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    12.0,
    100.0,
    2.0,
    10.0,
    0.0,
    150.0,
    100.0,
    100.0,
    25.0,
    25.0,
    5.0,
]

TAG_OBJ_LIST: List[AttributeDefinition | None] = [None] * len(ObjectTag)


# More of a ProxyObject
class TagObject:
    tag: ObjectTag

    def __init__(self, tag: ObjectTag) -> None:
        self.tag = tag

    def index(self) -> int:
        return self.tag.value

    def get_path(self):
        return TAG_PATH_LIST[self.index()]

    def get_obj(self) -> AttributeDefinition | None:
        return TAG_OBJ_LIST[self.index()]

    def load_obj(self) -> bool:
        obj = TAG_OBJ_LIST[self.index()]

        if obj is not None:
            return True

        try:
            TAG_OBJ_LIST[self.index()] = find_object("AttributeDefinition", self.get_path())
            TAG_OBJ_LIST[self.index()].ObjectFlags |= 0x4000
        except Exception:  # noqa
            pass

        return TAG_OBJ_LIST[self.index()] is not None

    def set_value(self, val: float | int | bool) -> bool:
        if not self.load_obj():
            return False

        try:
            obj = self.get_obj()
            size = len(obj.ValueResolverChain)
            if size == 0:
                logging.error(f"ValueResolverChain of {self.get_path()} is empty")
                return False
            else:
                obj.ValueResolverChain[size - 1].ConstantValue = val
        except Exception as ex:
            logging.dev_warning(f"Failed to set value for {self.get_path()}: {ex}")
            return False

        return True

    def get_value(self, allow_default=False) -> float | int | bool | None:
        if not self.load_obj():
            return TAG_STATIC_DEFAULTS[self.index()] if allow_default else None

        try:
            obj = self.get_obj()
            ty: EAttributeDataType = obj.AttributeDataType
            size = len(obj.ValueResolverChain)

            if size == 0:
                logging.error(f"ValueResolverChain of {self.get_path()} is empty")
                return TAG_STATIC_DEFAULTS[self.index()] if allow_default else None

            val = obj.ValueResolverChain[size - 1].ConstantValue

            if ty == ADT_Float:
                return round(float(val), 6)
            elif ty == ADT_Int:
                return int(val)
            elif ty == ADT_Bool:
                return int(val) != 0
            else:
                return val

        except Exception as ex:
            logging.dev_warning(f"Failed to get value for {self.get_path()}: {ex}")
            return TAG_STATIC_DEFAULTS[self.index()] if allow_default else None

    def get_static_default(self) -> float | int | bool:
        return TAG_STATIC_DEFAULTS[self.index()]
