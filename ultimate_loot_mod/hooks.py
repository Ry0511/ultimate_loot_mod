from unrealsdk import logging
from mods_base import hook

from .utils import sync_proxies_with_options

__all__ = [
    "hook_sync_options_state"
]


@hook("WillowGame.WillowPlayerController:SpawningProcessComplete")
def hook_sync_options_state(*_) -> None:
    sync_proxies_with_options()
    logging.info("Synced all proxy values to options")
