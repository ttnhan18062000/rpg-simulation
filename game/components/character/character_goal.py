from queue import PriorityQueue

from components.action.goal import Goal


class CharacterGoal:
    def __init__(self) -> None:
        self.goals = PriorityQueue()
        self.current_goal: Goal = None

    def add(self, priority: int, goal: Goal):
        self.goals.put((priority, goal))

    def get(self):
        return self.goals.get()

    def is_empty(self):
        return self.goals.empty()

    def get_current_goal(self):
        if not self.current_goal:
            if self.is_empty():
                return None
            self.current_goal = self.get()
        return self.current_goal

    def complete_goal(self):
        self.current_goal = None
