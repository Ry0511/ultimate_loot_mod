from typing import Tuple

import ultimate_loot_mod.ui_edits  # noqa

from unrealsdk import logging
from mods_base import build_mod

from .mapping.object_proxy import Tag, load_all_objects, TagProxy
from .options.option_list import create_option_list
from .ui_edits import auto_tag_all_options

from .ultimate_loot_mod import UltimateLootMod, the_mod

__version__: Tuple[int, int]


def _on_enable() -> None:
    load_all_objects()


def _on_disable() -> None:
    for tag in Tag:
        TagProxy(tag).unload_object()


# TODO: Need to change how options are loaded and applied because this approach can cause crashes.
#  Unfortunately there isn't a nice way to do this since we're integrating with quite a few systems
#  that we don't have control over.
load_all_objects()

build_mod(
    cls=UltimateLootMod,
    options=create_option_list(),
    on_enable=_on_enable,
    on_disable=_on_disable,
)

auto_tag_all_options(the_mod(), the_mod().options)

# Right after build_mod it will load the settings file and then those values would've been applied
# to the proxies grab those values and store them separately to enable restoring them.
for tag in Tag:
    proxy = TagProxy(tag)
    proxy.set_first_load_value(proxy.value(allow_default=True))

logging.info(f"Successfully loaded {the_mod().name} v{the_mod().version}")
