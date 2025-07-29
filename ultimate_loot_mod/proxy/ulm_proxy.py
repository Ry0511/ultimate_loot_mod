from dataclasses import dataclass

from unrealsdk import logging, find_object
from proxy.ulm_config import *
from proxy.ulm_object_list import *


@dataclass(frozen=True)
class ObjectProxy:
    tag: ObjectTag

    def index(self) -> int:
        return self.tag.value

    def get_path(self):
        return TAG_PATH_LIST[self.index()]

    def get_obj(self) -> AttributeDefinition | None:
        return TAG_OBJ_LIST[self.index()]

    def has_obj(self) -> bool:
        return self.get_obj() is not None

    def load_obj(self) -> bool:
        obj = TAG_OBJ_LIST[self.index()]

        if obj is not None:
            return True

        try:
            TAG_OBJ_LIST[self.index()] = find_object("AttributeDefinition", self.get_path())
            TAG_OBJ_LIST[self.index()].ObjectFlags |= 0x4000
        except Exception:  # noqa
            pass

        return TAG_OBJ_LIST[self.index()] is not None

    def set_config(self, val: AttributeDataType) -> None:
        ULM_CONFIG.set(self.tag, val)

    def set_value(self, val: AttributeDataType) -> bool:
        if not self.load_obj():
            return False

        try:
            obj = self.get_obj()
            size = len(obj.ValueResolverChain)
            if size == 0:
                logging.error(f"ValueResolverChain of {self.get_path()} is empty")
                return False
            else:
                obj.ValueResolverChain[size - 1].ConstantValue = val
        except Exception as ex:
            logging.dev_warning(f"Failed to set value for {self.get_path()}: {ex}")
            return False

        return True

    def get_value(self, allow_default=False) -> AttributeDataType | None:
        ret = self.get_static_default() if allow_default else None
        if not self.load_obj():
            return ret

        try:
            obj = self.get_obj()
            ty: EAttributeDataType = obj.AttributeDataType
            size = len(obj.ValueResolverChain)

            if size == 0:
                logging.error(f"ValueResolverChain of {self.get_path()} is empty")
                return ret

            ret: AttributeDataType = obj.ValueResolverChain[size - 1].ConstantValue

            if ty == ADT_Float:
                return round(float(ret), 6)
            elif ty == ADT_Int:
                return int(ret)
            elif ty == ADT_Bool:
                return int(ret) != 0
            else:
                return ret

        except Exception as ex:
            logging.dev_warning(f"Failed to get value for {self.get_path()}: {ex}")
            return ret

    def get_static_default(self) -> AttributeDataType:
        return TAG_STATIC_DEFAULTS[self.index()]
