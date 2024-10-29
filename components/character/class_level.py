class ClassLevel:
    def __init__(self) -> None:
        self.base_required_exp = 100
        self.next_level_mul = 2

    def get_next_level_required_exp(self, current_level: int):
        return self.base_required_exp * (self.next_level_mul**current_level)


class HumanLevel(ClassLevel):
    def __init__(self) -> None:
        super().__init__()
        self.base_required_exp = 100
        self.next_level_mul = 2


class DemonLevel(ClassLevel):
    def __init__(self) -> None:
        super().__init__()
        self.base_required_exp = 200
        self.next_level_mul = 2
