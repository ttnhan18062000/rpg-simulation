import time
import random
import pygame

from components.character.character_class import Human, Demon, RuinMob, ForestMob
from components.character.character import Character
from components.character.character_info import CharacterInfo
from components.character.character_stat import CharacterStat, StatDefinition
from components.character.character_level import CharacterLevel
from components.character.character_behavior import (
    FightingBehavior,
    AggressiveBehavior,
    PassiveBehavior,
)
from components.action.strategy.move_strategy import (
    ThinkingMove,
    AgressiveMobMove,
    PassiveMobMove,
)
from components.character.character_strategy import CharacterStrategyType
from components.common.point import Point
from components.world.store import get_store, EntityType
from data.logs.logger import logger


class CharacterGenerator:
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        self.name = "Character"
        self.interval = interval
        self.amount = amount
        self.spawn_counter = 0
        self.location = location
        self.timestamp = time.time()

    def spawn(self):
        pass

    def update(self):
        if self.timestamp + self.interval < time.time():
            logger.debug(f"Spawn one {self.name} at {self.location}")
            self.timestamp = time.time()
            self.spawn()
            self.spawn_counter += 1

    def is_stop(self):
        return self.amount == self.spawn_counter


class HumanGenerator(CharacterGenerator):
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        super().__init__(interval, amount, location)
        self.name = "Human"

    def spawn(self):
        stat = CharacterStat()
        stat.add_stat(StatDefinition.MAX_HEALTH, random.randint(100, 150))
        stat.add_stat(
            StatDefinition.CURRENT_HEALTH,
            stat.get_stat(StatDefinition.MAX_HEALTH).value,
        )
        stat.add_stat(StatDefinition.POWER, random.randint(15, 30))
        stat.add_stat(StatDefinition.SPEED, random.randint(80, 120))
        new_human = Character(
            self.location,
            pygame.image.load("data/sprites/character3.png"),
            CharacterInfo("Human"),
            stat,
            Human(),
            1,
        )
        new_human.set_vision_range(15)
        new_human.add_strategy(CharacterStrategyType.Move, ThinkingMove())
        new_human.add_behavior(
            FightingBehavior.name, FightingBehavior.create_random_behavior()
        )
        get_store().add(EntityType.CHARACTER, new_human.get_info().id, new_human)


class DemonGenerator(CharacterGenerator):
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        super().__init__(interval, amount, location)
        self.name = "Demon"

    def spawn(self):
        stat = CharacterStat()
        stat.add_stat(StatDefinition.MAX_HEALTH, random.randint(200, 300))
        stat.add_stat(
            StatDefinition.CURRENT_HEALTH,
            stat.get_stat(StatDefinition.MAX_HEALTH).value,
        )
        stat.add_stat(StatDefinition.POWER, random.randint(30, 50))
        stat.add_stat(StatDefinition.SPEED, random.randint(50, 70))
        new_demon = Character(
            self.location,
            pygame.image.load("data/sprites/demon2.png"),
            CharacterInfo("Demon"),
            stat,
            Demon(),
            1,
        )
        new_demon.set_vision_range(15)
        new_demon.add_strategy(CharacterStrategyType.Move, ThinkingMove())
        new_demon.add_behavior(
            FightingBehavior.name, FightingBehavior.create_random_behavior()
        )
        get_store().add(EntityType.CHARACTER, new_demon.get_info().id, new_demon)


class RuinMobGenerator(CharacterGenerator):
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        super().__init__(interval, amount, location)
        self.name = "RuinMob"

    def spawn(self):
        stat = CharacterStat()
        stat.add_stat(StatDefinition.MAX_HEALTH, random.randint(300, 600))
        stat.add_stat(
            StatDefinition.CURRENT_HEALTH,
            stat.get_stat(StatDefinition.MAX_HEALTH).value,
        )
        stat.add_stat(StatDefinition.POWER, random.randint(50, 80))
        stat.add_stat(StatDefinition.SPEED, random.randint(25, 50))
        new_mob = Character(
            self.location,
            pygame.image.load("data/sprites/ruinmob1.png"),
            CharacterInfo("RuinMob"),
            stat,
            RuinMob(),
            1,
        )
        new_mob.add_strategy(CharacterStrategyType.Move, AgressiveMobMove())
        new_mob.add_behavior(FightingBehavior.name, AggressiveBehavior())
        get_store().add(EntityType.CHARACTER, new_mob.get_info().id, new_mob)


class ForsetMobGenerator(CharacterGenerator):
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        super().__init__(interval, amount, location)
        self.name = "ForestMob"

    def spawn(self):
        stat = CharacterStat()
        stat.add_stat(StatDefinition.MAX_HEALTH, random.randint(75, 125))
        stat.add_stat(
            StatDefinition.CURRENT_HEALTH,
            stat.get_stat(StatDefinition.MAX_HEALTH).value,
        )
        stat.add_stat(StatDefinition.POWER, random.randint(10, 20))
        stat.add_stat(StatDefinition.SPEED, random.randint(50, 80))
        new_mob = Character(
            self.location,
            pygame.image.load("data/sprites/forestmob1.png"),
            CharacterInfo("ForestMob"),
            stat,
            ForestMob(),
            1,
        )
        new_mob.add_strategy(CharacterStrategyType.Move, PassiveMobMove())
        new_mob.add_behavior(FightingBehavior.name, PassiveBehavior())
        get_store().add(EntityType.CHARACTER, new_mob.get_info().id, new_mob)
