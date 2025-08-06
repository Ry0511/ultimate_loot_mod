from typing import Protocol, runtime_checkable, Iterable, Generator
from functools import wraps

from unrealsdk.unreal import UObject
from unrealsdk import logging

import willow1_mod_menu as wmm
from willow1_mod_menu.populators import Populator
from willow1_mod_menu.util import WillowGFxMenu

from mods_base import (
    Mod,
    BaseOption,
    NestedOption,
    GroupedOption,
    SliderOption,
    SpinnerOption,
    BoolOption
)

__all__ = [
    "SupportsCreateFormatLabel",
    "item_path",
    "update_slider_option",
    "update_spinner_option",
    "update_drawn_items",
    "update_option",
    "set_all_menu_tags",
    "iterate_last_drawn_items",
]

################################################################################
# | GLOBALS |
################################################################################

# TODO: I doubt this is the path for the ingame pause menu option list
BASE_ITEM_PATH = "_level0.menu.selections.mMenu.mList"

_draw_custom_menu = wmm.options.draw_custom_menu
_fmt_slider_label = wmm.populators.Populator.format_slider_label

_last_drawn_menu: WillowGFxMenu | None = None
_last_populator: Populator | None = None


################################################################################
# | STORE LAST MENU |
################################################################################

@wraps(wmm.options.draw_custom_menu)
def _store_last_menu(menu: WillowGFxMenu) -> None:
    global _last_drawn_menu
    global _last_populator
    _last_drawn_menu = menu
    _last_populator = wmm.options.populator_stack[-1]
    _draw_custom_menu(menu)


wmm.options.draw_custom_menu = _store_last_menu


################################################################################
# | LABELS |
################################################################################

@runtime_checkable
class SupportsCreateFormatLabel(Protocol):
    def create_format_label(self) -> str: ...


@wraps(wmm.populators.Populator.format_slider_label)
def format_slider_label(option: SliderOption) -> str:
    if isinstance(option, SupportsCreateFormatLabel):
        return option.create_format_label()

    return _fmt_slider_label(option)


wmm.populators.Populator.format_slider_label = staticmethod(format_slider_label)


################################################################################
# | HELPERS |
################################################################################

def item_path(index: int) -> str:
    return f"{BASE_ITEM_PATH}.item{index}"


def lobby_tools() -> UObject:
    return _last_drawn_menu.LobbyTools.Movie


def iterate_last_drawn_items() -> Generator[BaseOption, None, None]:
    if _last_drawn_menu is None:
        yield from ()

    def recurse(opt: Iterable[BaseOption]) -> Generator[BaseOption, None, None]:
        for opt in opt:
            if isinstance(opt, GroupedOption):
                yield from recurse(opt.children)
            elif not isinstance(opt, NestedOption):
                yield opt

    yield from recurse(_last_populator.drawn_options)


def update_slider_option(index: int, option: SliderOption) -> None:
    pth = item_path(index)
    lobby_tools().SetVariableNumber(f'{pth}.Value', option.value)
    lobby_tools().SetVariableString(f'{pth}.mLabel.text', format_slider_label(option))


def update_spinner_option(index: int, option: SpinnerOption | BoolOption) -> None:
    pth = item_path(index)
    item_index = -1
    option_text = None

    if isinstance(option, SpinnerOption):
        for i, choice in enumerate(option.choices):
            if choice == option.value:
                item_index = i
                option_text = choice
                break
    else:
        item_index = 1 if option.value else 0
        option_text = "On" if option.value else "Off"

    # Update the index and the current value text
    lobby_tools().SetVariableNumber(f'{pth}.mChoice', float(item_index))
    lobby_tools().SetVariableString(f'{pth}.mValue.text', option_text)


def update_option(opt: BaseOption, check_drawn_options=False) -> None:
    if not hasattr(opt, "menu_index"):
        set_all_menu_tags(opt.mod)

    if check_drawn_options:
        if opt not in _last_populator.drawn_options:
            return

    if isinstance(opt, SliderOption):
        update_slider_option(getattr(opt, "menu_index"), opt)
    elif isinstance(opt, SpinnerOption | BoolOption):
        update_spinner_option(getattr(opt, "menu_index"), opt)
    elif isinstance(opt, GroupedOption):
        for child in opt.children:
            update_option(child)


def set_all_menu_tags(start_index: int, mod: Mod) -> None:
    if getattr(mod, "_menu_tags_set", False):
        return

    # TODO: Hidden options complicate this indexing but we don't use them so /shrug
    def recurse_set_tags(base_index: int, items: Iterable[BaseOption]) -> None:

        for i, opt in enumerate(items):

            # Force set for all items
            setattr(opt, "menu_index", base_index + i)

            if isinstance(opt, GroupedOption):
                recurse_set_tags(base_index=(base_index + i + 1), items=opt.children)
                base_index += len(opt.children)
            elif isinstance(opt, NestedOption):
                recurse_set_tags(base_index=0, items=opt.children)

    recurse_set_tags(start_index, mod.options)
    setattr(mod, "_menu_tags_set", True)


def update_drawn_items() -> None:
    if _last_drawn_menu is None or _last_populator is None:
        logging.dev_warning(f"Can't update drawn items: {_last_drawn_menu}, {_last_populator}")
        return

    # No options have been drawn yet
    if _last_populator.drawn_options is None or len(_last_populator.drawn_options) == 0:
        return

    # Force all drawn options to update
    for opt in iterate_last_drawn_items():
        if opt.mod is None:
            continue
        update_option(opt)
