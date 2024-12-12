from enum import Enum

from components.action.goal import Goal
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
        self.current_apply_status: CharacterGoalStatus = CharacterGoalStatus.NOTHING

    def add(self, priority: int, goal: Goal):
        goal_name = goal.get_name()
        existing_duplicated_goal = None
        if self.goals.has(goal_name):
            existing_duplicated_goal = self.goals.get(goal_name)
        if self.current_goal and self.current_goal.get_name() == goal_name:
            existing_duplicated_goal = self.current_goal
        if existing_duplicated_goal:
            existing_duplicated_goal.update_with_goal(goal)
            logger.debug(f"Updated existing goal {existing_duplicated_goal}")
        else:
            self.goals.set_with_highest_priority(goal.get_name(), goal)
            self.load_current_goal()
            logger.debug(f"Added new goal {goal}")

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
            self.current_goal.apply_to_actions(character)
            self.current_apply_status = CharacterGoalStatus.ALREADY_APPLIED
            logger.debug(f"Applied goal {self.current_goal}")

    def reset_status_to_waiting(self):
        if self.current_apply_status == CharacterGoalStatus.ALREADY_APPLIED:
            self.current_apply_status = CharacterGoalStatus.WAITING_TO_APPLY

    def is_waiting_to_apply(self):
        return self.current_apply_status == CharacterGoalStatus.WAITING_TO_APPLY

    def is_already_applied_goal(self):
        return self.current_apply_status == CharacterGoalStatus.ALREADY_APPLIED

    def load_current_goal(self):
        if not self.current_goal:
            if self.is_empty():
                return None
            priority, self.current_goal = self.get()
            self.on_start_goal()

    def get_current_goal(self):
        self.load_current_goal()
        return self.current_goal

    def check_done_current_goal(self, character):
        if self.get_current_goal().is_complete(character):
            logger.debug(f"Goal {self.get_current_goal().get_name()} is completed")
            self.on_complete_goal(character)
            return True
        return False
