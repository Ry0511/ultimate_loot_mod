from typing import Iterable

import ultimate_loot_mod.ui_edits.format_labels
import ultimate_loot_mod.ui_edits.refresh_options
import ultimate_loot_mod.ui_edits.restore_menu_selection

from mods_base import BaseOption, HiddenOption, GroupedOption, NestedOption, Mod

__all__ = [
    "auto_tag_all_options",
]


# NOTE: This has only been tested for ultimate_loot_mod so unused options/keybinds may not be
# handled correctly in the tagging process.
def auto_tag_all_options(mod: Mod) -> None:
    base_index = 0

    from willow1_mod_menu.options import ModOptionPopulator

    if mod.description is not None:
        base_index += 1

    if not mod.enabling_locked:
        base_index += 1

    if ModOptionPopulator.any_keybind_visible(tuple(mod.iter_display_options())):
        base_index += 1

    def _recurse(base_index: int, options: Iterable[BaseOption]) -> int:

        offset = 0

        for i, opt in enumerate(options):

            if isinstance(opt, HiddenOption):
                continue

            setattr(opt, "_menu_index", base_index + offset)
            offset += 1

            if isinstance(opt, GroupedOption):
                offset += _recurse(base_index + offset, opt.children)

            elif isinstance(opt, NestedOption):
                _recurse(0, opt.children)

        return offset

    _recurse(base_index, mod.options)
