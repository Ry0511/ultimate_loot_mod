from collections.abc import Iterable, Sequence
from functools import wraps

import willow1_mod_menu as wmm
from mods_base import BaseOption, GroupedOption, HiddenOption, Mod, NestedOption
from willow1_mod_menu.util import WillowGFxMenu

from . import format_labels as format_labels
from . import refresh_options as refresh_options
from . import utils

__all__ = [
    "auto_tag_all_options",
]

# Grab and store the last drawn menu and populator so options can be refreshed in place
_original_draw_custom_menu = wmm.options.draw_custom_menu


@wraps(wmm.options.draw_custom_menu)
def _draw_custom_menu(menu: WillowGFxMenu) -> None:
    utils.last_drawn_menu = menu
    utils.last_drawn_populator = wmm.options.populator_stack[-1]
    _original_draw_custom_menu(menu)


wmm.options.draw_custom_menu = _draw_custom_menu


# NOTE: This has only been tested for ultimate_loot_mod so unused options/keybinds may not be
# handled correctly in the tagging process.
def auto_tag_all_options(mod: Mod, options: Sequence[BaseOption]) -> None:
    base_index = 0

    if mod.description:
        base_index += 1

    if not mod.enabling_locked:
        base_index += 1

    # TODO: This needs to be validated
    if len(mod.keybinds) > 0:
        base_index += 1

    def _recurse(base_index: int, options: Iterable[BaseOption]) -> int:
        offset = 0

        for opt in options:
            # skip/ignore hidden options
            if isinstance(opt, HiddenOption):
                continue

            setattr(opt, "_menu_index", base_index + offset)
            offset += 1

            # Grouped options are embedded into the same screen so need to be offset, taking care
            # to ensure that the offset is updated appropriately
            if isinstance(opt, GroupedOption):
                offset += _recurse(base_index + offset, opt.children)

            # Nested options are new screens and as such start at 0
            elif isinstance(opt, NestedOption):
                _ = _recurse(0, opt.children)

        return offset

    _ = _recurse(base_index, options)
