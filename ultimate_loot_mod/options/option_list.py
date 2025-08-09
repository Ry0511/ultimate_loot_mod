from typing import List, Callable

from unrealsdk import logging
from mods_base.options import BaseOption, ButtonOption, NestedOption, GroupedOption
from ui_utils import OptionBox, OptionBoxButton

from ..mapping.object_proxy import Tag, TagProxy
from ..mapping.internal_object_mappings import VHC_CONFIG_LIST, BASE_DROP_CHANCES, CHEST_MULTIPLIERS
from .internal_options import TagToggleOption, VHCSpinner, RaritySlider

from ..ui_edits.refresh_options import refresh_last_drawn_options

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


def _cascade_option_values(opt: BaseOption) -> None:
    def recurse_fetch_values(options):
        for opt in options:
            if isinstance(opt, (GroupedOption, NestedOption)):
                recurse_fetch_values(opt.children)
            elif hasattr(opt, "fetch_proxy_value") and callable(opt.fetch_proxy_value):
                opt.fetch_proxy_value()

    recurse_fetch_values(opt.mod.options)


# noinspection PyArgumentList
@ButtonOption("Reset Everything (Literally)")
def _button_reset_all(self: ButtonOption) -> None:
    def _on_yes() -> None:
        for tag in Tag:
            proxy = TagProxy(tag)
            proxy.set_value(proxy.default_value())

        _cascade_option_values(self)

    confirmation_box(
        message="Are you sure you want to reset everything back to their default values?",
        on_yes=_on_yes
    )

# noinspection PyArgumentList
@ButtonOption("Restore First Loaded Values")
def _button_restore_first_load_values(self: ButtonOption) -> None:
    def _on_yes() -> None:
        for tag in Tag:
            proxy = TagProxy(tag)
            proxy.set_value(proxy.first_load_value())
        _cascade_option_values(self)

    confirmation_box(
        message="Are you sure you want to restore all options to the state at which they were in "
                "when they were first loaded? \n\nThis will undo any changes you have made!",
        on_yes=_on_yes
    )


# noinspection PyArgumentList
@ButtonOption("Reset Drop Rates")
def _button_reset_drop_rates(self: ButtonOption) -> None:
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

        _cascade_option_values(self)

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
def _button_reset_drop_chances(self: ButtonOption) -> None:
    def _on_yes() -> None:
        for tag in BASE_DROP_CHANCES:
            proxy = TagProxy(tag)
            proxy.set_value(proxy.default_value())

        _cascade_option_values(self)

    confirmation_box(message="Are you sure you want to reset all drop chances to their default values?", on_yes=_on_yes)


# TODO: Might be a good idea to move this one out as it is a bit more complex than the others
# noinspection PyArgumentList
@ButtonOption("> Presets")
def _vhc_enabler_spinner(self: VHCSpinner) -> None:
    should_trigger = True

    # TODO: This could be implemented as a spinner?

    def _impl_on_select(_, btn: OptionBoxButton) -> None:

        nonlocal should_trigger

        if not should_trigger:
            logging.dev_warning(f'Why does this fire more than once?')
            return

        should_trigger = False

        def set_all(normal: bool, expanded: bool) -> None:
            for _, normal_tag, expanded_tag in VHC_CONFIG_LIST:
                TagProxy(normal_tag).set_value(normal)
                if expanded_tag is not None:
                    TagProxy(expanded_tag).set_value(expanded)

        def vhc_set_values(normal: bool, expanded: bool) -> None:
            # TagProxy(Tag.VHC_Enabler).set_value(normal)
            # TagProxy(Tag.VHC_Expanded_Enabler).set_value(expanded)
            _cascade_option_values(self)
            refresh_last_drawn_options()

        if btn.name == "All Off":
            set_all(False, False)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(False)
            vhc_set_values(False, False)

        elif btn.name == "All Normal":
            set_all(True, False)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(False)
            vhc_set_values(True, False)

        elif btn.name == "All Expanded":
            set_all(True, True)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(False)
            vhc_set_values(True, True)

        elif btn.name == "Randomizer":
            set_all(False, False)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(True)
            vhc_set_values(True, True)  # Assuming it uses both?

        elif btn.name == "Everything?":
            set_all(True, True)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(True)
            vhc_set_values(True, True)

        elif btn.name == "Random Manufacturer":
            set_all(False, False)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(False)

            from secrets import randbelow
            index = randbelow(len(VHC_CONFIG_LIST))
            _, normal, expanded = VHC_CONFIG_LIST[index]

            has_expanded = randbelow(2) == 1

            TagProxy(normal).set_value(True)
            if has_expanded and expanded is not None:
                TagProxy(expanded).set_value(has_expanded)

            vhc_set_values(True, has_expanded)
        elif btn.name == "Random Manufacturers":
            set_all(False, False)
            TagProxy(Tag.VHC_Randomizer_Enabler).set_value(False)

            from secrets import randbelow
            manufacturer_count = max(randbelow(len(VHC_CONFIG_LIST)), 2)
            to_change = dict()

            while len(to_change) < manufacturer_count:
                index = randbelow(len(VHC_CONFIG_LIST))
                tag_id, normal, expanded = VHC_CONFIG_LIST[index]
                if tag_id not in to_change:
                    to_change[tag_id] = (normal, expanded)

            has_expanded = False

            for tag_id, (normal, expanded) in to_change.items():
                TagProxy(normal).set_value(True)
                if expanded is not None:
                    v = randbelow(2) == 1
                    if v and not has_expanded:
                        has_expanded = True
                    TagProxy(expanded).set_value(v)

            vhc_set_values(True, has_expanded)

    enabler = OptionBox(
        title="Presets",
        message="Choose a preset to for Vault Hunter Challenges!",
        buttons=[
            OptionBoxButton("All Off"),
            OptionBoxButton("Randomizer"),
            OptionBoxButton("All Normal"),
            OptionBoxButton("All Expanded"),
            OptionBoxButton("Random Manufacturer"),
            OptionBoxButton("Random Manufacturers"),
            OptionBoxButton("Everything?"),
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
                _button_restore_first_load_values,
                TagToggleOption("Arsenal", Tag.Arsenal_Enabler),
                TagToggleOption("EWO", Tag.EWO_Enabler),
                NestedOption("> Vault Hunter Challenges", children=[
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
            ]
        ),
        GroupedOption("Drop Rates", children=[
            _button_reset_drop_rates,
            NestedOption("> Base Drop Chances", children=[
                _button_reset_drop_chances,
                RaritySlider("EWO Items", Tag.DropChance_EWO, step=1.0, value_suffix="%"),
                RaritySlider("Lootables", Tag.DropChance_Lootable, step=1.0, value_suffix="%"),
                RaritySlider("Legendaries", Tag.DropChance_Legendary, step=0.5, value_suffix="%"),
                RaritySlider("Pearls", Tag.DropChance_Pearlescent, step=0.1, value_suffix="%"),
            ]),
            NestedOption("> White Chest Multiplier", children=[
                RaritySlider("Legendaries", Tag.Multiplier_WhiteChest_Legendary, is_scalar=True, value_suffix="x"),
                RaritySlider("Pearls", Tag.Multiplier_WhiteChest_Pearlescent, is_scalar=True, value_suffix="x"),
            ]),
            NestedOption("> Red Chest Multiplier", children=[
                RaritySlider("Legendaries", Tag.Multiplier_RedChest_Legendary, is_scalar=True, value_suffix="x"),
                RaritySlider("Pearls", Tag.Multiplier_RedChest_Pearlescent, is_scalar=True, value_suffix="x"),
            ]),
            NestedOption("> Lance Chest Multiplier", children=[
                RaritySlider("Legendaries", Tag.Multiplier_CrimsonChest_Legendary, is_scalar=True, value_suffix="x"),
                RaritySlider("Pearls", Tag.Multiplier_CrimsonChest_Pearlescent, is_scalar=True, value_suffix="x"),
            ])
        ])
    ]
