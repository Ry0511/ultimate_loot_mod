from typing import Tuple

import ultimate_loot_mod.ui_edits  # noqa

from unrealsdk import logging
from mods_base import build_mod

from .mapping.object_proxy import Tag, load_all_objects, save_first_load_values, TagProxy
from .options.option_list import create_option_list
from .ui_edits import auto_tag_all_options
from .hooks import *

from .ultimate_loot_mod import UltimateLootMod, InstalledComponents, the_mod

import ultimate_loot_mod.options.starter_equipment  # noqa

__version__: Tuple[int, int]


def _on_enable() -> None:
    load_all_objects()


def _on_disable() -> None:
    for tag in Tag:
        TagProxy(tag).unload_object()


components = InstalledComponents()
if components.missing_components():
    logging.info("Some Ultimate Loot Mod components are missing")

load_all_objects()

build_mod(
    cls=UltimateLootMod,
    options=create_option_list(),
    hooks=[hook_sync_options_state],
    on_enable=_on_enable,
    on_disable=_on_disable,
)

auto_tag_all_options(the_mod(), the_mod().options)
save_first_load_values()

import ultimate_loot_mod.mission_rewards  # noqa

logging.info(f"Successfully loaded {the_mod().name} v{the_mod().version}")
