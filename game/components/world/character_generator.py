import time
import random
import pygame

from components.race.race import Human, Demon, Ruin, Forest
from components.archetype.archetype import Mob, Player
from components.archetype.swordman_lineage import SwordTrainee
from components.character.character import Character
from components.character.character_info import CharacterInfo
from components.character.character_stat import CharacterStat, StatDefinition
from components.attribute.character_attribute import CharacterAttribute
from components.attribute.attribute import Vitality, Endurance, Strength, Agility
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
from components.character.character_action import (
    CharacterAction,
    BasicCharacterAction,
    CombatCharacterAction,
    BasicMobCharacterAction,
)
from components.item.equipment import SteelArmor, SteelSword
from components.action.goal.goal import TrainingGoal
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
            return True
        return False

    def is_stop(self):
        return self.amount == self.spawn_counter


class HumanGenerator(CharacterGenerator):
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        super().__init__(interval, amount, location)
        self.name = "Human"

    def spawn(self):
        # stat = CharacterStat()
        # stat.add_stat(StatDefinition.MAX_HEALTH, random.randint(100, 150))
        # stat.add_stat(
        #     StatDefinition.CURRENT_HEALTH,
        #     stat.get_stat(StatDefinition.MAX_HEALTH).value,
        # )
        # stat.add_stat(StatDefinition.POWER, random.randint(15, 30))
        # stat.add_stat(StatDefinition.SPEED, random.randint(80, 120))
        attributes = CharacterAttribute()
        attributes.add_base_attribute(Vitality(random.randint(7, 9)))
        attributes.add_base_attribute(Endurance(random.randint(5, 7)))
        attributes.add_base_attribute(Strength(random.randint(7, 9)))
        attributes.add_base_attribute(Agility(random.randint(10, 14)))

        new_human = Character(
            self.location,
            pygame.image.load("data/sprites/character3.png"),
            CharacterInfo("Human"),
            # stat,
            attributes,
            Human(),
            1,
        )
        new_human.add_archetype(Player)
        new_human.add_archetype(SwordTrainee)

        new_human.set_character_action(BasicCharacterAction())
        new_human.set_vision_range(7)

        new_human.add_item(SteelArmor())
        new_human.add_item(SteelSword())

        new_human.add_strategy(CharacterStrategyType.Move, ThinkingMove())
        new_human.add_behavior(
            FightingBehavior.name, FightingBehavior.create_random_behavior()
        )
        new_human.add_goal(1, TrainingGoal(**{"target_level": 2}))
        get_store().add(EntityType.CHARACTER, new_human.get_info().id, new_human)


class DemonGenerator(CharacterGenerator):
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        super().__init__(interval, amount, location)
        self.name = "Demon"

    def spawn(self):
        # stat = CharacterStat()
        # stat.add_stat(StatDefinition.MAX_HEALTH, random.randint(200, 300))
        # stat.add_stat(
        #     StatDefinition.CURRENT_HEALTH,
        #     stat.get_stat(StatDefinition.MAX_HEALTH).value,
        # )
        # stat.add_stat(StatDefinition.POWER, random.randint(30, 50))
        # stat.add_stat(StatDefinition.SPEED, random.randint(50, 70))
        attributes = CharacterAttribute()
        attributes.add_base_attribute(Vitality(random.randint(8, 12)))
        attributes.add_base_attribute(Endurance(random.randint(8, 12)))
        attributes.add_base_attribute(Strength(random.randint(7, 13)))
        attributes.add_base_attribute(Agility(random.randint(4, 6)))
        new_demon = Character(
            self.location,
            pygame.image.load("data/sprites/demon2.png"),
            CharacterInfo("Demon"),
            # stat,
            attributes,
            Demon(),
            1,
        )
        new_demon.add_archetype(Player)
        new_demon.add_archetype(SwordTrainee)
        new_demon.set_character_action(BasicCharacterAction())
        new_demon.set_vision_range(7)

        new_demon.add_item(SteelArmor())
        new_demon.add_item(SteelSword())

        new_demon.add_strategy(CharacterStrategyType.Move, ThinkingMove())
        new_demon.add_behavior(
            FightingBehavior.name, FightingBehavior.create_random_behavior()
        )
        new_demon.add_goal(1, TrainingGoal(**{"target_level": 2}))
        get_store().add(EntityType.CHARACTER, new_demon.get_info().id, new_demon)


class RuinMobGenerator(CharacterGenerator):
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        super().__init__(interval, amount, location)
        self.name = "RuinMob"

    def spawn(self):
        # stat = CharacterStat()
        # stat.add_stat(StatDefinition.MAX_HEALTH, random.randint(300, 600))
        # stat.add_stat(
        #     StatDefinition.CURRENT_HEALTH,
        #     stat.get_stat(StatDefinition.MAX_HEALTH).value,
        # )
        # stat.add_stat(StatDefinition.POWER, random.randint(50, 80))
        # stat.add_stat(StatDefinition.SPEED, random.randint(25, 50))
        attributes = CharacterAttribute()
        attributes.add_base_attribute(Vitality(random.randint(10, 14)))
        attributes.add_base_attribute(Endurance(random.randint(10, 14)))
        attributes.add_base_attribute(Strength(random.randint(10, 14)))
        attributes.add_base_attribute(Agility(random.randint(3, 5)))
        new_mob = Character(
            self.location,
            pygame.image.load("data/sprites/ruinmob1.png"),
            CharacterInfo("RuinMob"),
            # stat,
            attributes,
            Ruin(),
            1,
        )
        new_mob.add_archetype(Mob)
        new_mob.set_character_action(BasicMobCharacterAction())
        new_mob.add_strategy(CharacterStrategyType.Move, AgressiveMobMove())
        new_mob.add_behavior(FightingBehavior.name, AggressiveBehavior())
        get_store().add(EntityType.CHARACTER, new_mob.get_info().id, new_mob)


class ForsetMobGenerator(CharacterGenerator):
    def __init__(self, interval: int, amount: int, location: Point) -> None:
        super().__init__(interval, amount, location)
        self.name = "ForestMob"

    def spawn(self):
        # stat = CharacterStat()
        # stat.add_stat(StatDefinition.MAX_HEALTH, random.randint(75, 125))
        # stat.add_stat(
        #     StatDefinition.CURRENT_HEALTH,
        #     stat.get_stat(StatDefinition.MAX_HEALTH).value,
        # )
        # stat.add_stat(StatDefinition.POWER, random.randint(10, 20))
        # stat.add_stat(StatDefinition.SPEED, random.randint(50, 80))
        attributes = CharacterAttribute()
        attributes.add_base_attribute(Vitality(random.randint(4, 6)))
        attributes.add_base_attribute(Endurance(random.randint(4, 6)))
        attributes.add_base_attribute(Strength(random.randint(4, 6)))
        attributes.add_base_attribute(Agility(random.randint(6, 10)))
        new_mob = Character(
            self.location,
            pygame.image.load("data/sprites/forestmob1.png"),
            CharacterInfo("ForestMob"),
            # stat,
            attributes,
            Forest(),
            1,
        )
        new_mob.add_archetype(Mob)
        new_mob.set_character_action(BasicMobCharacterAction())
        new_mob.add_strategy(CharacterStrategyType.Move, PassiveMobMove())
        new_mob.add_behavior(FightingBehavior.name, PassiveBehavior())
        get_store().add(EntityType.CHARACTER, new_mob.get_info().id, new_mob)
