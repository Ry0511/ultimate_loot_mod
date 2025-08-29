from enum import Enum, auto

__all__ = [
    "Tag"
]


class Tag(Enum):

    @staticmethod
    def _generate_next_value_(_0, _1, count, _2):
        return count

    ################################################################################
    # | STANDARD ENABLERS |
    ################################################################################

    Arsenal_Enabler = auto()
    BetterHealth_Enabler = auto()
    EWO_Enabler = auto()
    PearlescentSDUs_Enabler = auto()

    ################################################################################
    # | VAULT HUNTER CHALLENGES |
    ################################################################################

    VHC_Enabler = auto()
    VHC_Expanded_Enabler = auto()

    VHC_Gearbox_Enabler = auto()
    VHC_Randomizer_Enabler = auto()

    VHC_Atlas_Enabler = auto()
    VHC_Atlas_Expanded_Enabler = auto()
    VHC_Dahl_Enabler = auto()
    VHC_Dahl_Expanded_Enabler = auto()
    VHC_Hyperion_Enabler = auto()
    VHC_Hyperion_Expanded_Enabler = auto()
    VHC_Jakobs_Enabler = auto()
    VHC_Jakobs_Expanded_Enabler = auto()
    VHC_Maliwan_Enabler = auto()
    VHC_Maliwan_Expanded_Enabler = auto()
    VHC_SandS_Enabler = auto()
    VHC_SandS_Expanded_Enabler = auto()
    VHC_Tediore_Enabler = auto()
    VHC_Tediore_Expanded_Enabler = auto()
    VHC_Torgue_Enabler = auto()
    VHC_Torgue_Expanded_Enabler = auto()
    VHC_Vladof_Enabler = auto()
    VHC_Vladof_Expanded_Enabler = auto()

    ################################################################################
    # | DROP CHANCE MODIFIERS |
    ################################################################################

    DropChance_EWO = auto()

    DropChance_Lootable = auto()
    DropChance_Legendary = auto()
    DropChance_Pearlescent = auto()
    DropChance_Hybrid = auto()

    Multiplier_CrimsonChest_Legendary = auto()
    Multiplier_CrimsonChest_Pearlescent = auto()
    Multiplier_RedChest_Legendary = auto()
    Multiplier_RedChest_Pearlescent = auto()
    Multiplier_WhiteChest_Legendary = auto()
    Multiplier_WhiteChest_Pearlescent = auto()
