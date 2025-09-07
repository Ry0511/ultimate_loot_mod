from functools import cache
from pathlib import Path

from mods_base import Library, SETTINGS_DIR

__all__ = ["UltimateLootMod", "InstalledComponents", "the_mod"]


def the_mod() -> "UltimateLootMod":
    return UltimateLootMod._instance


class InstalledComponents:
    has_arsenal: bool = False
    has_ewo: bool = False
    has_ulm: bool = False

    def __init__(self):
        self._check_for_arsenal_files()
        self._check_for_ewo_files()
        self._check_for_ulm_files()
        self.find_borderlands_dir.cache_clear()

    @cache
    def find_borderlands_dir(self) -> Path | None:
        borderlands_dir: Path | None = None

        # This generally shouldn't fail
        for parent in SETTINGS_DIR.parents:
            if parent.name.lower() == "borderlands":
                borderlands_dir = parent
                break

        return borderlands_dir

    def missing_components(self) -> bool:
        return not all((self.has_arsenal, self.has_ewo, self.has_ulm))

    def _check_for_ulm_files(self) -> None:
        if not (path := self.find_borderlands_dir()):
            return
        self.has_ulm = sum(1 for _ in path.rglob('*UltimateLoot*', case_sensitive=False)) > 0

    def _check_for_arsenal_files(self) -> None:
        if not (path := self.find_borderlands_dir()):
            return
        self.has_arsenal = sum(1 for _ in path.rglob('*The_Dust_Wastes_*', case_sensitive=False)) > 0

    def _check_for_ewo_files(self) -> None:
        if not (path := self.find_borderlands_dir()):
            return
        self.has_ewo = sum(1 for _ in path.rglob('*Eridian_Weapons_Overhaul*', case_sensitive=False)) > 0


class UltimateLootMod(Library):
    _instance: "UltimateLootMod" = None

    def __init__(self, *args, **kwargs):
        UltimateLootMod._instance = self
        super().__init__(*args, **kwargs)
        self.is_enabled = True
