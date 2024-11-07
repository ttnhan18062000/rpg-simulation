import time

from components.world.store import get_store, EntityType
from components.database.producer import produce_messages
from data.logs.logger import logger


class Monitoring:
    def __init__(self) -> None:
        self.timestamp_fps = time.time()
        self.timestamp_data = time.time()
        self.frame_count = 0

    def check(self):
        self.fps_check()
        self.update_data()

    def fps_check(self):
        self.frame_count += 1
        if self.timestamp_fps + 1 < time.time():
            logger.debug(f"FPS: {self.frame_count}")
            self.check_population()
            self.frame_count = 0
            self.timestamp_fps = time.time()

    def update_data(self):
        if self.timestamp_data + 1 < time.time():
            store = get_store()
            # all_characters = store.get_all(EntityType.CHARACTER)
            # for character in all_characters:
            #     character_dict = character.to_dict()
            #     produce_messages(character_dict)

            all_events = store.get_all(EntityType.EVENT)
            for event in all_events:
                event_dict = event.to_dict()
                produce_messages(event_dict)

            self.timestamp_data = time.time()

    def check_population(self):
        store = get_store()
        all_characters = store.get_all(EntityType.CHARACTER)
        dead_count = {}
        alive_count = {}
        for character in all_characters:
            character_class = character.get_faction()
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
