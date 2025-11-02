from typing import List, Callable

from unrealsdk import logging
from mods_base.options import BaseOption, ButtonOption, NestedOption, GroupedOption
from ui_utils import OptionBox, OptionBoxButton

from ..mapping.object_proxy import Tag, TagProxy
from ..mapping.internal_object_mappings import VHC_CONFIG_LIST, BASE_DROP_CHANCES, CHEST_MULTIPLIERS
from .internal_options import TagToggleOption, VHCSpinner, RaritySlider

from ..ui_edits.refresh_options import refresh_last_drawn_options
from ..utils import sync_options_with_proxies

from .starter_equipment import create_starter_equipment_options

__all__ = [
    "create_option_list",
]


################################################################################
# | MANUAL OPTIONS |
################################################################################

def confirmation_box(message: str, on_yes: Callable[[], None]) -> None:
    trigger_update: bool = True

    def _on_select(_, btn: OptionBoxButton) -> None:
        nonlocal on_yes
        nonlocal trigger_update

        if not trigger_update:
            logging.dev_warning('Confirmation option box has triggered twice?')

        # Seems this will fire twice?
        if btn.name == "Yes" and trigger_update:
            on_yes()
            refresh_last_drawn_options()
            trigger_update = False

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

        sync_options_with_proxies()

    confirmation_box(
        message="Are you sure you want to reset everything back to their default values?",
        on_yes=_on_yes
    )


# noinspection PyArgumentList
@ButtonOption("Restore First Loaded Values")
def _button_restore_first_load_values(_: ButtonOption) -> None:
    def _on_yes() -> None:
        for tag in Tag:
            proxy = TagProxy(tag)
            proxy.set_value(proxy.first_load_value())

        sync_options_with_proxies()

    confirmation_box(
        message="Are you sure you want to restore all options to the state at which they were in "
                "when they were first loaded? \n\nThis will undo any changes you have made!",
        on_yes=_on_yes
    )


# noinspection PyArgumentList
@ButtonOption("Reset Drop Rates")
def _button_reset_drop_rates(_: ButtonOption) -> None:
    def _on_select(_, btn: OptionBoxButton) -> None:
        if btn.name == "Nothing!":
            return

        elif btn.name == "Drop Rates":
            for tag in BASE_DROP_CHANCES:
                proxy = TagProxy(tag)
                proxy.set_value(proxy.default_value())

        elif btn.name == "Chest Multipliers":
            for tag in CHEST_MULTIPLIERS:
                proxy = TagProxy(tag)
                proxy.set_value(proxy.default_value())

        elif btn.name == "Drop Rates and Multipliers":
            for tag in BASE_DROP_CHANCES + CHEST_MULTIPLIERS:
                proxy = TagProxy(tag)
                proxy.set_value(proxy.default_value())

        sync_options_with_proxies()

    box = OptionBox(
        title="Confirmation",
        message="Select what you want to reset back to their default values",
        buttons=[
            OptionBoxButton("Nothing!"),
            OptionBoxButton("Drop Rates"),
            OptionBoxButton("Chest Multipliers"),
            OptionBoxButton("Drop Rates and Multipliers"),
        ],
        on_select=_on_select
    )

    box.show()


# noinspection PyArgumentList
@ButtonOption("Reset Drop Chances")
def _button_reset_drop_chances(_: ButtonOption) -> None:
    def _on_yes() -> None:
        for tag in BASE_DROP_CHANCES:
            proxy = TagProxy(tag)
            proxy.set_value(proxy.default_value())

        sync_options_with_proxies()

    confirmation_box(
        message="Are you sure you want to reset all drop chances to their default values?",
        on_yes=_on_yes
    )


# TODO: Might be a good idea to move this one out as it is a bit more complex than the others
# noinspection PyArgumentList
@ButtonOption("> Presets")
def _vhc_enabler_spinner(_: VHCSpinner) -> None:

    def _impl_on_select(_, btn: OptionBoxButton) -> None:

        def set_all(normal: bool, expanded: bool) -> None:
            for _, normal_tag, expanded_tag in VHC_CONFIG_LIST:
                TagProxy(normal_tag).set_value(normal)
                if expanded_tag is not None:
                    TagProxy(expanded_tag).set_value(expanded)

        def vhc_sync_values() -> None:
            sync_options_with_proxies()
            refresh_last_drawn_options()

        if btn.name == "All Off":
            set_all(False, False)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(False)
            vhc_sync_values()

        elif btn.name == "All Normal":
            set_all(True, False)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(False)
            vhc_sync_values()

        elif btn.name == "All Expanded":
            set_all(True, True)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(False)
            vhc_sync_values()

        elif btn.name == "Randomizer":
            set_all(False, False)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(True)
            vhc_sync_values()

    enabler = OptionBox(
        title="Presets",
        message="Choose a preset to for Vault Hunter Challenges!",
        buttons=[
            OptionBoxButton("All Off"),
            OptionBoxButton("All Normal"),
            OptionBoxButton("All Expanded"),
            OptionBoxButton("Randomizer"),
        ],
        on_select=_impl_on_select
    )

    enabler.show()


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
                NestedOption("Vault Hunter Challenges", children=[
                    _vhc_enabler_spinner,
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
                create_starter_equipment_options(),
            ]
        ),
        GroupedOption("Drop Rates", children=[
            _button_reset_drop_rates,
            NestedOption("Base Drop Chances", children=[
                RaritySlider("EWO Equipment", Tag.DropChance_EWO, step=1.0, value_suffix="%"),
                RaritySlider("VHC Hybrids", Tag.DropChance_Hybrid, step=0.5, value_suffix="%"),
                RaritySlider("Enemy Equipment", Tag.DropChance_EnemyEquipment, step=1.0, value_suffix="%"),
                RaritySlider("Lootables", Tag.DropChance_Lootable, step=1.0, value_suffix="%"),
                RaritySlider("Legendaries", Tag.DropChance_Legendary, step=0.5, value_suffix="%"),
                RaritySlider("Pearls", Tag.DropChance_Pearlescent, step=0.1, value_suffix="%"),
            ]),
            NestedOption("White Chest Multiplier", children=[
                RaritySlider("Legendaries", Tag.Multiplier_WhiteChest_Legendary, is_scalar=True, value_suffix="x"),
                RaritySlider("Pearls", Tag.Multiplier_WhiteChest_Pearlescent, is_scalar=True, value_suffix="x"),
            ]),
            NestedOption("Red Chest Multiplier", children=[
                RaritySlider("Legendaries", Tag.Multiplier_RedChest_Legendary, is_scalar=True, value_suffix="x"),
                RaritySlider("Pearls", Tag.Multiplier_RedChest_Pearlescent, is_scalar=True, value_suffix="x"),
            ]),
            NestedOption("Lance Chest Multiplier", children=[
                RaritySlider("Legendaries", Tag.Multiplier_CrimsonChest_Legendary, is_scalar=True, value_suffix="x"),
                RaritySlider("Pearls", Tag.Multiplier_CrimsonChest_Pearlescent, is_scalar=True, value_suffix="x"),
            ])
        ])
    ]
