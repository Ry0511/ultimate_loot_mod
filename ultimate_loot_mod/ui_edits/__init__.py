from typing import Sequence, Iterable

import ultimate_loot_mod.ui_edits.format_labels
import ultimate_loot_mod.ui_edits.refresh_options

from mods_base.mod_list import base_mod

# Only enable restore menu selection if the mod menu version is <1.2
for mod in base_mod.components:
    if 'Willow1 Mod Menu' == mod.name:
        major, minor = tuple(map(lambda x: int(x), mod.version.split('.')))
        if major < 1 or (major == 1 and minor < 2):
            import ultimate_loot_mod.ui_edits.restore_menu_selection
        else:
            # Still need to grab and store the last drawn populator for other tweaks, bit of duplication here...
            from functools import wraps
            from willow1_mod_menu.util import WillowGFxMenu
            import willow1_mod_menu as wmm
            import ultimate_loot_mod.utils as utils

            _original_draw_custom_menu = wmm.options.draw_custom_menu


            @wraps(wmm.options.draw_custom_menu)
            def _draw_custom_menu(menu: WillowGFxMenu) -> None:
                utils.last_drawn_menu = menu
                utils.last_drawn_populator = wmm.options.populator_stack[-1]
                _original_draw_custom_menu(menu)


            wmm.options.draw_custom_menu = _draw_custom_menu

from mods_base import BaseOption, HiddenOption, GroupedOption, NestedOption, Mod

__all__ = [
    "auto_tag_all_options",
]


# NOTE: This has only been tested for ultimate_loot_mod so unused options/keybinds may not be
# handled correctly in the tagging process.
def auto_tag_all_options(mod: Mod, options: Sequence[BaseOption]) -> None:
    base_index = 0

    if mod.description is not None:
        base_index += 1

    if not mod.enabling_locked:
        base_index += 1

    # TODO: This needs to be validated
    if len(mod.keybinds) > 0:
        base_index += 1

    def _recurse(base_index: int, options: Iterable[BaseOption]) -> int:

        offset = 0

        for i, opt in enumerate(options):

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
                _recurse(0, opt.children)

        return offset

    _recurse(base_index, options)
