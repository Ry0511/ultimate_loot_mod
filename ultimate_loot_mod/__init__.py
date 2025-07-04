from typing import Tuple
from pathlib import Path

from unrealsdk import logging
from mods_base import build_mod, Mod
from mods_base.settings import SETTINGS_DIR

from .options import create_option_list

__version__: Tuple[int, int]

CONFIG_FILE: Path = SETTINGS_DIR / "ultimate_loot_mod.json"
CONFIG_FILE.unlink(True)

the_mod: Mod = build_mod(options=create_option_list())
logging.misc(f"Ultimate Loot Mod v{__version__} created by {the_mod.author}")
