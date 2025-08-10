from unrealsdk import logging
from typing import runtime_checkable, Protocol, Iterable

from mods_base import BaseOption, NestedOption, GroupedOption
from .ultimate_loot_mod import the_mod

__all__ = [
    "SupportsValueSync",
    "walk_options",
    "sync_options_with_proxies",
    "sync_proxies_with_options",
]


@runtime_checkable
class SupportsValueSync(Protocol):
    def sync_with_proxy(self) -> None: ...

    def sync_proxy(self) -> None: ...


def walk_options(options: Iterable[BaseOption]) -> Iterable[BaseOption]:
    for opt in options:
        if isinstance(opt, (GroupedOption, NestedOption)):
            yield from walk_options(opt.children)
        else:
            yield opt


def sync_options_with_proxies() -> None:
    for opt in walk_options(the_mod().options):
        if isinstance(opt, SupportsValueSync):
            opt.sync_with_proxy()


def sync_proxies_with_options() -> None:
    for opt in walk_options(the_mod().options):
        if isinstance(opt, SupportsValueSync):
            opt.sync_proxy()


def has_ulm_installed() -> bool:
    return True
