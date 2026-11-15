from dataclasses import dataclass
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
    @dataclass
    class ComponentInfo:
        name: str
        version: str
        author: str = ""

    instance: ClassVar[UltimateLootMod]
    components: ClassVar[list[ComponentInfo]] = []
    _base_description: str = ""

    @property
    @override
    def description(self) -> str:
        if not self.components:
            return self._base_description

        entries = "".join(
            f"<li>{c.name}: {c.version}{f' by {c.author}' if c.author else ''}</li>"
            for c in sorted(self.components, key=lambda c: c.name.lower())
        )
        return f"{self._base_description}<br><br>Components:<ul>{entries}</ul>"

    @description.setter
    def description(self, value: str) -> None:  # pyright: ignore[reportIncompatibleVariableOverride]
        self._base_description = value

    @override
    def __post_init__(self) -> None:
        UltimateLootMod.instance = self
        super().__post_init__()
        self.is_enabled = True
