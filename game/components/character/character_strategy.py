from enum import Enum

from components.action.strategy.base_strategy import BaseStrategy


class CharacterStrategyType(Enum):
    Move = 1
    USE_SKILL = 2


class CharacterStrategy:
    def __init__(self):
        self.strategies = {}

    def get(self, strategy_type: CharacterStrategyType):
        if strategy_type not in self.strategies:
            return None
        return self.strategies.get(strategy_type)

    def add(self, strategy_type: CharacterStrategyType, strategy: BaseStrategy):
        self.strategies[strategy_type] = strategy
