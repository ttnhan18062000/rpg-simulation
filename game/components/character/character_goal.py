from queue import PriorityQueue
from enum import Enum

from components.action.goal import Goal

from data.logs.logger import logger


class GoalPriorityQueue(PriorityQueue):
    def __init__(self):
        super().__init__()
        # self.lowest_priority = float("inf")  # Start with the highest possible value
        self.lowest_priority = 1000

    def put_with_highest_priority(self, item):
        # Add the new item with a priority smaller than the current smallest
        self.lowest_priority -= 1
        self.put((self.lowest_priority, item))


class CharacterGoalStatus(Enum):
    NOTHING = 1
    WAITING_TO_APPLY = 2
    ALREADY_APPLIED = 3


class CharacterGoal:
    def __init__(self) -> None:
        self.goals = GoalPriorityQueue()
        self.current_goal: Goal = None
        self.current_apply_status: CharacterGoalStatus = CharacterGoalStatus.NOTHING

    def add(self, priority: int, goal: Goal):
        self.goals.put_with_highest_priority(goal)
        self.load_current_goal()
        logger.debug(f"Added new goal {goal}")

    def get(self):
        return self.goals.get()

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
            logger.debug(f"Goal {self.get_current_goal()} is completed")
            self.on_complete_goal(character)
            return True
        return False
