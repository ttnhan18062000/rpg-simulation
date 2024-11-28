import numpy
from enum import Enum

from components.action.action import Move, Interact, Train, Standby, Fight, Escape
from components.character.character_behavior import FightingBehavior
from components.character.character_stat import StatDefinition


class ActionType(Enum):
    MOVE = 1
    INTERACT = 2
    TRAIN = 3
    STANDBY = 4
    FIGHT = 5
    ESCAPE = 6


class CharacterAction:
    def __init__(self, **kwargs) -> None:
        self.actions = {}
        self.kwargs = kwargs

    def get_modified_actions(self, character):
        return self.actions

    def get_next_action(self, character):
        modified_actions = self.get_modified_actions(character)
        action_list = [at["class"] for at in modified_actions.values()]
        prob_list = [at["prob"] for at in modified_actions.values()]
        next_action_id = numpy.random.choice(
            numpy.arange(0, len(action_list)),
            p=[ap / 100 for ap in prob_list],
        )
        return action_list[next_action_id]

    def set_action_probabilities(self, action_prob_dict):
        for action_type, new_prob in action_prob_dict.items():
            self.actions[action_type] = new_prob

    def do_action(self, character):
        next_action = self.get_next_action(character)
        return next_action.execute(character, **self.kwargs)


class BasicMobCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.actions = {
            ActionType.MOVE: {"class": Move, "prob": 20},
            ActionType.STANDBY: {"class": Standby, "prob": 80},
        }
        self.kwargs = kwargs


class BasicCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.actions = {
            ActionType.MOVE: {"class": Move, "prob": 50},
            ActionType.TRAIN: {"class": Train, "prob": 50},
        }
        self.kwargs = kwargs


class CombatCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.actions = {
            ActionType.FIGHT: {"class": Fight, "prob": 100},
            ActionType.ESCAPE: {"class": Escape, "prob": 0},
        }
        self.kwargs = kwargs
        if kwargs.get(FightingBehavior.name):
            self.escape_threshold = kwargs.get(
                FightingBehavior.name
            ).get_escape_threshold()
        else:
            self.escape_threshold = 0.25

    def get_modified_actions(self, character):
        cur_health = (
            character.get_status_applied_character_stat()
            .get_stat(StatDefinition.CURRENT_HEALTH)
            .value
        )
        max_health = (
            character.get_status_applied_character_stat()
            .get_stat(StatDefinition.MAX_HEALTH)
            .value
        )
        health_ratio = cur_health / max_health
        if health_ratio < self.escape_threshold:
            new_fight_prob = int(100 * (health_ratio / 2))
            return {
                ActionType.FIGHT: {
                    "class": Fight,
                    "prob": new_fight_prob,
                },
                ActionType.ESCAPE: {
                    "class": Escape,
                    "prob": 100 - new_fight_prob,
                },
            }
        else:
            return self.actions
