import numpy
from enum import Enum

from components.action.action import Move, Interact, Standby, Fight, Escape


class ActionType(Enum):
    MOVE = 1
    INTERACT = 2
    STANDBY = 3
    FIGHT = 4
    ESCAPE = 5


class CharacterAction:

    def __init__(self, **kwargs) -> None:
        self.actions = {}
        self.kwargs = kwargs

    def get_next_action(self):
        action_list = [at["class"] for at in self.actions.values()]
        prob_list = [at["prob"] for at in self.actions.values()]
        next_action_id = numpy.random.choice(
            numpy.arange(0, len(action_list)),
            p=[ap / 100 for ap in prob_list],
        )
        return action_list[next_action_id]

    def set_action_probabilities(self, action_prob_dict):
        for action_type, new_prob in action_prob_dict.items():
            self.actions[action_type] = new_prob

    def do_action(self, character):
        next_action = self.get_next_action()
        return next_action.execute(character, **self.kwargs)


class BasicCharacterAction(CharacterAction):

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.actions = {
            ActionType.MOVE: {"class": Move(), "prob": 50},
            ActionType.STANDBY: {"class": Standby(), "prob": 50},
        }
        self.kwargs = kwargs


class CombatCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.actions = {
            ActionType.FIGHT: {"class": Fight(), "prob": 50},
            ActionType.ESCAPE: {"class": Escape(), "prob": 50},
        }
        self.kwargs = kwargs
