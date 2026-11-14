from mods_base.options import (
    BaseOption,
    BoolOption,
    GroupedOption,
    HiddenOption,
    SliderOption,
    SpinnerOption,
)

from . import utils
from .utils import Populator, WillowGFxMenu, get_menu_tag

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

    menu.SetVariableNumber(f"{item_path}.Value", opt.value)
    menu.SetVariableString(f"{item_path}.mLabel.text", text)


def refresh_spinner(menu: WillowGFxMenu, opt: SpinnerOption) -> None:
    item_path: str = get_menu_tag(opt)

    if opt.value not in opt.choices:
        raise ValueError(f"Choice {opt.value} does not exist in {opt.choices}")

    item_index = opt.choices.index(opt.value)
    menu.SetVariableNumber(f"{item_path}.mChoice", float(item_index))
    menu.SetVariableString(f"{item_path}.mValue.text", opt.choices[item_index])


def refresh_bool_option(menu: WillowGFxMenu, opt: BoolOption) -> None:
    item_path: str = get_menu_tag(opt)

    index: int = int(opt.value)
    choices: list[str] = [opt.false_text or "Off", opt.true_text or "On"]

    menu.SetVariableNumber(f"{item_path}.mChoice", float(index))
    menu.SetVariableString(f"{item_path}.mValue.text", choices[index])


def refresh_option(menu: WillowGFxMenu, opt: BaseOption) -> None:
    if isinstance(opt, HiddenOption):
        return

    elif isinstance(opt, SliderOption):
        refresh_slider(menu, opt)

    elif isinstance(opt, SpinnerOption):
        refresh_spinner(menu, opt)

    elif isinstance(opt, BoolOption):
        refresh_bool_option(menu, opt)

    elif isinstance(opt, GroupedOption):
        for child in opt.children:
            refresh_option(menu, child)


def refresh_last_drawn_options() -> None:
    menu = utils.last_drawn_menu
    populator = utils.last_drawn_populator
    if menu is None or populator is None:
        return

    for opt in populator.drawn_options:
        if hasattr(opt, "_menu_index"):
            refresh_option(menu, opt)
