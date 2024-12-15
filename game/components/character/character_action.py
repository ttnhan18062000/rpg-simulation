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
    Recover,
    LearnSkill,
    ActionResult,
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
    RECOVER = 8
    LEARN_SKILL = 9


class CharacterActionModifyReason(Enum):
    APPLY_GOAL = 1


class CharacterAction:
    def __init__(self, **kwargs) -> None:
        self.actions = {}
        self.base_actions = {}
        self.kwargs = kwargs

        # TODO: this is a workaround for a bug
        # When character actively set the new character action (combat, find item)
        # the last action result doesn't contain the move
        last_action_results = kwargs.get("last_action_results", None)
        if last_action_results:
            last_action_results.append(ActionResult.MOVED_INTO_NEW_TILE)
            self.last_action_results = last_action_results
        else:
            self.last_action_results: list = [ActionResult.MOVED_INTO_NEW_TILE]

    @classmethod
    def get_name(cls):
        return cls.__name__

    # TODO: Should we change this to character_action_management?
    def get_last_action_results(self):
        return self.last_action_results

    def add_last_action_result(self, action_result: ActionResult):
        if self.last_action_results:
            self.last_action_results.append(action_result)
        else:
            self.last_action_results = [action_result]

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
        is_changed_location, last_action_results = next_action.execute(
            character, **self.kwargs
        )
        self.on_action_done()
        if last_action_results:
            self.last_action_results = last_action_results
        return is_changed_location

    def on_action_done(self):
        pass

    def modify_probabilities(
        self,
        target: ActionType,
        value: int,
        mode: str,  # "multiply" or "fixed"
        reason: CharacterActionModifyReason,
        **kwargs,
    ):
        """
        Modify the probabilities of actions.

        Parameters:
        - target (ActionType): The action to modify.
        - value (int): The multiplier or fixed probability value.
        - mode (str): "multiply" to adjust by a multiplier, "fixed" to set a fixed probability.
        - reason (CharacterActionModifyReason): The reason for modification.
        - **kwargs: Additional arguments.
        """
        # Validate target action
        if target not in self.base_actions:
            logger.debug(f"Cannot find action '{target}' in base actions.")
            return

        # Determine the new probability for the target action
        original_target_prob = self.base_actions[target]["prob"]
        total_assigned_prob = 0
        last_action_type = None
        if mode == "multiply":
            adjusted_target_prob = max(0, original_target_prob * value)

            # Calculate the total probability of other actions
            other_prob_sum = sum(
                self.base_actions[action]["prob"]
                for action in self.base_actions
                if action != target
            )

            if other_prob_sum == 0:
                logger.debug("Cannot adjust probabilities: no other actions defined.")
                return

            # Normalize probabilities
            total_prob = adjusted_target_prob + other_prob_sum

            for idx, (action_type, action_data) in enumerate(self.base_actions.items()):
                if idx == len(self.base_actions) - 1:
                    last_action_type = action_type
                    continue

                if action_type == target:
                    new_prob = int(100 * adjusted_target_prob / total_prob)
                else:
                    new_prob = int(
                        100 * self.base_actions[action_type]["prob"] / total_prob
                    )

                self.actions[action_type]["prob"] = new_prob
                total_assigned_prob += new_prob

        elif mode == "fixed":
            adjusted_target_prob = max(0, min(100, int(value)))

            remaining_prob = 100 - adjusted_target_prob

            other_prob_sum = sum(
                self.base_actions[action]["prob"]
                for action in self.base_actions
                if action != target
            )

            for idx, (action_type, action_data) in enumerate(self.base_actions.items()):
                if idx == len(self.base_actions) - 1:
                    last_action_type = action_type
                    continue

                if action_type == target:
                    new_prob = adjusted_target_prob
                else:
                    new_prob = int(
                        remaining_prob
                        * self.base_actions[action_type]["prob"]
                        / other_prob_sum
                    )

                self.actions[action_type]["prob"] = new_prob
                total_assigned_prob += new_prob
        else:
            logger.debug(f"Invalid mode '{mode}'. Use 'multiply' or 'fixed'.")
            return

        # Assign remaining probability to the last action
        if last_action_type:
            self.actions[last_action_type]["prob"] = max(0, 100 - total_assigned_prob)

        logger.debug(f"Modified probabilities for action '{target}': {self.actions}")

    def on_change(self):
        # Trigger when the character action is being replaced
        pass

    def reset_probabilities(self, reason: CharacterActionModifyReason):
        # if reason == CharacterActionModifyReason.APPLY_GOAL:
        #     self.is_applied_goal = False
        #     logger.debug(f"Reset applied goal")
        self.actions = copy.deepcopy(self.base_actions)
        logger.debug(f"Reset probabilities: {self.actions}")

    def set_kwargs(self, key, value):
        self.kwargs[key] = value

    def reset_kwargs_key(self, key):
        self.kwargs[key] = None

    def has_action(self, action_type: ActionType):
        return action_type in self.base_actions


class BasicMobCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.base_actions = {
            ActionType.MOVE: {"class": Move, "prob": 20},
            ActionType.STANDBY: {"class": Standby, "prob": 80},
        }
        self.actions = {
            ActionType.MOVE: {"class": Move, "prob": 20},
            ActionType.STANDBY: {"class": Standby, "prob": 80},
        }


class BasicCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.base_actions = {
            ActionType.MOVE: {"class": Move, "prob": 50},
            ActionType.TRAIN: {"class": Train, "prob": 50},
            ActionType.RECOVER: {"class": Recover, "prob": 0},
            ActionType.LEARN_SKILL: {"class": LearnSkill, "prob": 0},
        }
        self.actions = {
            ActionType.MOVE: {"class": Move, "prob": 50},
            ActionType.TRAIN: {"class": Train, "prob": 50},
            ActionType.RECOVER: {"class": Recover, "prob": 0},
            ActionType.LEARN_SKILL: {"class": LearnSkill, "prob": 0},
        }


class CombatCharacterAction(CharacterAction):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
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
        health_ratio = character.get_character_stat().get_health_ratio()
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
        super().__init__(**kwargs)
        self.base_actions = {
            ActionType.MOVE: {"class": Move, "prob": 0},
            ActionType.SEARCH: {"class": Search, "prob": 100},
        }
        self.actions = {
            ActionType.MOVE: {"class": Move, "prob": 0},
            ActionType.SEARCH: {"class": Search, "prob": 100},
        }
        self.kwargs = kwargs
        self.max_attempt = kwargs.get("max_attempt", 5)
        self.attempt_counter = 0

    def get_modified_actions(self, character):
        if self.attempt_counter < self.max_attempt:
            return self.actions
        else:
            return {
                ActionType.MOVE: {"class": Move, "prob": 100},
                ActionType.SEARCH: {"class": Search, "prob": 0},
            }

    def on_action_done(self):
        self.attempt_counter += 1
        if self.attempt_counter <= self.max_attempt:
            logger.debug(f"Search attempt: {self.attempt_counter}")
