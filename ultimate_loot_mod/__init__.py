from typing import Tuple
from pathlib import Path

from unrealsdk import logging
from mods_base import build_mod, Mod
from mods_base.settings import SETTINGS_DIR

from .mapping.object_proxy import Tag, load_all_objects

__version__: Tuple[int, int]

# Delete original config file if it exists
CONFIG_FILE: Path = SETTINGS_DIR / "ultimate_loot_mod.json"
CONFIG_FILE.unlink(True)


def _on_enable() -> None:
    fail_count = load_all_objects()
    total = len(Tag)
    logging.info(f"Loaded {total - fail_count}/{total} ultimate loot mod objects")


the_mod: Mod = build_mod(
    on_enable=_on_enable
)
logging.info(f"Successfully loaded {the_mod.name} v{the_mod.version}")
