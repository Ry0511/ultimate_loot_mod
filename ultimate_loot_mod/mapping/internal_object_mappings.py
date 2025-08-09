from typing import Dict, List, Tuple

from unrealsdk.unreal import UObject
from .attribute_types import AttributeDataType
from .internal_object_list import Tag

__all__ = [
    "Tag",
    "OBJECT_PATH_MAPPING",
    "VHC_CONFIG_LIST",
    "DEFAULT_VALUE_MAPPING",
    "LOADED_OBJECT_MAPPING",
    "BASE_DROP_CHANCES",
    "CHEST_MULTIPLIERS",
]

################################################################################
# | OBJECT PATH LIST |
################################################################################

OBJECT_PATH_MAPPING: Dict[Tag, str] = {
    Tag.Arsenal_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.Arsenal_Enabler',
    Tag.BetterHealth_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.BetterHealth_Enabler',
    Tag.EWO_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.EWO_Enabler',
    Tag.PearlescentSDUs_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.PearlescentSDUs_Enabler',
    Tag.VHC_Atlas_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Atlas_Enabler',
    Tag.VHC_Atlas_Expanded_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Atlas_Expanded_Enabler',
    Tag.VHC_Dahl_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Dahl_Enabler',
    Tag.VHC_Dahl_Expanded_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Dahl_Expanded_Enabler',
    Tag.VHC_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Enabler',
    Tag.VHC_Expanded_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Expanded_Enabler',
    Tag.VHC_Gearbox_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Gearbox_Enabler',
    Tag.VHC_Hyperion_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Hyperion_Enabler',
    Tag.VHC_Hyperion_Expanded_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Hyperion_Expanded_Enabler',
    Tag.VHC_Jakobs_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Jakobs_Enabler',
    Tag.VHC_Jakobs_Expanded_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Jakobs_Expanded_Enabler',
    Tag.VHC_Maliwan_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Maliwan_Enabler',
    Tag.VHC_Maliwan_Expanded_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Maliwan_Expanded_Enabler',
    Tag.VHC_Randomizer_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Randomizer_Enabler',
    Tag.VHC_SandS_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_SandS_Enabler',
    Tag.VHC_SandS_Expanded_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_SandS_Expanded_Enabler',
    Tag.VHC_Tediore_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Tediore_Enabler',
    Tag.VHC_Tediore_Expanded_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Tediore_Expanded_Enabler',
    Tag.VHC_Torgue_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Torgue_Enabler',
    Tag.VHC_Torgue_Expanded_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Torgue_Expanded_Enabler',
    Tag.VHC_Vladof_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Vladof_Enabler',
    Tag.VHC_Vladof_Expanded_Enabler: 'UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Vladof_Expanded_Enabler',

    Tag.DropChance_EWO: 'UltimateLoot_Attributes_TEST.Attributes.EWO.DropChance.DropChance_EWO',

    Tag.DropChance_Legendary: 'UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Legendary',
    Tag.DropChance_Lootable: 'UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Lootable',
    Tag.DropChance_Pearlescent: 'UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Pearlescent',

    Tag.Multiplier_CrimsonChest_Legendary: 'UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_CrimsonChest_Legendary',
    Tag.Multiplier_CrimsonChest_Pearlescent: 'UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_CrimsonChest_Pearlescent',
    Tag.Multiplier_RedChest_Legendary: 'UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_RedChest_Legendary',
    Tag.Multiplier_RedChest_Pearlescent: 'UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_RedChest_Pearlescent',
    Tag.Multiplier_WhiteChest_Legendary: 'UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_WhiteChest_Legendary',
    Tag.Multiplier_WhiteChest_Pearlescent: 'UltimateLoot_Attributes_TEST.Attributes.Shared.Multiplier.Multiplier_WhiteChest_Pearlescent',
}

################################################################################
# | VHC OBJECT LIST |
################################################################################

VHC_CONFIG_LIST: List[Tuple[str, Tag, Tag | None]] = [
    ("Gearbox", Tag.VHC_Gearbox_Enabler, None),
    ("Atlas", Tag.VHC_Atlas_Enabler, Tag.VHC_Atlas_Expanded_Enabler),
    ("SandS", Tag.VHC_SandS_Enabler, Tag.VHC_SandS_Expanded_Enabler),
    ("Maliwan", Tag.VHC_Maliwan_Enabler, Tag.VHC_Maliwan_Expanded_Enabler),
    ("Jakobs", Tag.VHC_Jakobs_Enabler, Tag.VHC_Jakobs_Expanded_Enabler),
    ("Torgue", Tag.VHC_Torgue_Enabler, Tag.VHC_Torgue_Expanded_Enabler),
    ("Hyperion", Tag.VHC_Hyperion_Enabler, Tag.VHC_Hyperion_Expanded_Enabler),
    ("Vladof", Tag.VHC_Vladof_Enabler, Tag.VHC_Vladof_Expanded_Enabler),
    ("Dahl", Tag.VHC_Dahl_Enabler, Tag.VHC_Dahl_Expanded_Enabler),
    ("Tediore", Tag.VHC_Tediore_Enabler, Tag.VHC_Tediore_Expanded_Enabler),
]

################################################################################
# | DROP RATE OPTIONS |
################################################################################

BASE_DROP_CHANCES: List[Tag] = [
    Tag.DropChance_EWO,
    Tag.DropChance_Legendary,
    Tag.DropChance_Lootable,
    Tag.DropChance_Pearlescent,
]

CHEST_MULTIPLIERS: List[Tag] = [
    Tag.Multiplier_CrimsonChest_Legendary,
    Tag.Multiplier_CrimsonChest_Pearlescent,
    Tag.Multiplier_RedChest_Legendary,
    Tag.Multiplier_RedChest_Pearlescent,
    Tag.Multiplier_WhiteChest_Legendary,
    Tag.Multiplier_WhiteChest_Pearlescent,
]

################################################################################
# | DEFAULT VALUE MAPPING |
################################################################################

# NOTE: These get overwritten by the actual values when initially loading.

DEFAULT_VALUE_MAPPING: Dict[Tag, AttributeDataType] = {
    Tag.Arsenal_Enabler: True,
    Tag.BetterHealth_Enabler: True,
    Tag.EWO_Enabler: True,
    Tag.PearlescentSDUs_Enabler: True,
    Tag.VHC_Enabler: False,
    Tag.VHC_Expanded_Enabler: True,
    Tag.VHC_Gearbox_Enabler: False,
    Tag.VHC_Randomizer_Enabler: False,
    Tag.VHC_Atlas_Enabler: False,
    Tag.VHC_Atlas_Expanded_Enabler: False,
    Tag.VHC_Dahl_Enabler: False,
    Tag.VHC_Dahl_Expanded_Enabler: False,
    Tag.VHC_Hyperion_Enabler: False,
    Tag.VHC_Hyperion_Expanded_Enabler: False,
    Tag.VHC_Jakobs_Enabler: False,
    Tag.VHC_Jakobs_Expanded_Enabler: False,
    Tag.VHC_Maliwan_Enabler: False,
    Tag.VHC_Maliwan_Expanded_Enabler: False,
    Tag.VHC_SandS_Enabler: False,
    Tag.VHC_SandS_Expanded_Enabler: False,
    Tag.VHC_Tediore_Enabler: False,
    Tag.VHC_Tediore_Expanded_Enabler: False,
    Tag.VHC_Torgue_Enabler: False,
    Tag.VHC_Torgue_Expanded_Enabler: False,
    Tag.VHC_Vladof_Enabler: False,
    Tag.VHC_Vladof_Expanded_Enabler: False,
    Tag.DropChance_EWO: 12.0,
    Tag.DropChance_Lootable: 10.0,
    Tag.DropChance_Legendary: 2.0,
    Tag.DropChance_Pearlescent: 0.1,
    Tag.Multiplier_CrimsonChest_Legendary: 150.0,
    Tag.Multiplier_CrimsonChest_Pearlescent: 100.0,
    Tag.Multiplier_RedChest_Legendary: 100.0,
    Tag.Multiplier_RedChest_Pearlescent: 25.0,
    Tag.Multiplier_WhiteChest_Legendary: 25.0,
    Tag.Multiplier_WhiteChest_Pearlescent: 5.0,
}

LOADED_OBJECT_MAPPING: Dict[Tag, UObject | None] = {tag: None for tag in Tag}
