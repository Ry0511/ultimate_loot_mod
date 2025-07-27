from typing import Tuple
from pathlib import Path

from unrealsdk import logging
from mods_base import build_mod, Mod
from mods_base.settings import SETTINGS_DIR

from .ulm_config import ULM_CONFIG
from .ulm_object_list import ObjectTag

__version__: Tuple[int, int]

# Delete original config file if it exists
CONFIG_FILE: Path = SETTINGS_DIR / "ultimate_loot_mod.json"
CONFIG_FILE.unlink(True)


def on_enable() -> None:
    ULM_CONFIG._manual_load()
    fail_count = ULM_CONFIG.apply_to_game()
    count = len(ObjectTag)
    logging.info(f"Wrote {count - fail_count}/{count} config values")


the_mod: Mod = build_mod(
    on_enable=on_enable
)
