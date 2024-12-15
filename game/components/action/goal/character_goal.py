from enum import Enum

from components.action.goal.goal import Goal
from components.common.priority_dict import PriorityDict

from data.logs.logger import logger


class GoalPriorityDict:
    def __init__(self):
        self.dict = {}


class CharacterGoalStatus(Enum):
    NOTHING = 1
    WAITING_TO_APPLY = 2
    ALREADY_APPLIED = 3


class CharacterGoal:
    def __init__(self) -> None:
        self.goals = PriorityDict()
        self.current_goal: Goal = None
        self.current_priority: int = -1
        self.current_apply_status: CharacterGoalStatus = CharacterGoalStatus.NOTHING

    def add(self, priority: int, goal: Goal, update_if_exist=False):
        goal_name = goal.get_name()

        # existing_duplicated_goal = None
        # if update_if_exist:
        #     if self.goals.has(goal_name):
        #         existing_duplicated_goal = self.goals.get(goal_name)
        #     if self.current_goal and self.current_goal.get_name() == goal_name:
        #         existing_duplicated_goal = self.current_goal
        #     if existing_duplicated_goal:
        #         existing_duplicated_goal.update_with_goal(goal)
        #         logger.debug(f"Updated existing goal {existing_duplicated_goal}")
        #     else:
        # self.goals.set_with_highest_priority(goal.get_name(), goal)
        # self.load_current_goal()
        # logger.debug(f"Added new goal {goal}")
        logger.debug(f"Adding goal {goal}")
        if goal.is_unique() and self.goals.has(goal_name, goal):
            logger.debug(f"Goal '{goal}' already added")
            return -1
        else:
            if priority <= 1:
                priority = self.goals.set_with_highest_priority(goal_name, goal)
                self.load_current_goal()
            else:
                priority = self.goals.set_to_priority(priority, goal_name, goal)
            logger.debug(f"Added new goal {goal}")
            return priority

    def get(self):
        return self.goals.get_highest_priority()

    def get_current_apply_status(self):
        return self.current_apply_status

    def is_empty(self):
        return self.goals.empty()

    def has_goal(self):
        return self.current_goal is not None

    def on_start_goal(self):
        self.current_apply_status = CharacterGoalStatus.WAITING_TO_APPLY

    def on_complete_goal(self, character):
        self.current_goal.on_complete(character)
        self.current_goal = None
        self.current_apply_status = CharacterGoalStatus.NOTHING
        self.load_current_goal()

    def apply_goal(self, character):
        if (
            self.current_apply_status == CharacterGoalStatus.WAITING_TO_APPLY
            and self.current_goal.can_apply_to(character)
        ):
            self.current_apply_status = CharacterGoalStatus.ALREADY_APPLIED
            if not self.current_goal.is_applied_to_character():
                self.current_goal.apply_to_character(character)
            self.current_goal.apply_to_actions(character)
            logger.debug(f"Applied goal {self.current_goal}")

    def reset_status_to_waiting(self):
        if self.current_apply_status == CharacterGoalStatus.ALREADY_APPLIED:
            self.current_apply_status = CharacterGoalStatus.WAITING_TO_APPLY

    def is_waiting_to_apply(self):
        return self.current_apply_status == CharacterGoalStatus.WAITING_TO_APPLY

    def is_already_applied_goal(self):
        return self.current_apply_status == CharacterGoalStatus.ALREADY_APPLIED

    # TODO: deal with big goal contain child goals
    def load_current_goal(self):
        if not self.current_goal:
            if self.is_empty():
                return None
            self.current_priority, self.current_goal = self.get()
            self.on_start_goal()

    def get_current_goal(self):
        self.load_current_goal()
        return self.current_goal

    def clear_current_goal(self):
        logger.debug(f"Clear the current goal {self.get_current_goal().get_name()}")
        self.current_goal = None
        self.goals.remove_with_priority(self.current_priority)
        self.current_priority = -1

    def check_done_current_goal(self, character):
        if self.has_goal() and self.get_current_goal().is_complete(character):
            logger.debug(f"Goal {self.get_current_goal().get_name()} is completed")
            self.on_complete_goal(character)
            return True
        return False

    def check_block_current_goal(self, character):
        if self.has_goal() and self.get_current_goal().is_block(character):
            logger.debug(f"Goal {self.get_current_goal().get_name()} is blocked")
            return True
        return False
