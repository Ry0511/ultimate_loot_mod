from unrealsdk import logging
from mods_base import BaseOption

from willow1_mod_menu.util import WillowGFxMenu, ASType, find_focused_item
from willow1_mod_menu.populators import Populator

__all__ = [
    "WillowGFxMenu",
    "ASType",
    "find_focused_item",
    "extract_item_base_path",
    "get_focused_item_base_path",
    "get_menu_tag",
    "Populator",
]

last_drawn_menu: WillowGFxMenu | None = None
last_drawn_populator: Populator | None = None
last_base_path: str | None = None

def _check_last_drawn_menu() -> None:
    if last_drawn_menu is None:
        raise RuntimeError("Last drawn menu is None")


def extract_item_base_path(item: str) -> str:
    pos = item.rfind('.item')

    if pos == -1:
        raise ValueError(f'Failed to find .item in {item}')

    return item[:pos]


def get_focused_item_base_path() -> str:
    global last_base_path
    _check_last_drawn_menu()
    item = find_focused_item(last_drawn_menu)

    if len(item) == 0 and last_base_path is None:
        raise ValueError("No item is focused and last known focused item is None")
    elif len(item) > 0:
        last_base_path = extract_item_base_path(item)
    else:
        logging.dev_warning("No item is focused, using last known focused item as the base path")

    return last_base_path

def get_menu_tag(opt: BaseOption | int) -> str:

    base_path = get_focused_item_base_path()

    # Just return base_path.item{index} here
    if isinstance(opt, int):
        return f'{base_path}.item{opt}'

    # We still assume the naming convention of item{index} just stored in the option
    if not hasattr(opt, "_menu_index"):
        raise ValueError(f"Option '{opt.identifier}' does not have a _menu_index attribute")

    return f'{base_path}.item{getattr(opt, "_menu_index")}'
