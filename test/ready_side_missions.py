from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from mods_base import get_pc, hook
from unrealsdk import find_enum, logging, make_struct
from unrealsdk.hooks import Type
from unrealsdk.unreal import BoundFunction

if TYPE_CHECKING:
    from BL1.WillowGame import (
        EMissionStatus,
        MissionObjectiveStatus,
        MissionStatus,
        WillowGameInfo,
        WillowPlayerController,
    )
else:
    EMissionStatus = find_enum("EMissionStatus")


def make_ready(pc: WillowPlayerController, status: MissionStatus) -> None:
    mission = status.MissionDef
    tracker = cast("WillowGameInfo", pc.WorldInfo.Game).MissionTracker
    if not tracker.MissionBeingTracked(mission):
        tracker.AddMission(mission)

    objectives = status.Objectives
    objectives.clear()
    for objective in mission.Objectives:
        objectives.append(
            cast(
                "MissionObjectiveStatus",
                make_struct(
                    "MissionObjectiveStatus",
                    StatId=objective.StatId,
                    CurrentAmount=objective.ObjectiveCount,
                ),
            )
        )

    status.Status = EMissionStatus.MS_ReadyToTurnIn


@hook(  # pyright: ignore[reportArgumentType]
    "WillowGame.WillowPlayerController:CompleteMission", Type.POST
)
def on_complete_mission(
    pc: WillowPlayerController,
    args: WillowPlayerController.CompleteMissionArgs,
    _3: Any,
    _4: BoundFunction,
) -> None:
    mission = args.InMission
    if mission.bPlotCritical:
        return

    index = pc.GetMissionIndexForMission(mission)
    make_ready(pc, pc.MissionPlaythroughData[pc.GetCurrentPlaythrough()].MissionList[index])
    logging.info(f"[ready_side_missions] {mission.Name} set back to ready to turn in")


player = cast("WillowPlayerController", get_pc())
count = 0
for mission_status in player.MissionPlaythroughData[player.GetCurrentPlaythrough()].MissionList:
    if not mission_status.MissionDef.bPlotCritical:
        make_ready(player, mission_status)
        count += 1

on_complete_mission.disable()
on_complete_mission.enable()

logging.info(f"[ready_side_missions] {count} side missions set to ready to turn in, hook enabled")
