from typing import Protocol, runtime_checkable, Iterable, Generator, Any
from functools import wraps

from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from unrealsdk import logging

from mods_base import hook

import willow1_mod_menu as wmm

from willow1_mod_menu.populators import Populator
from willow1_mod_menu.util import WillowGFxMenu, ASType

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

_create_nested_options_menu = wmm.options.create_nested_options_menu
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

    def set_selected_item(movie: UObject, item: str) -> None:
        item_index = int(item[item.rfind(".item") + 5:])

        logging.info(f"[UI_HELPERS] ~ Menu Focus ( '{item_index}' )")

        invoke = movie.Invoke
        params = WrappedStruct(invoke.func)
        params.args.emplace_struct(Type=ASType.AS_Number, N=item_index)
        params.Method = f'{item[:item.rfind(".mList")]}.mList.setSelectedItem'
        invoke(params)

    def set_ypos(movie: UObject, item: str, ypos: float) -> None:
        movie.SetVariableNumber(f'{item[:item.rfind(".mList")]}.mList._y', ypos)

    # Restore original menu position
    if hasattr(_last_populator, "_cached_ypos") and hasattr(_last_populator, "_cached_focused_item"):
        item = _last_populator._cached_focused_item
        ypos = _last_populator._cached_ypos
        original_tick_rate = menu.TickRateSeconds
        menu.TickRateSeconds = 1.0 / 60.0

        # You can't instantly update the selection I would assume because its potentially running
        # in parallel or async so it may not be finished til the next frame
        @hook("GearboxFramework.GearboxGFxMovie:OnTick")
        def do_this_shit_next_tick(
            obj: UObject,
            _args: WrappedStruct,
            _ret: Any,
            _func: BoundFunction,
        ) -> None:
            nonlocal item
            nonlocal ypos
            nonlocal menu
            nonlocal original_tick_rate

            if obj != menu:
                return

            # This one does not work immediately after `LobbyTools.endMenu()` is called need to wait a few frames
            set_selected_item(menu, item)

            # This seems to always work
            set_ypos(menu, item, ypos)

            # Can be the empty string, unsure why but if so then try again next tick
            focused_item = wmm.util.find_focused_item(menu)

            # Only stop trying to mess with the selection when it worked
            if len(focused_item) != 0:
                obj.TickRateSeconds = original_tick_rate
                do_this_shit_next_tick.disable()

            logging.info(f"[UI_HELPERS] ~ Menu Restore ( '{ypos}', '{item}', '{wmm.util.find_focused_item(menu)}' )")

        do_this_shit_next_tick.enable()

        delattr(_last_populator, "_cached_focused_item")
        delattr(_last_populator, "_cached_ypos")


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
    if _last_drawn_menu is None:
        raise RuntimeError("Last drawn menu is None")

    full_path = wmm.util.find_focused_item(_last_drawn_menu)
    pos = full_path.rfind(".item")

    # Should not happen, but if it does we would like to know
    if pos == -1:
        raise RuntimeError(f"Failed to get base path from '{full_path}'")

    return f'{full_path[:pos]}.item{index}'


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

    # There are more types than this but we only care about these ones
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

    # TODO: Hidden options complicate this indexing but we don't use them currently so that is fine
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
