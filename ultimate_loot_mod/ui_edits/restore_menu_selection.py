import math
from functools import wraps

import willow1_mod_menu as wmm
from mods_base import hook
from mods_base.options import BaseOption, NestedOption
from unrealsdk import logging
from unrealsdk.unreal import UObject, WrappedStruct
from willow1_mod_menu.populators import Populator
from willow1_mod_menu.populators.options import OptionPopulator
from willow1_mod_menu.util import ASType, WillowGFxMenu, find_focused_item

from . import utils

################################################################################
# | GLOBALS |
################################################################################

_original_opt_pop_handle_activate = wmm.options.OptionPopulator.handle_activate
_original_draw_custom_menu = wmm.options.draw_custom_menu


################################################################################
# | HELPERS |
################################################################################


def get_current_selection(menu: WillowGFxMenu) -> tuple[str, int, float] | None:
    item = find_focused_item(menu)

    if len(item) == 0:
        logging.dev_warning("Can't save selection as no item is focused")
        return None

    item_pos = item.rfind(".item")
    list_pos = item.rfind(".mList")

    if item_pos == -1 or list_pos == -1:
        logging.dev_warning(f"Path does not contain '.item' or '.mList': '{item}'")
        return None

    index_str = item[item_pos + 5 :]
    if not index_str.isnumeric():
        logging.dev_warning(f"Item path does not contain an index after '.item': '{item}'")
        return None

    ypos = menu.GetVariableNumber(f"{item[:list_pos]}.mList._y")

    # Never seen this happen but just in case; we could fallback to centerIt on the item
    if not math.isfinite(ypos):
        logging.dev_warning("Y Position is not finite")
        return None

    return item, int(index_str), ypos


def restore_selection(menu: WillowGFxMenu, populator: Populator) -> None:
    if not hasattr(populator, "_selection_info"):
        return

    item, index, ypos = getattr(populator, "_selection_info")
    delattr(populator, "_selection_info")
    original_tick_rate = menu.TickRateSeconds
    menu.TickRateSeconds = 1.0 / 60.0

    logging.misc(f"Restoring menu selection: ( '{item}', {index}, {ypos} )")

    # If it doesnt work after this many attempts then somethings gone wrong
    ticks_remaining = 10

    @hook("GearboxFramework.GearboxGFxMovie:OnTick")
    def _apply_next_tick(obj: UObject, *_) -> None:

        nonlocal item
        nonlocal index
        nonlocal ypos
        nonlocal menu
        nonlocal original_tick_rate
        nonlocal ticks_remaining

        if obj != menu:
            return

        ticks_remaining -= 1

        # Update Selection
        invoke = menu.Invoke
        params = WrappedStruct(invoke.func)
        params.args.emplace_struct(Type=ASType.AS_Number, N=index)
        params.Method = f"{item[: item.rfind('.mList')]}.mList.setSelectedItem"
        invoke(params)

        # Update Y Scroll Position
        menu.SetVariableNumber(f"{item[: item.rfind('.mList')]}.mList._y", ypos)

        # Check if the selection worked or if we timed out
        if len(find_focused_item(menu)) != 0 or ticks_remaining <= 0:
            if ticks_remaining <= 0:
                logging.error("Failed to restore selection after 10 ticks, aborting")
            menu.TickRateSeconds = original_tick_rate
            _apply_next_tick.disable()

    _apply_next_tick.enable()


################################################################################
# | WRAPPERS |
################################################################################


@wraps(wmm.options.OptionPopulator.handle_activate)
def _handle_activate_opt_populator(
    self: OptionPopulator, menu: WillowGFxMenu, option: BaseOption
) -> None:
    if (
        isinstance(option, NestedOption)
        and utils.last_drawn_populator is not None
        and utils.last_drawn_menu is not None
        and (selection := get_current_selection(utils.last_drawn_menu))
    ):
        setattr(utils.last_drawn_populator, "_selection_info", selection)

    _original_opt_pop_handle_activate(self, menu, option)


@wraps(wmm.options.draw_custom_menu)
def _draw_custom_menu(menu: WillowGFxMenu) -> None:
    populator = wmm.options.populator_stack[-1]
    utils.last_drawn_menu = menu
    utils.last_drawn_populator = populator

    _original_draw_custom_menu(menu)
    restore_selection(menu, populator)


################################################################################
# | APPLY WRAPPERS |
################################################################################

wmm.options.draw_custom_menu = _draw_custom_menu
wmm.options.OptionPopulator.handle_activate = _handle_activate_opt_populator
