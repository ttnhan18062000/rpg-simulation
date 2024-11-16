from enum import Enum
import random

from components.common.point import Point
from components.action.event import EventType

from data.logs.logger import logger


class Memory:
    def __init__(self, id, pos: Point) -> None:
        self.id = id
        self.pos = pos

    def get_location(self):
        return self.pos

    def get_id(self):
        return self.id


class PowerEst(Enum):
    MUCH_WEAKER = 1
    WEAKER = 2
    SAME = 3
    STRONGER = 4
    MUCH_STRONGER = 5
    UNKNOWN = 6


class MemoryCharacter(Memory):
    def __init__(self, id, pos: Point, faction) -> None:
        super().__init__(id, pos)
        self.power_value_est: PowerEst = PowerEst.UNKNOWN
        self.faction = faction

    def get_faction(self):
        return self.faction

    def remember_power(self, character, target_character, perception_accuracy=90):
        # Calculate power ratio
        ratio = target_character.get_power() / character.get_power()

        # Add random factor for error
        if perception_accuracy < 100:
            randomness_factor = 1 - (perception_accuracy / 100)
            error_factor = random.uniform(1 - randomness_factor, 1 + randomness_factor)
            adjusted_ratio = ratio * error_factor
        else:
            adjusted_ratio = ratio

        # Define ranges for each PowerEst level
        if adjusted_ratio <= 0.75:
            self.power_value_est = PowerEst.MUCH_WEAKER
        elif 0.75 < adjusted_ratio <= 0.9:
            self.power_value_est = PowerEst.WEAKER
        elif 0.9 < adjusted_ratio <= 1.1:
            self.power_value_est = PowerEst.SAME
        elif 1.1 < adjusted_ratio <= 1.35:
            self.power_value_est = PowerEst.STRONGER
        elif adjusted_ratio > 1.35:
            self.power_value_est = PowerEst.MUCH_STRONGER

    def get_power_est(self):
        return self.power_value_est


class MemoryEvent(Memory):

    def __init__(self, id, pos: Point, event_type: EventType) -> None:
        super().__init__(id, pos)
        self.event_type: EventType = event_type

    def get_event_type(self):
        return self.event_type

    # TODO: MemoryEvent holds different event types, should be split into multiple derived classes
    # since remember_power only belong to combat event
    def remember_power(self, character, combat, perception_accuracy=90):
        # Calculate power ratio
        character_faction = character.get_faction()
        ratio = combat.get_hostile_power(character_faction) / (
            character.get_power() + combat.get_total_power_by_faction(character_faction)
        )

        # Add random factor for error
        if perception_accuracy < 100:
            randomness_factor = 1 - (perception_accuracy / 100)
            error_factor = random.uniform(1 - randomness_factor, 1 + randomness_factor)
            adjusted_ratio = ratio * error_factor
        else:
            adjusted_ratio = ratio

        # Define ranges for each PowerEst level
        if adjusted_ratio <= 0.5:
            self.power_value_est = PowerEst.MUCH_WEAKER
        elif 0.5 < adjusted_ratio <= 0.8:
            self.power_value_est = PowerEst.WEAKER
        elif 0.8 < adjusted_ratio <= 1.25:
            self.power_value_est = PowerEst.SAME
        elif 1.25 < adjusted_ratio <= 2:
            self.power_value_est = PowerEst.STRONGER
        elif adjusted_ratio > 2:
            self.power_value_est = PowerEst.MUCH_STRONGER

    def get_power_est(self):
        return self.power_value_est
