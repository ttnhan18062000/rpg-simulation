from components.action.strategy.base_strategy import BaseStrategy
from components.archetype.skill.skill import Skill


class UseSkillStrategy(BaseStrategy):
    def __init__(self):
        pass

    @classmethod
    def get_next_skill(cls, character):
        pass


class SaveEnergy(UseSkillStrategy):
    # Use skill with most efficient energy cost
    @classmethod
    def get_next_skill(cls, character):
        highest_damage_per_energy_value = 0
        selected_skill = None
        selected_skill_damage = 0
        skills: dict[str, Skill] = character.get_skills()
        for skill_name, skill in skills.items():
            if skill.is_learned():
                damage = skill.get_damage(
                    character.get_final_stat(), character.get_final_attributes()
                )
                energy_cost = skill.get_energy_cost()
                damage_per_energy = damage / energy_cost
                if damage_per_energy > highest_damage_per_energy_value:
                    highest_damage_per_energy_value = damage_per_energy
                    selected_skill = skill
                    selected_skill_damage = damage
        return selected_skill, selected_skill_damage


class HighestDamageOutput(UseSkillStrategy):
    # Use skill with most efficient energy cost
    @classmethod
    def get_next_skill(cls, character):
        selected_skill = None
        selected_skill_damage = 0
        skills: dict[str, Skill] = character.get_skills()
        for skill_name, skill in skills.items():
            if skill.is_learned():
                damage = skill.get_damage(
                    character.get_final_stat(), character.get_final_attributes()
                )
                energy_cost = skill.get_energy_cost()
                if damage > selected_skill_damage:
                    selected_skill = skill
                    selected_skill_damage = damage
        return selected_skill, selected_skill_damage
