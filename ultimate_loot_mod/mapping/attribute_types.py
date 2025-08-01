__all__ = [
    "EAttributeDataType",
    "ADT_Float",
    "ADT_Int",
    "ADT_Bool",
    "ADT_MAX",
    "to_py_type",
    "AttributeDataType",
]

type EAttributeDataType = int
ADT_Float: EAttributeDataType = 0
ADT_Int: EAttributeDataType = 1
ADT_Bool: EAttributeDataType = 2
ADT_MAX: EAttributeDataType = 3

type AttributeDataType = float | int | bool


def to_py_type(ty: EAttributeDataType, val: AttributeDataType) -> AttributeDataType:
    # Generally speaking usage of Int is wrong
    if ty == ADT_Float or ty == ADT_Int:
        return round(float(val), 6)
    elif ty == ADT_Bool:
        return bool(val)
    else:
        raise AssertionError(f"Invalid AttributeDataType '{ty}'")
