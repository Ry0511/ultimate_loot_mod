from unrealsdk import logging
from mods_base import Mod

__all__ = ["UltimateLootMod", "the_mod"]


def the_mod() -> "UltimateLootMod":
    return UltimateLootMod._instance


class UltimateLootMod(Mod):
    _instance: "UltimateLootMod" = None

    def __init__(self, *args, **kwargs):
        logging.info("UltimateLootMod instantiated")
        UltimateLootMod._instance = self
        super().__init__(*args, **kwargs)
