from typing import ClassVar, final, override

from mods_base import MODS_DIR, Library

__all__ = ["UltimateLootMod", "InstalledComponents", "the_mod"]


def the_mod() -> UltimateLootMod:
    return UltimateLootMod.instance


class InstalledComponents:
    has_arsenal: bool = False
    has_ewo: bool = False
    has_ulm: bool = False

    def __init__(self) -> None:
        for path in (MODS_DIR.parent / "WillowGame" / "CookedPC").rglob("*"):
            name = path.name.lower()
            self.has_arsenal |= "the_dust_wastes_" in name
            self.has_ewo |= "eridian_weapons_overhaul" in name
            self.has_ulm |= "ultimateloot" in name

    def missing_components(self) -> bool:
        return not all((self.has_arsenal, self.has_ewo, self.has_ulm))


@final
class UltimateLootMod(Library):
    instance: ClassVar[UltimateLootMod]

    @override
    def __post_init__(self) -> None:
        UltimateLootMod.instance = self
        super().__post_init__()
        self.is_enabled = True
