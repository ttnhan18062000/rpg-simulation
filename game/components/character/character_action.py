import numpy
from enum import Enum
import copy

from components.action.action import (
    Move,
    Interact,
    Train,
    Standby,
    Fight,
    Escape,
    Search,
)
from components.character.character_behavior import FightingBehavior
from components.character.character_stat import StatDefinition

from data.logs.logger import logger


class ActionType(Enum):
    MOVE = 1
    INTERACT = 2
    TRAIN = 3
    STANDBY = 4
    FIGHT = 5
    ESCAPE = 6
    SEARCH = 7


class CharacterActionModifyReason(Enum):
    APPLY_GOAL = 1


class CharacterAction:
    def __init__(self, **kwargs) -> None:
        self.actions = {}
        self.base_actions = {}
        self.kwargs = kwargs

    @classmethod
    def get_name(cls):
        return cls.__name__

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

    def modify_probabilities(
        self,
        target: ActionType,
        multiplier: int,
        reason: CharacterActionModifyReason,
        **kwargs,
    ):
        # if reason == CharacterActionModifyReason.APPLY_GOAL:
        #     if self.applied_goal:
        #         logger.debug(f"Already applied goal")
        #     else:
        #         self.applied_goal = kwargs.get("goal")
        if target not in self.base_actions:
            logger.debug(f"Cannot find action '{target}'")

        new_total_prob = self.base_actions[target]["prob"] * multiplier + (
            100 - self.base_actions[target]["prob"]
        )

        total_assigned_prob = 0
        last_action_type = None
        for idx, action_type in enumerate(self.base_actions.keys()):
            if idx == len(self.base_actions) - 1:
                # Save the last action to adjust later
                last_action_type = action_type
                continue

            if action_type == target:
                new_prob = int(
                    100
                    * self.base_actions[action_type]["prob"]
                    * multiplier
                    / new_total_prob
                )
            else:
                new_prob = int(
                    100 * self.base_actions[action_type]["prob"] / new_total_prob
                )

            self.actions[action_type]["prob"] = new_prob
            total_assigned_prob += new_prob

        # Assign remaining probability to the last action
        if last_action_type:
            self.actions[last_action_type]["prob"] = 100 - total_assigned_prob

        logger.debug(
            f"Applied multiplier to action: {target}={self.actions[target]['prob']}"
        )

    def on_change(self):
        # Trigger when the character action is being replaced
        pass

    def reset_probabilities(self, reason: CharacterActionModifyReason):
        # if reason == CharacterActionModifyReason.APPLY_GOAL:
        #     self.is_applied_goal = False
        #     logger.debug(f"Reset applied goal")
        self.actions = copy.deepcopy(self.base_actions)

    def has_action(self, action_type: ActionType):
        return action_type in self.base_actions


class BasicMobCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.base_actions = {
            ActionType.MOVE: {"class": Move, "prob": 20},
            ActionType.STANDBY: {"class": Standby, "prob": 80},
        }
        self.actions = {
            ActionType.MOVE: {"class": Move, "prob": 20},
            ActionType.STANDBY: {"class": Standby, "prob": 80},
        }
        self.kwargs = kwargs


class BasicCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.base_actions = {
            ActionType.MOVE: {"class": Move, "prob": 50},
            ActionType.TRAIN: {"class": Train, "prob": 50},
        }
        self.actions = {
            ActionType.MOVE: {"class": Move, "prob": 50},
            ActionType.TRAIN: {"class": Train, "prob": 50},
        }
        self.kwargs = kwargs


class CombatCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.base_actions = {
            ActionType.FIGHT: {"class": Fight, "prob": 100},
            ActionType.ESCAPE: {"class": Escape, "prob": 0},
        }
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
            character.get_final_stat().get_stat(StatDefinition.CURRENT_HEALTH).value
        )
        max_health = (
            character.get_final_stat().get_stat(StatDefinition.MAX_HEALTH).value
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


class FindItemCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.base_actions = {
            ActionType.MOVE: {"class": Move, "prob": 10},
            ActionType.SEARCH: {"class": Search, "prob": 90},
        }
        self.actions = {
            ActionType.MOVE: {"class": Move, "prob": 10},
            ActionType.SEARCH: {"class": Search, "prob": 90},
        }
        self.kwargs = kwargs
