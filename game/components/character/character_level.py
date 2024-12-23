from components.character.class_level import ClassLevel
from data.logs.logger import logger


class CharacterLevel:
    def __init__(self, class_level: ClassLevel, current_level: int) -> None:
        self.current_exp = 0
        self.class_level = class_level
        self.current_level = current_level
        self.next_level_required_exp = self.class_level.get_next_level_required_exp(
            self.current_level
        )

    def add_exp(self, exp: int):
        self.current_exp += exp

        if self.current_exp >= self.next_level_required_exp:
            self.current_level += 1
            self.current_exp -= self.next_level_required_exp
            self.next_level_required_exp = self.class_level.get_next_level_required_exp(
                self.current_level
            )
            return True

        return False

    def get_current_level(self):
        return self.current_level

    def get_exp_visualization(self):
        return f"({self.current_exp}/{self.next_level_required_exp})"
