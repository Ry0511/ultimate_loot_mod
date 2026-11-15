from __future__ import annotations

from typing import TYPE_CHECKING, cast

from mods_base import ENGINE, get_pc
from unrealsdk import find_class, find_enum, make_struct

if TYPE_CHECKING:
    from BL1.WillowGame import (
        EMissionStatus,
        MissionDefinition,
        MissionObjectiveStatus,
        MissionStatus,
        WillowGameInfo,
        WillowPlayerController,
        WillowPlayerReplicationInfo,
    )
else:
    EMissionStatus = find_enum("EMissionStatus")

pc = cast("WillowPlayerController", get_pc())
tracker = cast("WillowGameInfo", pc.WorldInfo.Game).MissionTracker
mission = cast(
    "MissionDefinition",
    ENGINE.DynamicLoadObject(
        "dlc1_Missions.SideMissions.M_dlc1_FixJakobsVending",
        find_class("MissionDefinition"),
        False,
    ),
)

if not tracker.MissionBeingTracked(mission):
    tracker.AddMission(mission)

missions = pc.MissionPlaythroughData[pc.GetCurrentPlaythrough()].MissionList
index = pc.GetMissionIndexForMission(mission)
if index == -1:
    missions.append(cast("MissionStatus", make_struct("MissionStatus", MissionDef=mission)))
    index = len(missions) - 1

objectives = missions[index].Objectives
objectives.clear()
for objective in mission.Objectives:
    objectives.append(
        cast(
            "MissionObjectiveStatus",
            make_struct(
                "MissionObjectiveStatus",
                StatId=objective.StatId,
                CurrentAmount=0,
            ),
        )
    )
pc.SetMissionStatus(index, EMissionStatus.MS_Active)
tracker.UpdateObjective(mission, 0)

cast("WillowPlayerReplicationInfo", pc.PlayerReplicationInfo).SetCurrencyOnHand(100_000_000)
