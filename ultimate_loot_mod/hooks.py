from typing import Any

from mods_base import hook
from unrealsdk import logging
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct

from .utils import sync_proxies_with_options

__all__ = ["hook_sync_options_state"]


@hook("Engine.GameInfo:PreCommitMapChange")
def hook_sync_options_state(_1: UObject, _2: WrappedStruct, _3: Any, _4: BoundFunction) -> None:
    sync_proxies_with_options()
    logging.info("Synced all proxy values to options")
