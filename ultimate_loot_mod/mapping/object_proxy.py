from dataclasses import dataclass

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
]


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


@dataclass
class TagProxy:
    tag: Tag

    def __post_init__(self):
        self.tag = Tag(self.tag)

    @staticmethod
    def class_type() -> str:
        return 'AttributeDefinition'

    def path(self) -> str:
        return OBJECT_PATH_MAPPING[self.tag]

    def default_value(self) -> AttributeDataType | None:
        return DEFAULT_VALUE_MAPPING[self.tag]

    def object(self) -> UObject | None:
        return LOADED_OBJECT_MAPPING[self.tag]

    def value(self) -> AttributeDataType | None:
        if not self.try_load_object():
            return None

        try:
            return get_constant_value(self.object())
        except Exception as ex:
            logging.error(f"Failed to get value for {self.path()}: {ex}")
            return None

    def set_value(self, value: AttributeDataType) -> bool:
        if not self.try_load_object():
            return False

        try:
            return set_constant_value(self.object(), value)
        except Exception as ex:
            logging.error(f"Failed to set value for {self.path()}: {ex}")
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
                return False
        return LOADED_OBJECT_MAPPING[self.tag] is not None

    def force_int_to_float(self) -> None:
        if not self.try_load_object():
            return

        if (obj := self.object()) and obj.AttributeDataType == ADT_Int:
            obj.AttributeDataType = ADT_Float
