from typing import List, Callable

from mods_base.options import BaseOption, ButtonOption, NestedOption, GroupedOption
from ui_utils import OptionBox, OptionBoxButton

from unrealsdk import logging

from ..mapping.object_proxy import Tag, TagProxy, try_reload_current_screen
from ..mapping.internal_object_mappings import VHC_CONFIG_LIST, BASE_DROP_CHANCES, CHEST_MULTIPLIERS
from .internal_options import TagToggleOption, VHCSpinner, RaritySlider

__all__ = [
    "create_option_list"
]


################################################################################
# | MANUAL OPTIONS |
################################################################################

def confirmation_box(message: str, on_yes: Callable[[], None]) -> None:
    def _on_select(_, btn: OptionBoxButton) -> None:
        nonlocal on_yes
        if btn.name == "Yes":
            on_yes()
            try_reload_current_screen()
        else:
            logging.info("Not resetting anything!")

    confirm = OptionBox(
        title="Confirmation",
        message=message,
        # Big temptation to randomise these to piss people off
        buttons=[OptionBoxButton("No"), OptionBoxButton("Yes")],
        on_select=_on_select
    )

    confirm.show()


# noinspection PyArgumentList
@ButtonOption("Reset Everything (Literally)")
def _button_reset_all(_: ButtonOption) -> None:
    def _on_yes() -> None:
        for tag in Tag:
            proxy = TagProxy(tag)
            proxy.set_value(proxy.default_value())

    confirmation_box(
        message="Are you sure you want to reset everything back to their default values?",
        on_yes=_on_yes
    )


# noinspection PyArgumentList
@ButtonOption("Reset All")
def _button_reset_vhc_config(_: ButtonOption) -> None:
    def _on_yes() -> None:
        has_normal = False
        has_expanded = False
        for _, normal, expanded in VHC_CONFIG_LIST:
            proxy = TagProxy(normal)
            val: bool = bool(proxy.default_value())
            has_normal = has_normal or val
            proxy.set_value(val)

            if expanded is not None:
                proxy = TagProxy(expanded)
                val: bool = bool(proxy.default_value())
                proxy.set_value(val)
                has_expanded = has_expanded or val

    confirmation_box(
        message="Are you sure you want to reset all Vault Hunter Challenges options to their default values?",
        on_yes=_on_yes
    )


# noinspection PyArgumentList
@ButtonOption("Reset All Drop Rates and Multipliers")
def _button_reset_drop_rates(_: ButtonOption) -> None:
    def _on_yes() -> None:
        for tag in iter(BASE_DROP_CHANCES + CHEST_MULTIPLIERS):
            proxy = TagProxy(tag)
            proxy.set_value(proxy.default_value())

    confirmation_box(message="Are you sure you want to reset all drop rates to their default values?", on_yes=_on_yes)


# noinspection PyArgumentList
@ButtonOption("Reset Drop Chances")
def _button_reset_drop_chances(_: ButtonOption) -> None:
    def _on_yes() -> None:
        for tag in BASE_DROP_CHANCES:
            proxy = TagProxy(tag)
            proxy.set_value(proxy.default_value())

    confirmation_box(message="Are you sure you want to reset all drop chances to their default values?", on_yes=_on_yes)


# noinspection PyArgumentList
@ButtonOption("Reset Multipliers")
def _button_reset_chest_rarities(_: ButtonOption) -> None:
    def _on_yes() -> None:
        for tag in CHEST_MULTIPLIERS:
            proxy = TagProxy(tag)
            proxy.set_value(proxy.default_value())

    confirmation_box(message="Are you sure you want to reset all chest multipliers to their default values?", on_yes=_on_yes)


################################################################################
# | OPTION LIST |
################################################################################

# noinspection PyArgumentList
def create_option_list() -> List[BaseOption]:
    return [
        GroupedOption(
            "General",
            children=[
                _button_reset_all,
                TagToggleOption("Arsenal", Tag.Arsenal_Enabler),
                TagToggleOption("EWO", Tag.EWO_Enabler),
                NestedOption("> Vault Hunter Challenges", children=[
                    _button_reset_vhc_config,
                    TagToggleOption("Randomizer", Tag.VHC_Randomizer_Enabler),
                    GroupedOption("Manufacturers", children=[
                        *[
                            VHCSpinner(identifier, normal, expanded)
                            for identifier, normal, expanded in VHC_CONFIG_LIST
                        ]
                    ])
                ]),
                TagToggleOption("Better Health", Tag.BetterHealth_Enabler),
                TagToggleOption("Pearlescent SDU's", Tag.PearlescentSDUs_Enabler),
            ]
        ),
        GroupedOption("Drop Rates", children=[
            _button_reset_drop_rates,
            NestedOption("> Base Drop Chances", children=[
                _button_reset_drop_chances,
                RaritySlider("EWO Items", Tag.DropChance_EWO, step=1.0),
                RaritySlider("Lootables", Tag.DropChance_Lootable, step=1.0),
                RaritySlider("Legendaries", Tag.DropChance_Legendary, step=0.5),
                RaritySlider("Pearls", Tag.DropChance_Pearlescent, step=0.1),
            ]),
            GroupedOption("Chest Multipliers", children=[
                _button_reset_chest_rarities,
                NestedOption("> White Chest Multiplier", children=[
                    RaritySlider("Legendaries", Tag.Multiplier_WhiteChest_Legendary, is_scalar=True),
                    RaritySlider("Pearls", Tag.Multiplier_WhiteChest_Pearlescent, is_scalar=True),
                ]),
                NestedOption("> Red Chest Multiplier", children=[
                    RaritySlider("Legendaries", Tag.Multiplier_RedChest_Legendary, is_scalar=True),
                    RaritySlider("Pearls", Tag.Multiplier_RedChest_Pearlescent, is_scalar=True),
                ]),
                NestedOption("> Lance Chest Multiplier", children=[
                    RaritySlider("Legendaries", Tag.Multiplier_CrimsonChest_Legendary, is_scalar=True),
                    RaritySlider("Pearls", Tag.Multiplier_CrimsonChest_Pearlescent, is_scalar=True),
                ])
            ])
        ])
    ]
