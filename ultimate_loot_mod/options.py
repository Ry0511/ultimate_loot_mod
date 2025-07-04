from typing import List

from unrealsdk import logging
from mods_base.options import BaseOption, NestedOption, GroupedOption, ButtonOption
from .object_tags import *


def restore_everything(_: ButtonOption) -> None:
    logging.info("Not implemented yet")


def restore_vhc_defaults(_: ButtonOption) -> None:
    logging.info("Not implemented yet")


def create_option_list() -> List[BaseOption]:
    def get(tag: ObjectTag) -> BaseOption:
        return OPTION_MAPPING[tag]

    ls: List[BaseOption] = [
        GroupedOption("Weapon Toggles", children=[
            get(ObjectTag.Arsenal),
            get(ObjectTag.EWO),
            get(ObjectTag.VHC),
        ]),
        GroupedOption("Quality of Life", children=[
            ButtonOption("Reset to defaults (everything)", on_press=restore_everything),
            get(ObjectTag.BetterHealth),
            get(ObjectTag.PearlescentSDUs),
            NestedOption("Presets", children=[
                get(ObjectTag.EWO_DropChance),
                get(ObjectTag.Shared_Chance_Legendary),
                get(ObjectTag.Shared_Chance_Pearlescent),
                get(ObjectTag.Shared_Chance_Lootable),
            ]),
            NestedOption("Drop Rates", children=[
                get(ObjectTag.EWO_DropChance),
                get(ObjectTag.Shared_Chance_Legendary_A),
                get(ObjectTag.Shared_Chance_Pearlescent_A),
                get(ObjectTag.Shared_Chance_Lootable_A),
            ])
        ]),
        NestedOption("Vault Hunter Challenges", children=[
            GroupedOption("Primary", children=[
                get(ObjectTag.VHC),
                ButtonOption("Reset to defaults", on_press=restore_vhc_defaults)
            ]),
            GroupedOption("Config", children=[
                get(ObjectTag.VHC_Randomizer),
                get(ObjectTag.VHC_Gearbox),
                get(ObjectTag.VHC_Atlas),
                get(ObjectTag.VHC_Dahl),
                get(ObjectTag.VHC_Hyperion),
                get(ObjectTag.VHC_Jakobs),
                get(ObjectTag.VHC_Maliwan),
                get(ObjectTag.VHC_SandS),
                get(ObjectTag.VHC_Tediore),
                get(ObjectTag.VHC_Torgue),
                get(ObjectTag.VHC_Vladof),
            ])
        ])
    ]

    return ls
