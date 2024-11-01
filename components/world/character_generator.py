import time
import random
import pygame

from components.character.character_class import Human, Demon
from components.character.character import Character
from components.character.character_info import CharacterInfo
from components.character.character_stat import CharacterStat, StatDefinition
from components.character.character_level import CharacterLevel
from components.common.point import Point
from components.world.store import get_store, EntityType
from data.logs.logger import logger


class CharacterGenerator:
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        self.name = "Character"
        self.interval = interval
        self.amount = amount
        self.location = location
        self.timestamp = time.time()

    def spawn(self):
        pass

    def update(self):
        if self.timestamp + self.interval < time.time():
            logger.debug(f"Spawn one {self.name} at {self.location}")
            self.timestamp = time.time()
            self.spawn()


class HumanGenerator(CharacterGenerator):
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        super().__init__(interval, amount, location)
        self.name = "Human"

    def spawn(self):
        stat = CharacterStat()
        stat.add_stat(StatDefinition.MAX_HEALTH, random.randint(50, 150))
        stat.add_stat(
            StatDefinition.CURRENT_HEALTH,
            stat.get_stat(StatDefinition.MAX_HEALTH).value,
        )
        stat.add_stat(StatDefinition.POWER, random.randint(10, 20))
        stat.add_stat(StatDefinition.SPEED, random.randint(80, 120))
        new_human = Character(
            self.location,
            pygame.image.load("data/sprites/character3.png"),
            CharacterInfo("Human"),
            stat,
            Human(),
            1,
        )
        get_store().add(EntityType.CHARACTER, new_human.get_info().id, new_human)


class DemonGenerator(CharacterGenerator):
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        super().__init__(interval, amount, location)
        self.name = "Demon"

    def spawn(self):
        stat = CharacterStat()
        stat.add_stat(StatDefinition.MAX_HEALTH, random.randint(150, 250))
        stat.add_stat(
            StatDefinition.CURRENT_HEALTH,
            stat.get_stat(StatDefinition.MAX_HEALTH).value,
        )
        stat.add_stat(StatDefinition.POWER, random.randint(15, 25))
        stat.add_stat(StatDefinition.SPEED, random.randint(30, 60))
        new_demon = Character(
            self.location,
            pygame.image.load("data/sprites/character5.png"),
            CharacterInfo("Demon"),
            stat,
            Demon(),
            1,
        )
        get_store().add(EntityType.CHARACTER, new_demon.get_info().id, new_demon)
