from components.common.point import Point
from components.common.game_object import GameObject
from components.character.character_info import CharacterInfo
from components.character.character_action import CharacterAction
from components.character.character_stat import CharacterStat, StatDefinition
from components.character.character_class import CharacterClass
from components.character.character_level import CharacterLevel
from components.world.store import get_store, EntityType

from data.logs.logger import logger


class Character(GameObject):
    def __init__(
        self,
        pos: Point,
        img: str,
        character_info: CharacterInfo,
        character_stats: CharacterStat,
        character_class: CharacterClass,
        level: int,
    ):
        super().__init__(pos, img)
        self.pos = pos
        self.img = img
        self.character_info = character_info
        self.character_action = CharacterAction()
        self.character_stats = character_stats
        self.character_class = character_class
        self.level = CharacterLevel(character_class.class_level, level)
        self.is_dead = False

        store = get_store()
        self.tile_id = store.get(EntityType.GRID, 0).tiles[pos.x][pos.y]
        tile = store.get(EntityType.TILE, self.tile_id)
        tile.add_character_id(character_info.id)

    def get_info(self):
        return self.character_info

    def get_stats(self):
        return self.character_stats

    def get_character_class(self):
        return self.character_class.__class__.__name__

    def is_alive(self):
        return (
            self.character_stats.get_stat(StatDefinition.HEALTH).value > 0
            and not self.is_dead
        )

    def set_status(self, status):
        if status == "dead":
            self.is_dead = True

    def is_hostile_with(self, character: "Character"):
        return (
            self.character_class.__class__.__name__
            != character.character_class.__class__.__name__
        )

    def level_up(self):
        for stat_def, value in self.character_class.stats_gain.items():
            self.character_stats.update_stat(stat_def, value)
        logger.debug(f"f{self.get_info()} has leveled up: {self.character_stats}")

    def do_action(self):
        next_action = self.character_action.get_next_action()
        next_action.execute(self)
