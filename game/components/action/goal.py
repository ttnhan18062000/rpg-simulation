class Goal:
    def __init__(self) -> None:
        pass

    def is_complete(self, character):
        pass

    
    def apply_goal(self, character):
        pass


class TrainingGoal(Goal):
    # Keep training until reach a given level
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.target_level = kwargs.get("target_level")

    def is_complete(self, character):
        return character.get_level().get_current_level() >= self.target_level
    
    def apply_goal(self, character):

