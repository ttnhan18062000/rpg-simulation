import numpy

from components.action.action import Move, Interact, Standby


class CharacterAction:
    def __init__(self) -> None:
        self.actions = [
            Move(),
            # Interact(),
            Standby(),
        ]  # PROBLEM: Many duplicated instances will be created
        self.action_probabilities = [1 / 2, 1 / 2]

    def get_next_action(self):
        next_action_id = numpy.random.choice(
            numpy.arange(0, len(self.actions)), p=self.action_probabilities
        )
        return self.actions[next_action_id]
