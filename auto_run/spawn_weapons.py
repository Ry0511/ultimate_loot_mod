import math

from random import uniform
from typing import *

from unrealsdk import logging, find_class, find_object, load_package, make_struct
from unrealsdk.unreal import *
from mods_base import get_pc

LOOT_POOL_TYPE = "ItemPoolDefinition"
LOOT_POOL_PATH = "UltimateLoot_Pools_TEST.ChestPools.RedChest.RedChest_Weapons_All"

pool: UObject | None = None
item_pool_class = find_class("WillowGame.ItemPool")

try:
    pool = find_object(LOOT_POOL_TYPE, LOOT_POOL_PATH)
except ValueError as ex:
    pkg = load_package("UltimateLoot_Pools_TEST")
    if pkg is None:
        logging.misc("loaded package is None")
    else:
        pool = find_object(LOOT_POOL_TYPE, LOOT_POOL_PATH)


class Vec:
    pos_x: float
    pos_y: float
    pos_z: float

    def __init__(self, inner: Tuple[float, float, float] | None):
        self.pos_x, self.pos_y, self.pos_z = inner or (0.0, 0.0, 0.0)

    def add(self, other: "Vec"):
        return Vec((self.pos_x + other.pos_x, self.pos_y + other.pos_y, self.pos_z + other.pos_z))

    def sub(self, other: "Vec") -> "Vec":
        return Vec((self.pos_x - other.pos_x, self.pos_y - other.pos_y, self.pos_z - other.pos_z))

    def magnitude(self):
        return math.sqrt(self.pos_x ** 2 + self.pos_y ** 2 + self.pos_z ** 2)

    def mul(self, scalar: float):
        return Vec((self.pos_x * scalar, self.pos_y * scalar, self.pos_z * scalar))

    def normalise(self):
        mag = self.magnitude()
        if mag == 0:
            return Vec(None)
        return Vec((self.pos_x / mag, self.pos_y / mag, self.pos_z / mag))

    def to_wrapped_struct(self) -> WrappedStruct:
        return make_struct("Vector", X=self.pos_x, Y=self.pos_y, Z=self.pos_z)


pc = get_pc()
player_pos = pc.Pawn.Location

vec_player_pos = Vec((player_pos.X, player_pos.Y, player_pos.Z))
vec_drop_pos = Vec((player_pos.X + 200.0, player_pos.Y, player_pos.Z + 1250.0))
vel = vec_player_pos.sub(vec_drop_pos).normalise().mul(500.0)


def spherical_pos(centre: Vec, radius: float) -> Vec:
    while True:
        pos = Vec((uniform(-radius, radius), uniform(-radius, radius), uniform(-radius, radius)))
        if pos.magnitude() <= radius ** 2:
            return pos.add(centre)


if pool is not None and item_pool_class is not None:
    pool.ObjectFlags |= 0x4000
    cdo = item_pool_class.ClassDefaultObject

    pool.Quantity.BaseValueConstant = 30
    pool.Quantity.BaseValueScaleConstant = 1
    pool.Quantity.BaseValueAttribute = None
    pool.Quantity.InitializationDefinition = None
    res, items = cdo.SpawnBalancedInventoryFromPool(pool, 69, 200, pc, [])

    if not res:
        logging.error("Failed to spawn items")
    else:

        logging.info(f"Spawned {len(items)} items")
        for item in items:
            vec_pos = spherical_pos(vec_drop_pos, 1000.0)
            dir_pos = vec_pos if uniform(0, 1) < 0.5 else vec_pos.mul(-1)
            vec_dir = vec_player_pos.sub(dir_pos).normalise().mul(300.0)
            item.DropFrom(vec_pos.to_wrapped_struct(), vec_dir.to_wrapped_struct(), False)
