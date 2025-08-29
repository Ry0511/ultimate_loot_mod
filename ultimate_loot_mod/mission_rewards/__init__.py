from typing import Tuple, Type, List, Dict, Iterable

from unrealsdk.hooks import Block, prevent_hooking_direct_calls, Type as HookType
from unrealsdk.unreal import UObject
from unrealsdk import logging
from mods_base import hook

from .mission_override import *

_reward_overrides: Dict[str, MissionRewardOverride] | None = None
_toggle_cheat_missions: bool = False


@hook('WillowGame.WillowPlayerController:SpawningProcessComplete')
def hook_init_on_first_load(*_) -> None:
    global _reward_overrides
    hook_init_on_first_load.disable()

    mission_overrides: List[MissionRewardOverride] = load_mission_reward_overrides()
    _reward_overrides = {m.override_path: m for m in mission_overrides}


hook_init_on_first_load.enable()


@hook('WillowGame.MissionDefinition:GetItemRewardForPlayer')
def hook_on_mission_complete(
    obj: UObject,
    args,
    *_
) -> Tuple[Type[Block], UObject | None] | None:
    global _reward_overrides
    hook_on_mission_complete.disable()

    # Shouldn't happen but we will check anyway
    if _reward_overrides is None or obj is None:
        logging.dev_warning(f'Illegal reward state')
        return None

    mission_path: str = obj._path_name().lower()

    # Not sure if this is required considering we just disabled ourself
    with prevent_hooking_direct_calls():
        mission_override: MissionRewardOverride | None = _reward_overrides.get(mission_path)

        if mission_override is not None:
            logging.info(f'Overriding mission reward for "{mission_path}"')
            return Block, mission_override.get_reward(args.InWPC)

        normal_reward = obj.GetItemRewardForPlayer(args.InWPC)

        if normal_reward is None:
            logging.info(f'Mission has no reward "{mission_path}"')
            return Block, None

        normal_reward_path = normal_reward._path_name().lower()

        if (override := _reward_overrides.get(normal_reward_path)) is not None:
            logging.info(f'Overriding mission reward "{normal_reward_path}"')
            return Block, override.get_reward(args.InWPC)
        else:
            return Block, normal_reward


@hook('WillowGame.QuestAcceptGFxMovie:extCompleteConfirmed', immediately_enable=True)
def hook_on_grant_mission_reward_pre(*_) -> None:
    hook_on_mission_complete.enable()


@hook('WillowGame.QuestAcceptGFxMovie:extCompleteConfirmed', hook_type=HookType.POST_UNCONDITIONAL, immediately_enable=True)
def hook_on_grant_mission_reward_post(*_) -> None:
    global _toggle_cheat_missions
    if _toggle_cheat_missions:
        _cheat_missions(None)  # noqa


hook_on_mission_complete.disable()
hook_on_grant_mission_reward_pre.enable()
hook_on_grant_mission_reward_post.enable()

################################################################################
# | REMOVE EVENTUALLY |
################################################################################


from mods_base import command, get_pc


@command('cheat_missions')
def _cheat_missions(*_) -> None:
    from dataclasses import dataclass
    from ultimate_loot_mod.utils import dynamic_load_object

    global _toggle_cheat_missions
    _toggle_cheat_missions = True

    wpc: UObject = get_pc()


    @dataclass
    class Proxy:
        MissionDef: UObject
        Status: int


    def all_missions() -> Iterable[UObject | Proxy]:
        play_index = wpc.GetCurrentPlaythrough()
        yield from wpc.MissionPlaythroughData[play_index].MissionList

        for dlc_mission in wpc.MissionPlaythroughData[play_index].UnloadableDlcMissionList:
            yield Proxy(
                MissionDef=dynamic_load_object('MissionDefinition', dlc_mission.MissionDefName),
                Status=-1
            )

    for m in all_missions():

        if m is None or m.MissionDef is None or m.Status == -1:
            continue

        if m.MissionDef.bPlotCritical:
            m.Status = 4  # Completed
        else:
            m.Status = 2  # Ready to turn in


_cheat_missions.enable()


@command('reload_rewards')
def _reload_reward_overrides(*_) -> None:
    global _reward_overrides
    mission_overrides: List[MissionRewardOverride] = load_mission_reward_overrides()
    _reward_overrides = {m.override_path: m for m in mission_overrides}


_reload_reward_overrides.enable()
