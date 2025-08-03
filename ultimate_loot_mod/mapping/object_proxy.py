from dataclasses import dataclass
from functools import wraps

from unrealsdk import load_package, find_object, logging
from unrealsdk.unreal import UObject

from mods_base import ObjectFlags

from .attribute_types import *
from .internal_object_list import Tag
from .internal_object_mappings import *

__all__ = [
    "AttributeDataType",
    "Tag",
    "TagProxy",
    "get_constant_value",
    "set_constant_value",
    "load_all_objects",
    "try_reload_current_screen",
]


################################################################################
# | HELPER FUNCTIONS |
################################################################################


def get_constant_value(obj: UObject) -> AttributeDataType:
    ty = obj.AttributeDataType
    chain = obj.ValueResolverChain
    return to_py_type(ty, chain[len(chain) - 1].ConstantValue)


def set_constant_value(obj: UObject, value: AttributeDataType) -> bool:
    ty = obj.AttributeDataType
    chain = obj.ValueResolverChain
    chain[len(chain) - 1].ConstantValue = to_py_type(ty, value)
    return True


def load_all_objects() -> int:
    fail_count = 0
    load_package("UltimateLoot_Attributes_TEST")
    load_package("UltimateLoot_Lootables_TEST")
    load_package("UltimateLoot_Pools_TEST")

    for tag in Tag:
        proxy = TagProxy(tag)
        if not proxy.try_load_object():
            fail_count += 1
    return fail_count


import willow1_mod_menu.options
from willow1_mod_menu.util import WillowGFxMenu
from willow1_mod_menu.options import draw_custom_menu as original_draw_custom_menu

_LAST_DRAWN_MENU: WillowGFxMenu | None = None


@wraps(original_draw_custom_menu)
def _store_last_menu(menu: WillowGFxMenu) -> None:
    global _LAST_DRAWN_MENU
    _LAST_DRAWN_MENU = menu
    original_draw_custom_menu(menu)


willow1_mod_menu.options.draw_custom_menu = _store_last_menu


def try_reload_current_screen() -> None:
    from willow1_mod_menu.options import draw_custom_menu
    if _LAST_DRAWN_MENU is not None:
        draw_custom_menu(_LAST_DRAWN_MENU)
    else:
        logging.dev_warning("Last drawn menu is None")


################################################################################
# | PROXY |
################################################################################

@dataclass
class TagProxy:
    tag: Tag

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TagProxy):
            return self.tag == other.tag
        return False

    @staticmethod
    def class_type() -> str:
        return 'AttributeDefinition'

    def path(self) -> str:
        return OBJECT_PATH_MAPPING[self.tag]

    def default_value(self) -> AttributeDataType | None:
        return DEFAULT_VALUE_MAPPING[self.tag]

    def object(self) -> UObject | None:
        self.try_load_object()
        return LOADED_OBJECT_MAPPING[self.tag]

    def value(self, allow_default=False) -> AttributeDataType | None:
        if not self.try_load_object():
            return self.default_value() if allow_default else None

        try:
            return get_constant_value(self.object())
        except Exception as ex:
            logging.error(f"Failed to get value for {self.path()}: {ex}")
            return self.default_value() if allow_default else None

    def set_value(self, value: AttributeDataType) -> bool:
        if not self.try_load_object():
            return False

        try:
            return set_constant_value(self.object(), value)
        except Exception as ex:
            logging.error(f"Failed to set value for {self.path()}: {ex}")
            from traceback import format_exc
            logging.error(format_exc(4))
            return False

    def try_load_object(self) -> bool:
        if LOADED_OBJECT_MAPPING[self.tag] is None:
            try:
                LOADED_OBJECT_MAPPING[self.tag] = find_object(self.class_type(), self.path())
                LOADED_OBJECT_MAPPING[self.tag].ObjectFlags |= ObjectFlags.KEEP_ALIVE
                # Seems a few of the attributes use ADT_Int when they want fractional numbers.
                # Since it is stored as a float anyway we might as well just enforce it globally
                # for all ADT_Int attributes
                self.force_int_to_float()
                return True
            except ValueError:
                logging.warning(f"Failed to load object {self.path()}")
        return LOADED_OBJECT_MAPPING[self.tag] is not None

    def force_int_to_float(self) -> None:
        if not self.try_load_object():
            return

        if (obj := self.object()) and obj.AttributeDataType == ADT_Int:
            logging.dev_warning(f"Forcing ADT_Int to ADT_Float for {self.path()}")
            obj.AttributeDataType = ADT_Float
