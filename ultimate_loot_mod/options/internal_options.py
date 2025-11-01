from unrealsdk import logging
from typing import Tuple
from mods_base.options import BoolOption, SpinnerOption, SliderOption

from ..mapping.object_proxy import Tag, TagProxy

################################################################################
# | EXPORTS |
################################################################################

__all__ = [
    "TagToggleOption",
    "VHCSpinner",
    "RaritySlider",
]


################################################################################
# | TAG TOGGLE OPTION |
################################################################################

# noinspection PyArgumentList
class TagToggleOption(BoolOption):
    proxy: TagProxy

    def __init__(self, identifier: str, tag: Tag, **kwargs):
        self.proxy = TagProxy(tag)

        if "value" not in kwargs:
            kwargs["value"] = bool(self.proxy.default_value())

        if "on_change" not in kwargs:
            kwargs["on_change"] = self._on_change

        super().__init__(identifier, **kwargs)

    @staticmethod
    def _on_change(self: "TagToggleOption", val: bool) -> None:
        self.proxy.set_value(val)

    def sync_with_proxy(self) -> None:
        object.__setattr__(self, "value", bool(self.proxy.value()))

    def sync_proxy(self) -> None:
        if not self.proxy.set_value(self.value):
            logging.dev_warning(f"Failed to update tag: '{self.proxy.tag.name}'")


################################################################################
# | VHC SPINNER |
################################################################################

# noinspection PyArgumentList
class VHCSpinner(SpinnerOption):
    _normal_tag: TagProxy
    _expanded_tag: TagProxy | None

    NORMAL_CHOICE_LIST: list[str] = ["Off", "Normal"]
    EXPANDED_CHOICE_LIST: list[str] = ["Off", "Normal", "Expanded"]

    def __init__(self, identifier: str, normal: Tag, expanded: Tag | None = None, **kwargs):
        self._normal_tag = TagProxy(normal)
        self._expanded_tag = TagProxy(expanded) if expanded is not None else None

        if "choices" not in kwargs:
            kwargs["choices"] = VHCSpinner.NORMAL_CHOICE_LIST if not expanded else VHCSpinner.EXPANDED_CHOICE_LIST

        if "on_change" not in kwargs:
            kwargs["on_change"] = self._on_change

        if "value" not in kwargs:
            kwargs["value"] = self.get_str_value_from_proxy(use_proxy_value=False)

        super().__init__(identifier=identifier, **kwargs)

    def set_normal(self, val: bool) -> None:
        if not self._normal_tag.set_value(val):
            logging.dev_warning(f"Failed to update tag: '{self._normal_tag.tag.name}'")

    def set_expanded(self, val: bool) -> None:
        if self._expanded_tag and not self._expanded_tag.set_value(val):
            logging.dev_warning(f"Failed to update tag: '{self._expanded_tag.tag.name}'")

    def get_value_state(self, value: str | None = None) -> Tuple[bool, bool]:
        if value is None:
            value = self.value

        if value == 'Expanded':
            return True, True
        elif value == 'Normal':
            return True, False
        elif value == 'Off':
            return False, False
        else:
            raise ValueError(f"Invalid value: {value}")

    @staticmethod
    def _on_change(self: "VHCSpinner", val: str) -> None:
        normal, expanded = self.get_value_state(val)
        self.set_normal(normal)
        self.set_expanded(expanded)

    def get_str_value_from_proxy(self, use_proxy_value=True) -> str:

        if use_proxy_value:
            is_normal: bool = bool(self._normal_tag.value())
            is_expanded: bool = self._expanded_tag and bool(self._expanded_tag.value())
        else:
            is_normal: bool = bool(self._normal_tag.default_value())
            is_expanded: bool = self._expanded_tag and bool(self._expanded_tag.default_value())

        if is_expanded:
            return "Expanded"
        elif is_normal:
            return "Normal"
        else:
            return "Off"

    def sync_with_proxy(self) -> None:
        object.__setattr__(self, "value", self.get_str_value_from_proxy())

    def sync_proxy(self) -> None:
        normal, expanded = self.get_value_state()
        self.set_normal(normal)
        self.set_expanded(expanded)


################################################################################
# | RARITY SLIDER |
################################################################################

# noinspection PyArgumentList
class RaritySlider(SliderOption):
    tag: TagProxy
    is_scalar: bool
    value_suffix: str = ""

    def __init__(self, identifier: str, tag: Tag, is_scalar=False, value_suffix="", **kwargs):
        self.tag = TagProxy(tag)
        self.is_scalar = is_scalar
        self.value_suffix = value_suffix

        if "min_value" not in kwargs:
            kwargs["min_value"] = 0.0

        if "max_value" not in kwargs:
            kwargs["max_value"] = 100.0 if not is_scalar else 10.0

        if "step" not in kwargs:
            kwargs["step"] = 1.0 if not is_scalar else 0.05

        if "is_integer" not in kwargs:
            kwargs["is_integer"] = False

        if "value" not in kwargs:
            val = float(self.tag.default_value())

            # Default values is 150% not 1.5x
            if is_scalar:
                val /= 100.0

            kwargs["value"] = val

        if "on_change" not in kwargs:
            kwargs["on_change"] = self._on_change

        super().__init__(identifier, **kwargs)

    @staticmethod
    def _on_change(self: "RaritySlider", val: float) -> None:
        if self.is_scalar:
            self.tag.set_value(val * 100.0)
        else:
            self.tag.set_value(val)

    def create_format_label(self) -> str:
        value_text = f"{self.value:d}" if self.is_integer else f"{self.value:.2f}"
        return f'{self.identifier}: {value_text}{self.value_suffix}'

    def sync_with_proxy(self) -> None:
        val = self.tag.value()
        object.__setattr__(self, "value", val if not self.is_scalar else val / 100.0)

    def sync_proxy(self) -> None:
        if self.is_scalar:
            if not self.tag.set_value(self.value * 100.0):
                logging.dev_warning(f"Failed to update tag: '{self.tag.tag.name}'")
        else:
            if not self.tag.set_value(self.value):
                logging.dev_warning(f"Failed to update tag: '{self.tag.tag.name}'")