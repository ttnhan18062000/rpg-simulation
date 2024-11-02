import pygame

from components.world.store import get_store, EntityType
from components.action.event import CombatEvent
from components.character.character_stat import StatDefinition
from components.display.box import Box, BoxContent, TextContent, ImageContent

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)

class CombatBox:
    def __init__(self, width, height, combat_event_id) -> None:
        self.width = width
        self.height = height
        self.combat_event_id = combat_event_id

        self.bg_color = (175, 175, 175)

        character_info_dict = self.get_character_info_dict()

        self.init_boxes(self.n_character)

    def get_character_info_dict(self):
        store = get_store()
        combat_event: CombatEvent = store.get(EntityType.EVENT, self.combat_event_id)
        character_info_dict = {}
        for faction in combat_event.get_factions():
            for cid in combat_event.get_character_ids_with_faction(faction):
                character = store.get(EntityType.CHARACTER, cid)
                current_health = character.character_stats.get_stat(StatDefinition.CURRENT_HEALTH).value
                max_health = character.character_stats.get_stat(StatDefinition.MAX_HEALTH).value
                power = character.character_stats.get_stat(StatDefinition.POWER).value
                level = character.level.current_level
                exp = character.level.current_exp
                next_level_exp = character.level.next_level_required_exp
                self.character_info_dict.update({cid : {
                    "faction": faction,
                    "info": str(character.get_info()),
                    "current_health": current_health,
                    "max_health": max_health,
                    "power": power,
                    "level": level,
                    "exp": exp,
                    "next_level_exp": next_level_exp,
                    "img": character.img
                }})
        return character_info_dict


    def display_character_info(self, character_info_dict):
        b = Box(300, 100, self.bg_color, (0, 0, 0))

        c_b1 = Box(25, 25, self.bg_color, (0, 0, 0))
        header = Box(300, 25, self.bg_color, (0, 0, 0))
        header.add_box(c_b1, (180, 0))

        for character_info in character_info_dict.values():
            char_box = Box(250, 50, self.bg_color, None)

            avt_box = Box(25, 25, self.bg_color, None)
            char_box.add_box(avt_box, (0, 0))

            level_box = Box(50, 25, self.bg_color, None)
            char_box.add_box(level_box, (25, 0))

            exp_box = Box(100, 25, self.bg_color, None)
            char_box.add_box(exp_box, (75, 0))

            power_box = Box(75, 25, self.bg_color, None)
            char_box.add_box(power_box, (175, 0))

            info_box = Box(150, 25, self.bg_color, None)
            char_box.add_box(info_box, (0, 25))

            hp_box = Box(100, 25, self.bg_color, None)
            char_box.add_box(hp_box, (150, 25))

            b.add_box(header, (0, 0))
            b.add_box(char_box, (0, 25))

            avt_content = ImageContent(character_info["img"])
            avt_box.box_content = avt_content

            level_content = TextContent(character_info["level"])
            level_box.box_content = level_content

            exp_content = TextContent(f"{character_info['exp']}/{character_info['next_level_exp']}")
            exp_box.box_content = exp_content

            power_content = TextContent(character_info["power"])
            power_box.box_content = power_content

            hp_content = TextContent(f"{character_info['current_health']}/{character_info['max_health']}")
            hp_box.box_content = hp_content

            info_content = TextContent(character_info["info"])
            info_box.box_content = info_content


    def draw(self, surface: pygame.Surface, character_to_health_dict):

