from mods_base import build_mod
from unrealsdk import logging

from . import ui_edits as ui_edits
from .hooks import hook_sync_options_state
from .mapping.object_proxy import Tag, TagProxy, load_all_objects, save_first_load_values
from .options import starter_equipment as starter_equipment
from .options.option_list import create_option_list
from .ui_edits import auto_tag_all_options
from .ultimate_loot_mod import InstalledComponents, UltimateLootMod, the_mod

__version__: tuple[int, int]


def _on_enable() -> None:
    _ = load_all_objects()


def _on_disable() -> None:
    for tag in Tag:
        TagProxy(tag).unload_object()


components = InstalledComponents()
if components.missing_components():
    logging.info("Some Ultimate Loot Mod components are missing")

_ = load_all_objects()

_ = build_mod(
    cls=UltimateLootMod,
    options=create_option_list(),
    hooks=[hook_sync_options_state],
    on_enable=_on_enable,
    on_disable=_on_disable,
)

auto_tag_all_options(the_mod(), the_mod().options)
save_first_load_values()

from . import mission_rewards as mission_rewards  # noqa: E402

logging.info(f"Successfully loaded {the_mod().name} v{the_mod().version}")
