from dataclasses import dataclass

from unrealsdk import load_package, find_object, logging
from unrealsdk.unreal import UObject

from mods_base import ObjectFlags  # noqa

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


################################################################################
# | HELPER FUNCTIONS |
################################################################################


def get_constant_value(obj: UObject, convert_to_py_type=True) -> AttributeDataType:
    ty = obj.AttributeDataType
    chain = obj.ValueResolverChain

    if convert_to_py_type:
        return to_py_type(ty, chain[len(chain) - 1].ConstantValue)
    else:
        return chain[len(chain) - 1].ConstantValue


def set_constant_value(obj: UObject, value: AttributeDataType) -> bool:
    ty = obj.AttributeDataType
    chain = obj.ValueResolverChain
    chain[len(chain) - 1].ConstantValue = to_py_type(ty, value)
    return True


def load_all_objects() -> bool:
    # TODO: This can cause a crash at startup. Unsure why but I would assume it is just too early
    #  to try and load a package. We don't need to load the package immediately, but it does
    #  guarantee all objects are loaded which simplifies things. I am moderately curious if using
    #  StaticLoadObject could avoid the crash here.

    load_package("UltimateLoot_Attributes_TEST")
    load_package("UltimateLoot_Lootables_TEST")

    no_errors = True

    # Try fetch and keep alive the configuration objects
    for tag in Tag:
        proxy = TagProxy(tag)

        if proxy.is_loaded():
            continue
        elif not proxy.try_load_object():
            no_errors = False
        else:
            # Update the default value to whatever the game has stored
            proxy.set_default_value(proxy.value(allow_default=True))

    return no_errors


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

    def is_loaded(self) -> bool:
        return LOADED_OBJECT_MAPPING[self.tag] is not None

    def path(self) -> str:
        return OBJECT_PATH_MAPPING[self.tag]

    def default_value(self) -> AttributeDataType | None:
        return DEFAULT_VALUE_MAPPING[self.tag]

    def first_load_value(self) -> AttributeDataType | None:
        return FIRST_LOAD_VALUE_MAPPING[self.tag]

    def object(self) -> UObject | None:
        self.try_load_object()
        return LOADED_OBJECT_MAPPING[self.tag]

    def value(self, allow_default=False, convert_to_py_type=True) -> AttributeDataType | None:
        if not self.try_load_object():
            return self.default_value() if allow_default else None

        try:
            return get_constant_value(obj=self.object(), convert_to_py_type=convert_to_py_type)
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

    def set_default_value(self, value: AttributeDataType) -> None:
        DEFAULT_VALUE_MAPPING[self.tag] = value

    def set_first_load_value(self, value: AttributeDataType) -> None:
        FIRST_LOAD_VALUE_MAPPING[self.tag] = value

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

    def unload_object(self) -> None:
        if not (obj := self.object()):
            return

        # Remove keep alive flag and clear mapping
        obj.ObjectFlags &= (~ObjectFlags.KEEP_ALIVE)
        LOADED_OBJECT_MAPPING[self.tag] = None

    def force_int_to_float(self) -> None:
        if not self.try_load_object():
            return

        if (obj := self.object()) and obj.AttributeDataType == ADT_Int:
            logging.dev_warning(f"Forcing ADT_Int to ADT_Float for {self.path()}")
            obj.AttributeDataType = ADT_Float
