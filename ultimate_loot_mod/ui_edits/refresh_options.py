from mods_base.options import BaseOption, HiddenOption, SliderOption, BoolOption, SpinnerOption, GroupedOption

from .utils import WillowGFxMenu, Populator, get_menu_tag

import ultimate_loot_mod.ui_edits.utils as utils

__all__ = [
    "refresh_last_drawn_options",
    "refresh_option",
]


################################################################################
# | REFRESH OPTIONS |
################################################################################


def refresh_slider(menu: WillowGFxMenu, opt: SliderOption) -> None:
    item_path: str = get_menu_tag(opt)
    text: str = Populator.format_slider_label(opt)

    menu.SetVariableNumber(f'{item_path}.Value', opt.value)
    menu.SetVariableString(f'{item_path}.mLabel.text', text)


def refresh_spinner(menu: WillowGFxMenu, opt: SpinnerOption) -> None:
    item_path: str = get_menu_tag(opt)

    item_index = opt.choices.index(opt.value)

    if item_index == -1:
        raise ValueError(f"Choice {opt.value} does not exist in {opt.choices}")

    menu.SetVariableNumber(f'{item_path}.mChoice', float(item_index))
    menu.SetVariableString(f'{item_path}.mValue.text', opt.choices[item_index])


def refresh_bool_option(menu: WillowGFxMenu, opt: BoolOption) -> None:
    item_path: str = get_menu_tag(opt)

    index: int = int(opt.value)
    choices: list[str] = [opt.false_text or "Off", opt.true_text or "On"]

    menu.SetVariableNumber(f'{item_path}.mChoice', float(index))
    menu.SetVariableString(f'{item_path}.mValue.text', choices[index])


def refresh_option(opt: BaseOption) -> None:
    if isinstance(opt, HiddenOption):
        return

    elif isinstance(opt, SliderOption):
        refresh_slider(utils.last_drawn_menu, opt)

    elif isinstance(opt, SpinnerOption):
        refresh_spinner(utils.last_drawn_menu, opt)

    elif isinstance(opt, BoolOption):
        refresh_bool_option(utils.last_drawn_menu, opt)

    elif isinstance(opt, GroupedOption):
        for child in opt.children:
            refresh_option(child)


def refresh_last_drawn_options() -> None:
    if (
        utils.last_drawn_menu is None
        or utils.last_drawn_populator is None
        or len(utils.last_drawn_populator.drawn_options) == 0
    ):
        return

    for opt in utils.last_drawn_populator.drawn_options:
        if hasattr(opt, "_menu_index"):
            refresh_option(opt)
