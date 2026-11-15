from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from mods_base import get_pc, hook
from unrealsdk import find_enum
from unrealsdk.hooks import Block, Type

from ..ultimate_loot_mod import UltimateLootMod
from ..utils import dynamic_load_object

if TYPE_CHECKING:
    from BL1.Engine import WorldInfo
    from BL1.WillowGame import (
        Behavior_GFxMoviePlay,
        EMissionStatus,
        EShopType,
        ItemPoolDefinition,
        MissionDefinition,
        PopulationFactoryVendingMachine,
        VendingMachineGFxDefinition,
        WillowGameInfo,
        WillowInteractiveObject,
        WillowPlayerReplicationInfo,
        WillowSeqEvent_MissionObjectiveComplete,
        WillowVendingMachine,
    )
    from mods_base import HookType
    from unrealsdk.unreal import BoundFunction

    ObjectiveComplete = WillowSeqEvent_MissionObjectiveComplete
    VendingFactory = PopulationFactoryVendingMachine
else:
    EMissionStatus = find_enum("EMissionStatus")
    EShopType = find_enum("EShopType")

__all__ = ["hooks"]


def _fix_mission_done(world: WorldInfo) -> bool:
    game = cast("WillowGameInfo | None", world.Game)
    if game is None:
        return False
    mission = cast(
        "MissionDefinition",
        dynamic_load_object(
            "MissionDefinition", "dlc1_missions.SideMissions.M_dlc1_FixJakobsVending"
        ),
    )
    return game.MissionTracker.GetMissionStatus(mission) >= EMissionStatus.MS_ReadyToTurnIn


@hook(  # pyright: ignore[reportArgumentType]
    "WillowGame.WillowSeqEvent_MissionObjectiveComplete:ProcessMissionReaction"
)
def block_complete_reaction(
    _1: ObjectiveComplete,
    args: ObjectiveComplete.ProcessMissionReactionArgs,
    _3: Any,
    _4: BoundFunction,
) -> type[Block] | None:
    if args.MissionDefinition.Name == "M_dlc1_FixJakobsVending":
        return Block
    return None


@hook(  # pyright: ignore[reportArgumentType]
    "WillowGame.WillowSeqEvent_MissionObjectiveComplete:ProcessMissionObjectiveReaction"
)
def block_stale_objective_reaction(
    obj: ObjectiveComplete,
    args: ObjectiveComplete.ProcessMissionObjectiveReactionArgs,
    _3: Any,
    _4: BoundFunction,
) -> type[Block] | None:
    mission_name = "m_dlc1_fixjakobsvending"
    if args.MissionDefinition.Name.lower() == mission_name and _fix_mission_done(
        obj.GetWorldInfo()
    ):
        return Block
    return None


@hook(  # pyright: ignore[reportArgumentType]
    "WillowGame.WillowInteractiveObject:Behavior_ChangeBehaviorSet"
)
def keep_vendor_on(
    obj: WillowInteractiveObject,
    args: WillowInteractiveObject.Behavior_ChangeBehaviorSetArgs,
    _3: Any,
    _4: BoundFunction,
) -> type[Block] | None:
    if (
        obj.InteractiveObjectDefinition.Name == "dlc1_InteractiveObj_VendingMachine_Jakobs"
        and str(args.BehaviorSetName) in ("NoFuse", "ReadyForFuse")
        and _fix_mission_done(obj.WorldInfo)
    ):
        return Block
    return None


@hook(  # pyright: ignore[reportArgumentType]
    "WillowGame.PopulationFactoryVendingMachine:CreateInteractiveObject"
)
def setup_jakobs_vendor(
    obj: VendingFactory,
    args: VendingFactory.CreateInteractiveObjectArgs,
    _3: Any,
    _4: BoundFunction,
) -> None:
    balance = obj.ObjectBalanceDefinition
    if balance.Name != "dlc1_ObjectGrade_VendingMachine_Jakobs":
        return

    obj.ShopType = EShopType.SType_Items

    movie = cast(
        "VendingMachineGFxDefinition",
        dynamic_load_object(
            "VendingMachineGFxDefinition",
            "menus_vending_MOD.Definitions.VendingMachineDefinition2",
        ),
    )
    for behavior_set in args.SelectedObjectDefinition.ExtraBehaviorSets:
        for behavior in behavior_set.OnUsedBy:
            if behavior.Class.Name == "Behavior_GFxMoviePlay":
                cast("Behavior_GFxMoviePlay", behavior).MovieDefinition = movie

    pools = {
        "Inventory": "UltimateLoot_Pools_TEST.LootablePools.ShopPool_Inventory_Jakobs",
        "FeaturedItem": "UltimateLoot_Pools_TEST.LootablePools.shoppool_FeaturedItem_Jakobs",
    }
    for loot in balance.DefaultLoot:
        pool = cast(
            "ItemPoolDefinition",
            dynamic_load_object("ItemPoolDefinition", pools[str(loot.ConfigurationName)]),
        )
        if str(loot.ConfigurationName) == "Inventory":
            pool.Quantity.BaseValueConstant = 12
        for attachment in loot.ItemAttachments:
            attachment.ItemPool = pool


@hook(  # pyright: ignore[reportArgumentType]
    "WillowGame.PopulationFactoryVendingMachine:CreateInteractiveObject",
    Type.POST,
)
def set_jakobs_vendor_level(
    obj: VendingFactory,
    _2: VendingFactory.CreateInteractiveObjectArgs,
    ret: WillowVendingMachine,
    _4: BoundFunction,
) -> None:
    if obj.ObjectBalanceDefinition.Name != "dlc1_ObjectGrade_VendingMachine_Jakobs":
        return
    # always on level
    ret.SetGameStage(cast("WillowPlayerReplicationInfo", get_pc().PlayerReplicationInfo).ExpLevel)


hooks = cast(
    "tuple[HookType[Any], ...]",
    (
        setup_jakobs_vendor,
        set_jakobs_vendor_level,
        keep_vendor_on,
        block_stale_objective_reaction,
        block_complete_reaction,
    ),
)

UltimateLootMod.components.append(
    UltimateLootMod.ComponentInfo(
        "Jakobs Vendor Fix", "1.5", "ugyuu, sleepmaster, BioHazardAlbatross"
    )
)
