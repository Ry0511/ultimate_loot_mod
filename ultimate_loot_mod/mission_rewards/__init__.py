from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from mods_base import get_pc, hook
from unrealsdk import logging
from unrealsdk.hooks import Block, Type, prevent_hooking_direct_calls
from unrealsdk.unreal import BoundFunction, UObject

from .mission_override import MissionRewardOverride, load_mission_reward_overrides

if TYPE_CHECKING:
    from BL1.WillowGame import MissionDefinition, WillowPlayerReplicationInfo

_reward_overrides: dict[str, MissionRewardOverride] | None = None
_granting_rewards: bool = False


@hook("Engine.GameInfo:PreCommitMapChange")
def hook_init_on_first_load(*_: Any) -> None:
    global _reward_overrides
    hook_init_on_first_load.disable()

    mission_overrides = load_mission_reward_overrides()
    _reward_overrides = {m.override_path: m for m in mission_overrides}

    for reward in _reward_overrides.values():
        if reward.reward_uobject() is None:
            logging.error(f'Failed to load reward "{reward.reward_path}"')


hook_init_on_first_load.enable()


@hook("WillowGame.MissionTracker:GrantMissionRewards", immediately_enable=True)
def hook_grant_rewards_pre(*_: Any) -> None:
    global _granting_rewards
    _granting_rewards = True


@hook(
    "WillowGame.MissionTracker:GrantMissionRewards",
    hook_type=Type.POST_UNCONDITIONAL,
    immediately_enable=True,
)
def hook_grant_rewards_post(*_: Any) -> None:
    global _granting_rewards
    _granting_rewards = False


@hook("WillowGame.MissionDefinition:GetGameStage", immediately_enable=True)
def hook_reward_game_stage(*_: Any) -> tuple[type[Block], int] | None:
    if not _granting_rewards:
        return None
    return Block, cast("WillowPlayerReplicationInfo", get_pc().PlayerReplicationInfo).ExpLevel


@hook(  # pyright: ignore[reportArgumentType]
    "WillowGame.MissionDefinition:GetItemRewardForPlayer", immediately_enable=True
)
def hook_override_item_reward(
    obj: MissionDefinition,
    args: MissionDefinition.GetItemRewardForPlayerArgs,
    _3: Any,
    _4: BoundFunction,
) -> tuple[type[Block], UObject | None] | None:
    if not _granting_rewards or _reward_overrides is None:
        return None

    mission_path: str = obj._path_name().lower()
    wpc = args.InWPC

    # Calls to GetItemRewardForPlayer below must not re-enter this hook
    with prevent_hooking_direct_calls():
        mission_override = _reward_overrides.get(mission_path)

        if mission_override is not None:
            logging.info(f'Overriding mission reward for "{mission_path}"')
            return Block, mission_override.get_reward(wpc)

        normal_reward = obj.GetItemRewardForPlayer(wpc)

        if normal_reward is None:
            logging.info(f'Mission has no reward "{mission_path}"')
            return Block, None

        normal_reward_path = normal_reward._path_name().lower()

        if (override := _reward_overrides.get(normal_reward_path)) is not None:
            logging.info(f'Overriding mission reward "{normal_reward_path}"')
            return Block, override.get_reward(wpc)
        else:
            return Block, normal_reward
