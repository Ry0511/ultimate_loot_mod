from typing import Tuple, List
from unrealsdk import logging
from mods_base import build_mod, Mod, BaseOption

from .pkg_enablers import create_options

__version__: Tuple[int, int]

options: List[BaseOption] = list(create_options())
the_mod: Mod = build_mod(options=options)
logging.misc(f"Ultimate Loot Mod v{__version__} created by {the_mod.author}")
