from unrealsdk.unreal import UObject

from .attribute_types import AttributeDataType
from .internal_object_list import Tag

__all__ = [
    "Tag",
    "OBJECT_PATH_MAPPING",
    "VHC_CONFIG_LIST",
    "DEFAULT_VALUE_MAPPING",
    "FIRST_LOAD_VALUE_MAPPING",
    "LOADED_OBJECT_MAPPING",
    "BASE_DROP_CHANCES",
    "CHEST_MULTIPLIERS",
]

################################################################################
# | OBJECT PATH LIST |
################################################################################

OBJECT_PATH_MAPPING: dict[Tag, str] = {
    tag: f"UltimateLoot_Attributes_TEST.Attributes.{group}.{tag.name}"
    for group, tags in (
        (
            "_Enabler",
            (
                Tag.Arsenal_Enabler,
                Tag.BetterHealth_Enabler,
                Tag.EWO_Enabler,
                Tag.PearlescentSDUs_Enabler,
                Tag.VHC_Atlas_Enabler,
                Tag.VHC_Atlas_Expanded_Enabler,
                Tag.VHC_Dahl_Enabler,
                Tag.VHC_Dahl_Expanded_Enabler,
                Tag.VHC_Enabler,
                Tag.VHC_Expanded_Enabler,
                Tag.VHC_Gearbox_Enabler,
                Tag.VHC_Hyperion_Enabler,
                Tag.VHC_Hyperion_Expanded_Enabler,
                Tag.VHC_Jakobs_Enabler,
                Tag.VHC_Jakobs_Expanded_Enabler,
                Tag.VHC_Maliwan_Enabler,
                Tag.VHC_Maliwan_Expanded_Enabler,
                Tag.VHC_Randomizer_Enabler,
                Tag.VHC_SandS_Enabler,
                Tag.VHC_SandS_Expanded_Enabler,
                Tag.VHC_Tediore_Enabler,
                Tag.VHC_Tediore_Expanded_Enabler,
                Tag.VHC_Torgue_Enabler,
                Tag.VHC_Torgue_Expanded_Enabler,
                Tag.VHC_Vladof_Enabler,
                Tag.VHC_Vladof_Expanded_Enabler,
            ),
        ),
        (
            "EWO.DropChance",
            (Tag.DropChance_EWO,),
        ),
        (
            "Shared.DropChance",
            (
                Tag.DropChance_Legendary,
                Tag.DropChance_Lootable,
                Tag.DropChance_Pearlescent,
                Tag.DropChance_EnemyEquipment,
            ),
        ),
        (
            "VHC.DropChance",
            (Tag.DropChance_Hybrid,),
        ),
        (
            "Shared.Multiplier",
            (
                Tag.Multiplier_CrimsonChest_Legendary,
                Tag.Multiplier_CrimsonChest_Pearlescent,
                Tag.Multiplier_RedChest_Legendary,
                Tag.Multiplier_RedChest_Pearlescent,
                Tag.Multiplier_WhiteChest_Legendary,
                Tag.Multiplier_WhiteChest_Pearlescent,
            ),
        ),
    )
    for tag in tags
}

################################################################################
# | VHC OBJECT LIST |
################################################################################

VHC_CONFIG_LIST: list[tuple[str, Tag, Tag | None]] = [
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

BASE_DROP_CHANCES: list[Tag] = [
    Tag.DropChance_EWO,
    Tag.DropChance_Legendary,
    Tag.DropChance_Lootable,
    Tag.DropChance_Pearlescent,
    Tag.DropChance_Hybrid,
    Tag.DropChance_EnemyEquipment,
]

CHEST_MULTIPLIERS: list[Tag] = [
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

# NOTE
#   These get overwritten by the actual values when initially loading the game objects

DEFAULT_VALUE_MAPPING: dict[Tag, AttributeDataType] = {
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
    Tag.DropChance_Hybrid: 1.0,
    Tag.DropChance_EnemyEquipment: 10.0,
    Tag.Multiplier_CrimsonChest_Legendary: 150.0,
    Tag.Multiplier_CrimsonChest_Pearlescent: 100.0,
    Tag.Multiplier_RedChest_Legendary: 100.0,
    Tag.Multiplier_RedChest_Pearlescent: 25.0,
    Tag.Multiplier_WhiteChest_Legendary: 25.0,
    Tag.Multiplier_WhiteChest_Pearlescent: 5.0,
}

FIRST_LOAD_VALUE_MAPPING: dict[Tag, AttributeDataType] = {}

LOADED_OBJECT_MAPPING: dict[Tag, UObject | None] = {tag: None for tag in Tag}
