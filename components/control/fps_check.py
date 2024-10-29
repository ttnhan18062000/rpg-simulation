import time

from components.world.store import get_store, EntityType

from data.logs.logger import logger


class FPSCheck:
    def __init__(self) -> None:
        self.timestamp = time.time()
        self.frame_count = 0

    def check(self):
        self.frame_count += 1
        if self.timestamp + 1 < time.time():
            logger.debug(f"FPS: {self.frame_count}")
            self.check_population()
            self.frame_count = 0
            self.timestamp = time.time()

    def check_population(self):
        store = get_store()
        all_characters = store.get_all(EntityType.CHARACTER)
        dead_count = {}
        alive_count = {}
        for character in all_characters:
            character_class = character.get_character_class()
            if character.is_alive():
                if character_class not in alive_count:
                    alive_count[character_class] = 1
                else:
                    alive_count[character_class] += 1
            else:
                if character_class not in dead_count:
                    dead_count[character_class] = 1
                else:
                    dead_count[character_class] += 1
        logger.debug(f"DEAD: {dead_count}")
        logger.debug(f"ALIVE: {alive_count}")
