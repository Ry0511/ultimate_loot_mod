from typing import Tuple
from pathlib import Path

from unrealsdk import logging
from mods_base import build_mod, Mod
from mods_base.settings import SETTINGS_DIR

from .mapping.object_proxy import Tag, load_all_objects, TagProxy
from .options.option_list import create_option_list

from . import ui_edits  # noqa
from .ui_edits import auto_tag_all_options

from .options.lazy_loading_sequence import LazyLoadedOptionSequence

# from .ui_helpers import set_all_menu_tags

__version__: Tuple[int, int]

# Delete original config file if it exists
CONFIG_FILE: Path = SETTINGS_DIR / "ultimate_loot_mod.json"
CONFIG_FILE.unlink(True)


def _on_enable() -> None:
    auto_tag_all_options(the_mod, the_mod.options)
    if load_all_objects():
        return

    failed_list = [tag.name for tag in Tag if not TagProxy(tag).object()]
    logging.warning(f'Failed to load: {", ".join(failed_list)} ultimate loot mod objects')


def _on_disable() -> None:
    for tag in Tag:
        TagProxy(tag).unload_object()


def _on_load_options():
    load_all_objects()
    return create_option_list()


the_mod: Mod = build_mod(
    on_enable=_on_enable,
    on_disable=_on_disable,
    options=LazyLoadedOptionSequence(loader_func=_on_load_options),
)

logging.info(f"Successfully loaded {the_mod.name} v{the_mod.version}")
