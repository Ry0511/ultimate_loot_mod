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
    _tag: TagProxy

    def __init__(self, identifier: str, tag: Tag, **kwargs):
        self._tag = TagProxy(tag)

        if "value" not in kwargs:
            kwargs["value"] = bool(self._tag.value(allow_default=True))

        if "on_change" not in kwargs:
            kwargs["on_change"] = self._on_change

        super().__init__(identifier, **kwargs)

    @staticmethod
    def _on_change(self: "TagToggleOption", val: bool) -> None:
        self._tag.set_value(val)

    def fetch_proxy_value(self) -> None:
        setattr(self, "_on_change_recursion_guard", None)
        self.value = bool(self._tag.value(allow_default=True))
        delattr(self, "_on_change_recursion_guard")


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
            kwargs["value"] = self.get_str_value_from_proxy()

        super().__init__(identifier=identifier, **kwargs)

    def set_normal(self, val: bool) -> None:
        self._normal_tag.set_value(val)

    def set_expanded(self, val: bool) -> None:
        if self._expanded_tag:
            self._expanded_tag.set_value(val)

    @staticmethod
    def _on_change(self: "VHCSpinner", val: str) -> None:

        if val == "Off":
            self.set_normal(False)
            self.set_expanded(False)

        elif val == "Normal":
            self.set_normal(True)
            self.set_expanded(False)
            TagProxy(Tag.VHC_Enabler).set_value(True)

        elif val == "Expanded":
            self.set_normal(True)
            self.set_expanded(True)
            TagProxy(Tag.VHC_Enabler).set_value(True)
            TagProxy(Tag.VHC_Expanded_Enabler).set_value(True)

    def get_str_value_from_proxy(self) -> str:
        if self._expanded_tag and bool(self._expanded_tag.value(allow_default=True)):
            return "Expanded"
        elif bool(self._normal_tag.value(allow_default=True)):
            return "Normal"
        else:
            return "Off"

    def fetch_proxy_value(self) -> None:
        setattr(self, "_on_change_recursion_guard", None)
        self.value = self.get_str_value_from_proxy()
        delattr(self, "_on_change_recursion_guard")


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
            val = float(self.tag.value(allow_default=True))

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

    def fetch_proxy_value(self) -> None:
        setattr(self, "_on_change_recursion_guard", None)
        if val := self.tag.value():
            self.value = val if not self.is_scalar else val / 100.0
        delattr(self, "_on_change_recursion_guard")

    def create_format_label(self) -> str:
        if self.is_integer:
            value_text = f"{self.value:d}{self.value_suffix}"
        else:
            value_text = f"{self.value:.2f}{self.value_suffix}"

        return f'{self.identifier}: {value_text}'
