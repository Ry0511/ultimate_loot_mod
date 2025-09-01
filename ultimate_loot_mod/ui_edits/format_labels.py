from functools import wraps
from typing import runtime_checkable, Protocol

from unrealsdk import logging
import willow1_mod_menu as wmm
from willow1_mod_menu.populators import Populator

from mods_base import SliderOption

_original_format_slider_label = Populator.format_slider_label


@runtime_checkable
class SupportsFormatLabel(Protocol):
    def create_format_label(self) -> str: ...


@wraps(Populator.format_slider_label)
def _format_slider_label(option: SliderOption) -> str:
    if isinstance(option, SupportsFormatLabel):
        try:
            return option.create_format_label()
        except Exception as ex:  # noqa
            logging.error(f'Failed to create format label for option {option}, error: {ex}')
    return _original_format_slider_label(option)


wmm.populators.Populator.format_slider_label = staticmethod(_format_slider_label)
