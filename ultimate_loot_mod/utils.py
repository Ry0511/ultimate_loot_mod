from typing import runtime_checkable, Protocol, Iterable

from unrealsdk.unreal import UObject, UClass
from unrealsdk import find_class
from mods_base import BaseOption, NestedOption, GroupedOption
from .ultimate_loot_mod import the_mod

__all__ = [
    "SupportsValueSync",
    "walk_options",
    "sync_options_with_proxies",
    "sync_proxies_with_options",
    "dynamic_load_object",
]

_obj_class: UClass | None = None


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


def dynamic_load_object(obj_class: str | UClass, obj_name: str, may_fail: bool = False) -> UObject:
    global _obj_class

    if _obj_class is None:
        _obj_class = find_class('Core.Object')

    found_cls: UClass

    # Get the objects class
    if isinstance(obj_class, str):
        found_cls = find_class(obj_class)
    else:
        found_cls = obj_class

    # Attempt to load the object
    obj: UObject = _obj_class.ClassDefaultObject.DynamicLoadObject(obj_name, found_cls, may_fail)

    # Assume this can only happen if may_fail is True?
    if obj is None:
        raise ValueError(f"Failed to load object '{obj_name}' of class '{obj_class}'")

    return obj
