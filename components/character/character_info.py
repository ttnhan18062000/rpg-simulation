class CharacterInfo:
    id_counter = 0

    def __init__(self, name) -> None:
        self.id = CharacterInfo.id_counter
        CharacterInfo.id_counter += 1
        self.name = name

    def __str__(self) -> str:
        return f"{self.id}@{self.name}"
