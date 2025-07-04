from typing import Dict
from enum import Enum

from dataclasses import dataclass, field

from unrealsdk import find_object, find_class, logging
from unrealsdk.unreal import UObject, UClass
from mods_base.options import BaseOption, BoolOption, SpinnerOption, SliderOption

__all__ = [
    "LazyObject",
    "ObjectTag",
    "OPTION_MAPPING",
]


@dataclass(eq=False)
class LazyObject:
    _path: str
    _class: str | UClass
    _load_immediately: bool = False
    _obj: UObject | None = field(default=None)

    def __post_init__(self):
        if not self._load_immediately:
            return
        self.try_load()

    def try_load(self) -> bool:
        if self._obj is not None:
            return True

        try:
            self._obj = find_object(self._class, self._path)
            self._obj.ObjectFlags |= 0x4000
            return True
        except ValueError:
            return False

    def is_loaded(self) -> bool:
        return self._obj is not None

    def get(self) -> UObject | None:
        if self._obj is None and not self.try_load():
            return None
        return self._obj

    def __call__(self) -> UObject | None:
        return self.get()


ATTR_CLASS: str | UClass

try:
    ATTR_CLASS = find_class("AttributeDefinition")
except ValueError:
    logging.misc("AttributeDefinition class not found, using path-name instead")
    ATTR_CLASS = "AttributeDefinition"


# @formatter:off

class ObjectTag(Enum):
    BetterHealth          = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.BetterHealth_Enabler')
    PearlescentSDUs       = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.PearlescentSDUs_Enabler')
    Arsenal               = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.Arsenal_Enabler')
    EWO                   = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.EWO_Enabler')
    EWO_DropChance        = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes.EWO.DropChance.DropChance_EWO')
    VHC                   = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Enabler')
    VHC_Expanded          = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Expanded_Enabler')
    VHC_Randomizer        = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Randomizer_Enabler')
    VHC_Gearbox           = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Gearbox_Enabler')

    VHC_Atlas             = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Atlas_Enabler')
    VHC_Atlas_Expanded    = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Atlas_Expanded_Enabler')
    VHC_Dahl              = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Dahl_Enabler')
    VHC_Dahl_Expanded     = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Dahl_Expanded_Enabler')
    VHC_Hyperion          = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Hyperion_Enabler')
    VHC_Hyperion_Expanded = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Hyperion_Expanded_Enabler')
    VHC_Jakobs            = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Jakobs_Enabler')
    VHC_Jakobs_Expanded   = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Jakobs_Expanded_Enabler')
    VHC_Maliwan           = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Maliwan_Enabler')
    VHC_Maliwan_Expanded  = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Maliwan_Expanded_Enabler')
    VHC_SandS             = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_SandS_Enabler')
    VHC_SandS_Expanded    = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_SandS_Expanded_Enabler')
    VHC_Tediore           = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Tediore_Enabler')
    VHC_Tediore_Expanded  = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Tediore_Expanded_Enabler')
    VHC_Torgue            = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Torgue_Enabler')
    VHC_Torgue_Expanded   = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Torgue_Expanded_Enabler')
    VHC_Vladof            = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Vladof_Enabler')
    VHC_Vladof_Expanded   = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes._Enabler.VHC_Vladof_Expanded_Enabler')

    # TODO: Order fighting will occur on these objects
    Shared_Chance_Common      = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Common')
    Shared_Chance_Legendary   = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Legendary')
    Shared_Chance_Pearlescent = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Pearlescent')
    Shared_Chance_Lootable    = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Lootable')

    # Advanced Tags
    Shared_Chance_Common_A      = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Common')
    Shared_Chance_Legendary_A   = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Legendary')
    Shared_Chance_Pearlescent_A = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Pearlescent')
    Shared_Chance_Lootable_A    = LazyObject(_class=ATTR_CLASS, _path='UltimateLoot_Attributes_TEST.Attributes.Shared.DropChance.DropChance_Lootable')


# @formatter:on

class ToggleOption(BoolOption):
    tag: ObjectTag

    def __init__(self, identifier: str, tag: ObjectTag):
        self.tag = tag

        # Try load the value directly from unreal if we can
        if obj := tag.value():
            val = round(obj.ValueResolverChain[0].ConstantValue) != 0
        else:
            val = tag in (ObjectTag.EWO, ObjectTag.Arsenal)

        super().__init__(identifier=identifier, value=val, on_change=ToggleOption.on_change)

    @staticmethod
    def on_change(self: "ToggleOption", value: bool):
        obj = self.tag.value()
        if obj is None:
            logging.error(f"Failed to find object '{self.tag}'")
            return

        val = 1.0 if value else 0.0
        obj.ValueResolverChain[0].ConstantValue = val
        logging.misc(f"Setting {self.tag} to {val}")


class VHCSpinner(SpinnerOption):
    tag: ObjectTag
    expanded: ObjectTag | None

    def __init__(self, identifier: str, tag: ObjectTag, expanded: ObjectTag | None = None):
        self.tag = tag
        self.expanded = expanded

        super().__init__(
            identifier=identifier,
            value="Off",
            choices=["Off", "Normal", "Expanded"],
            on_change=self.on_change
        )

    def _get_normal_state(self) -> bool:
        if obj := self.tag.value():
            return round(obj.ValueResolverChain[0].ConstantValue) != 0
        return False

    def _get_expanded_state(self) -> bool:
        if self.expanded is not None and (obj := self.expanded.value()):
            return round(obj.ValueResolverChain[0].ConstantValue) != 0
        return False

    def _get_value_state(self) -> str:
        is_normal = self._get_normal_state()
        is_expanded = self._get_expanded_state()

        if is_normal:
            return "Normal"
        elif is_expanded:
            return "Expanded"
        else:
            return "Off"

    def _set_all(self, normal_val: float, expanded_val: float) -> bool:
        no_errors = True

        if obj := self.tag.value():
            obj.ValueResolverChain[0].ConstantValue = normal_val
        else:
            logging.error(f"Failed to find object '{self.tag}'")
            no_errors = False

        if self.expanded is not None and (obj := self.expanded.value()):
            obj.ValueResolverChain[0].ConstantValue = expanded_val
        elif self.expanded is not None:
            logging.error(f"Failed to find object '{self.expanded}'")
            no_errors = False

        return no_errors

    @staticmethod
    def on_change(self: "VHCSpinner", val: str) -> None:
        if val == "Off":
            self._set_all(0.0, 0.0)
        elif val == "Normal":
            self._set_all(1.0, 0.0)
        elif val == "Expanded":
            self._set_all(0.0, 1.0)


class RaritySpinner(SpinnerOption):
    tag: ObjectTag

    @staticmethod
    def rarity_to_value(rarity: str) -> float:
        match rarity:
            case "Common":
                return 100.0
            case "Uncommon":
                return 40.0
            case "Rare":
                return 20.0
            case "Ultra Rare":
                return 8.0
            case "Legendary":
                return 2.0
            case "Pearlescent":
                return 0.1
            case "Bloodless":
                return 0.0000000000000000000000000005

        raise ValueError(f"Invalid rarity: {rarity}")

    @staticmethod
    def value_to_rarity(value: float) -> str:
        if value <= RaritySpinner.rarity_to_value("Bloodless"):
            return "Bloodless"
        elif value <= RaritySpinner.rarity_to_value("Pearlescent"):
            return "Pearlescent"
        elif value <= RaritySpinner.rarity_to_value("Legendary"):
            return "Legendary"
        elif value <= RaritySpinner.rarity_to_value("Ultra Rare"):
            return "Ultra Rare"
        elif value <= RaritySpinner.rarity_to_value("Rare"):
            return "Rare"
        elif value <= RaritySpinner.rarity_to_value("Uncommon"):
            return "Uncommon"
        else:
            return "Common"

    @staticmethod
    def default_value_for(tag: ObjectTag) -> str:
        match tag:
            case ObjectTag.Shared_Chance_Common:
                return "Common"
            case ObjectTag.Shared_Chance_Legendary:
                return "Legendary"
            case ObjectTag.Shared_Chance_Pearlescent:
                return "Pearlescent"
            case ObjectTag.Shared_Chance_Lootable:
                return "Uncommon"
            case _:
                raise ValueError(f"Invalid tag: {tag}")

    @staticmethod
    def on_change(self: "RaritySlider", value: str):
        if obj := self.tag.value():
            rarity = RaritySpinner.rarity_to_value(value)
            obj.ValueResolverChain[0].ConstantValue = rarity
        else:
            logging.error(f"Failed to find object '{self.tag}'")

    def __init__(self, identifier: str, tag: ObjectTag):
        self.tag = tag

        if obj := self.tag.value():
            val = RaritySpinner.value_to_rarity(obj.ValueResolverChain[0].ConstantValue)
        else:
            val = RaritySpinner.default_value_for(tag)

        super().__init__(
            identifier,
            value=val,
            choices=[
                "Common",
                "Uncommon",
                "Rare",
                "Ultra Rare",
                "Legendary",
                "Pearlescent",
                "Bloodless"
            ],
            on_change=RaritySpinner.on_change
        )


class RaritySlider(SliderOption):
    tag: ObjectTag

    def __init__(self, identifier: str, tag: ObjectTag, **kwargs):

        if "is_integer" not in kwargs:
            kwargs["is_integer"] = False

        self.tag = tag
        super().__init__(identifier=identifier, **kwargs, on_change=RaritySlider.on_change)

        if obj := self.tag.value():
            self.value = obj.ValueResolverChain[0].ConstantValue

    @staticmethod
    def on_change(self: "RaritySlider", value: float):
        if obj := self.tag.value():
            self.value = round(value, 2)
            obj.ValueResolverChain[0].ConstantValue = self.value
        else:
            logging.error(f"Failed to find object '{self.tag}'")
            return


# @formatter:off

OPTION_MAPPING: Dict[ObjectTag, BaseOption] = {
    ObjectTag.BetterHealth:    ToggleOption("Better Health", ObjectTag.BetterHealth),
    ObjectTag.PearlescentSDUs: ToggleOption("Pearlescent SDUs", ObjectTag.PearlescentSDUs),
    ObjectTag.Arsenal:         ToggleOption("Arsenal", ObjectTag.Arsenal),
    ObjectTag.EWO:             ToggleOption("Eridian Weapon Overhaul", ObjectTag.EWO),
    ObjectTag.VHC:             VHCSpinner("VHC", ObjectTag.VHC, ObjectTag.VHC_Expanded),

    ObjectTag.VHC_Randomizer: ToggleOption("Randomizer", ObjectTag.VHC_Randomizer),
    ObjectTag.VHC_Gearbox:    ToggleOption("Gearbox", ObjectTag.VHC_Gearbox),

    ObjectTag.VHC_Atlas:    VHCSpinner("Atlas", ObjectTag.VHC_Atlas, ObjectTag.VHC_Atlas_Expanded),
    ObjectTag.VHC_Dahl:     VHCSpinner("Dahl", ObjectTag.VHC_Dahl, ObjectTag.VHC_Dahl_Expanded),
    ObjectTag.VHC_Hyperion: VHCSpinner("Hyperion", ObjectTag.VHC_Hyperion, ObjectTag.VHC_Hyperion_Expanded),
    ObjectTag.VHC_Jakobs:   VHCSpinner("Jakobs", ObjectTag.VHC_Jakobs, ObjectTag.VHC_Jakobs_Expanded),
    ObjectTag.VHC_Maliwan:  VHCSpinner("Maliwan", ObjectTag.VHC_Maliwan, ObjectTag.VHC_Maliwan_Expanded),
    ObjectTag.VHC_SandS:    VHCSpinner("SandS", ObjectTag.VHC_SandS, ObjectTag.VHC_SandS_Expanded),
    ObjectTag.VHC_Tediore:  VHCSpinner("Tediore", ObjectTag.VHC_Tediore, ObjectTag.VHC_Tediore_Expanded),
    ObjectTag.VHC_Torgue:   VHCSpinner("Torgue", ObjectTag.VHC_Torgue, ObjectTag.VHC_Torgue_Expanded),
    ObjectTag.VHC_Vladof:   VHCSpinner("Vladof", ObjectTag.VHC_Vladof, ObjectTag.VHC_Vladof_Expanded),

    ObjectTag.EWO_DropChance: RaritySlider(
        "EWO Drop Chance",
        ObjectTag.EWO_DropChance,
        value=12,
        min_value=0,
        max_value=100,
        step=1
    ),

    ObjectTag.Shared_Chance_Common:      RaritySpinner("Common",      ObjectTag.Shared_Chance_Common),
    ObjectTag.Shared_Chance_Legendary:   RaritySpinner("Legendary",   ObjectTag.Shared_Chance_Legendary),
    ObjectTag.Shared_Chance_Pearlescent: RaritySpinner("Pearlescent", ObjectTag.Shared_Chance_Pearlescent),
    ObjectTag.Shared_Chance_Lootable:    RaritySpinner("Lootables",   ObjectTag.Shared_Chance_Lootable),

    ObjectTag.Shared_Chance_Common_A: RaritySlider(
        "Common",
        ObjectTag.Shared_Chance_Common,
        value=100,
        min_value=0,
        max_value=100,
        step=1
    ),
    ObjectTag.Shared_Chance_Legendary_A: RaritySlider(
        "Legendary",
        ObjectTag.Shared_Chance_Legendary,
        value=2,
        min_value=0,
        max_value=100,
        step=0.1
    ),
    ObjectTag.Shared_Chance_Pearlescent_A: RaritySlider(
        "Pearlescent",
        ObjectTag.Shared_Chance_Pearlescent,
        value=0.1,
        min_value=0,
        max_value=100,
        step=0.05
    ),
    ObjectTag.Shared_Chance_Lootable_A: RaritySlider(
        "Lootables",
        ObjectTag.Shared_Chance_Lootable,
        value=12,
        min_value=0,
        max_value=100,
        step=1
    ),
}

# @formatter:on
