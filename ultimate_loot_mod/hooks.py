from unrealsdk import logging
from mods_base import hook

from .mapping.object_proxy import Tag, TagProxy
from .utils import sync_proxies_with_options


__all__ = [
    "hook_sync_options_state"
]

#
# These should not be required but
#

@hook("WillowGame.WillowPlayerController:SpawningProcessComplete")
def hook_sync_options_state(*_) -> None:
    sync_proxies_with_options()
    TagProxy(Tag.VHC_Enabler).set_value(False)
    TagProxy(Tag.VHC_Expanded_Enabler).set_value(False)
    logging.info("Synced all proxy values to options")
