from typing import Tuple

from unrealsdk import logging
from mods_base import Mod, register_mod

from .mapping.object_proxy import Tag, load_all_objects, TagProxy
from .options.option_list import create_option_list

import ultimate_loot_mod.ui_edits  # noqa
from .ui_edits import auto_tag_all_options

from .options.lazy_loading_sequence import LazyLoadedOptionSequence

__version__: Tuple[int, int]


def _on_enable() -> None:
    if load_all_objects():
        return

    failed_list = [tag.name for tag in Tag if not TagProxy(tag).object()]
    logging.warning(f'Failed to load: {", ".join(failed_list)} ultimate loot mod objects')


def _on_disable() -> None:
    for tag in Tag:
        TagProxy(tag).unload_object()


def _on_load_options():
    global the_mod
    load_all_objects()

    def set_mod(all_options) -> None:
        from mods_base import NestedOption, GroupedOption

        for option in all_options:
            option.mod = the_mod
            if isinstance(option, NestedOption | GroupedOption):
                set_mod(option.children)

    all_options = create_option_list()
    set_mod(all_options)
    auto_tag_all_options(the_mod, all_options)
    return all_options

# This is a fair bit more complex than it needs to be...
def create_mod() -> Mod:
    from tomllib import loads
    from pathlib import Path
    from mods_base import SETTINGS_DIR

    settings_file = SETTINGS_DIR / "ultimate_loot_mod.json"
    pyproject_file = Path(__file__).parent / "pyproject.toml"

    t = loads(pyproject_file.read_text(encoding='utf-8'))

    mod = Mod(name=t['tool']['sdkmod']['name'])

    from mods_base.mod_factory import (
        ModFactoryFields,
        deregister_using_settings_file,
        update_fields_with_pyproject_tool_sdkmod,
        update_fields_with_pyproject_project,
    )

    fields: ModFactoryFields = {
        "name": None,
        "author": None,
        "description": None,
        "version": None,
        "_version_info": None,
        "mod_type": None,
        "supported_games": None,
        "coop_support": None,
        "settings_file": SETTINGS_DIR / "ultimate_loot_mod.json",
        "keybinds": None,
        "options": None,
        "hooks": None,
        "commands": None,
        "auto_enable": True,
        "on_enable": None,
        "on_disable": None,
    }

    deregister_using_settings_file(settings_file)
    update_fields_with_pyproject_tool_sdkmod(t["tool"]["sdkmod"], fields)
    update_fields_with_pyproject_project(t["project"], fields)

    for field, value in fields.items():
        if value is None or field.startswith("_"):
            continue
        setattr(mod, field, value)

    return mod


the_mod: Mod = create_mod()

# Delayed assignment to ensure the_mod is accessible
the_mod.on_enable = _on_enable
the_mod.on_disable = _on_disable
the_mod.options = LazyLoadedOptionSequence(_on_load_options)
the_mod.__post_init__()

register_mod(the_mod)

logging.info(f"Successfully loaded {the_mod.name} v{the_mod.version}")
