from typing import Generator, Dict

from mods_base import BoolOption
from unrealsdk import logging, find_object
from unrealsdk.unreal import UObject, WeakPointer
from math import trunc

__all__ = [
    "pkg_enabler_list",
    "pkg_enabler_objects",
    "find_pkg_enabler",
    "create_options",
]

BASE_PATH = "UltimateLoot_Attributes_TEST.Attributes._Enabler"

pkg_enabler_list = [
    "VHC_Vladof_Expanded_Enabler",
    "Arsenal_Enabler",
    "BetterHealth_Enabler",
    "EWO_Enabler",
    "VHC_Enabler",
    "PearlescentSDUs_Enabler",
    "VHC_Atlas_Enabler",
    "VHC_Atlas_Expanded_Enabler",
    "VHC_Dahl_Enabler",
    "VHC_Dahl_Expanded_Enabler",
    "VHC_Expanded_Enabler",
    "VHC_Gearbox_Enabler",
    "VHC_Hyperion_Enabler",
    "VHC_Hyperion_Expanded_Enabler",
    "VHC_Jakobs_Enabler",
    "VHC_Jakobs_Expanded_Enabler",
    "VHC_Maliwan_Enabler",
    "VHC_Maliwan_Expanded_Enabler",
    "VHC_Randomizer_Enabler",
    "VHC_SandS_Enabler",
    "VHC_SandS_Expanded_Enabler",
    "VHC_Tediore_Enabler",
    "VHC_Tediore_Expanded_Enabler",
    "VHC_Torgue_Enabler",
    "VHC_Torgue_Expanded_Enabler",
    "VHC_Vladof_Enabler",
]

pkg_enabler_objects: Dict[str, WeakPointer] = {
    "VHC_Vladof_Expanded_Enabler": WeakPointer(),
    "Arsenal_Enabler": WeakPointer(),
    "BetterHealth_Enabler": WeakPointer(),
    "EWO_Enabler": WeakPointer(),
    "VHC_Enabler": WeakPointer(),
    "PearlescentSDUs_Enabler": WeakPointer(),
    "VHC_Atlas_Enabler": WeakPointer(),
    "VHC_Atlas_Expanded_Enabler": WeakPointer(),
    "VHC_Dahl_Enabler": WeakPointer(),
    "VHC_Dahl_Expanded_Enabler": WeakPointer(),
    "VHC_Expanded_Enabler": WeakPointer(),
    "VHC_Gearbox_Enabler": WeakPointer(),
    "VHC_Hyperion_Enabler": WeakPointer(),
    "VHC_Hyperion_Expanded_Enabler": WeakPointer(),
    "VHC_Jakobs_Enabler": WeakPointer(),
    "VHC_Jakobs_Expanded_Enabler": WeakPointer(),
    "VHC_Maliwan_Enabler": WeakPointer(),
    "VHC_Maliwan_Expanded_Enabler": WeakPointer(),
    "VHC_Randomizer_Enabler": WeakPointer(),
    "VHC_SandS_Enabler": WeakPointer(),
    "VHC_SandS_Expanded_Enabler": WeakPointer(),
    "VHC_Tediore_Enabler": WeakPointer(),
    "VHC_Tediore_Expanded_Enabler": WeakPointer(),
    "VHC_Torgue_Enabler": WeakPointer(),
    "VHC_Torgue_Expanded_Enabler": WeakPointer(),
    "VHC_Vladof_Enabler": WeakPointer(),
}


def find_pkg_enabler(name: str) -> UObject | None:
    full_path = BASE_PATH + "." + name
    try:
        return find_object("AttributeDefinition", full_path)
    except ValueError:
        logging.info(f"Failed to find object '{full_path}'")
        return None


def create_options() -> Generator[BoolOption, None, None]:
    def on_change(self: BoolOption, value: bool):
        name = getattr(self, "pkg_name")
        if name not in pkg_enabler_objects:
            logging.misc(f"Option doesn't exist in list '{name}'")
            return

        obj = pkg_enabler_objects[name]()

        if obj is None:
            obj = find_pkg_enabler(name)
            if obj is not None:
                pkg_enabler_objects[name].replace(obj)
            else:
                return

        obj.ValueResolverChain[0].ConstantValue = 1.0 if value else 0.0

    for pkg_enabler in pkg_enabler_list:
        obj: UObject | None = find_pkg_enabler(pkg_enabler)
        dflt_value = True

        if obj is not None:
            pkg_enabler_objects[pkg_enabler] = WeakPointer(obj)
            val = obj.ValueResolverChain[0].ConstantValue
            logging.info(f"[{pkg_enabler:<32}] ~ {val}, {obj}")
            dflt_value = trunc(val) != 0
            obj.ObjectFlags |= 0x4000

        opt = BoolOption(pkg_enabler.replace("_", " "), value=dflt_value, on_change=on_change)
        setattr(opt, "pkg_name", pkg_enabler)
        yield opt
