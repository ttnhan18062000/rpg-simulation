import random


class CharacterBehavior:
    def __init__(self) -> None:
        pass


class FightingBehavior(CharacterBehavior):
    name = "fighting_behavior"

    derived_classes = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Register each subclass in the base class list
        FightingBehavior.derived_classes.append(cls)

    @classmethod
    def create_random_behavior(cls):
        # Get a random derived class and create an instance of it
        random_class = random.choice(cls.derived_classes)
        return random_class()

    def __init__(self) -> None:
        super().__init__()

    def get_escape_threshold(self):
        return 0.25


class AggressiveBehavior(FightingBehavior):
    def __init__(self) -> None:
        super().__init__()

    def get_escape_threshold(self):
        return 0.1


class PassiveBehavior(FightingBehavior):
    def __init__(self) -> None:
        super().__init__()

    def get_escape_thresold(self):
        return 0.4
