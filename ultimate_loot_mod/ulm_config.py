from typing import List
from dataclasses import dataclass, field

from unrealsdk import logging
from unrealsdk import load_package
from .ulm_object_list import ObjectTag, TagObject

__all__: List[str] = [
    "UltimateLootModConfig",
    "TagObject",
    "ULM_CONFIG",
]

type ConfigValue = int | float | bool | None


@dataclass
class UltimateLootModConfig:
    cfg: List[ConfigValue] = field(default_factory=list)
    _defaults: List[ConfigValue] = field(default_factory=list)
    _loaded: bool = False

    def _manual_load(self):

        if self._loaded:
            return

        self.cfg = [None] * len(ObjectTag)
        self._defaults = [None] * len(ObjectTag)
        for i in ObjectTag:
            proxy = TagObject(i)
            self.cfg[i.value] = proxy.get_value()
            self._defaults[i.value] = proxy.get_value(allow_default=True)

    def set(self, tag: ObjectTag, value: ConfigValue):
        self.cfg[tag.value] = value

    def get(self, tag: ObjectTag) -> ConfigValue:
        return self.cfg[tag.value]

    def overwrite_with_defaults(self):
        for i in ObjectTag:
            self.cfg[i.value] = self._defaults[i.value]

    def load_values_from_game(self):

        # This step isn't explicitly required but might as well try
        obj = load_package("UltimateLoot_Attributes_TEST.upk")
        if obj is None:
            logging.error("Failed to load UltimateLoot_Attributes_TEST.upk things might be broken")

        # Load from game values or static defaults
        for i in ObjectTag:
            proxy = TagObject(i)
            self.cfg[i.value] = proxy.get_value(allow_default=True)

    def apply_to_game(self) -> int:
        fail_count = 0
        for i in ObjectTag:
            proxy = TagObject(i)
            if not proxy.set_value(self.cfg[i.value]):
                fail_count += 1
        return fail_count


ULM_CONFIG: UltimateLootModConfig = UltimateLootModConfig()
