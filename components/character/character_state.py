class CharacterState:
    def __init__(self) -> None:
        pass


class CombatState(CharacterState):
    def __init__(self, target_character_ids) -> None:
        super().__init__()
        self.name = "Combat"
        self.target_character_ids = target_character_ids
