from components.archetype.archetype import Archetype, Player
from components.archetype.lineage import Lineage
from components.race.race import Human, Demon
from components.attribute.attribute import Strength, Agility
from components.archetype.skill.swordman_skill import Slash, SwordDance


class SwordmanLineage(Lineage):
    pass


class SwordTrainee(Archetype, SwordmanLineage):
    required_attributes = {Strength(15), Agility(15)}
    required_races = [Human.get_name(), Demon.get_name()]
    required_archetypes = [Player()]
    learnable_skills = [Slash, SwordDance]


class Swordman(Archetype, SwordmanLineage):
    required_attributes = {Strength(25), Agility(25)}
    required_races = [Human.get_name(), Demon.get_name()]
    required_archetypes = [Player(), SwordTrainee()]
    learnable_skills = None


# class Swordmaster(Archetype):
#     required_attributes = {Strength(8), Agility(8)}
#     required_races = [Human.get_name(), Demon.get_name()]
#     required_archetypes = [Player.get_name()]
#     lineage = SwordmanLineage()


# class Swordsaint(Archetype):
#     required_attributes = {Strength(8), Agility(8)}
#     required_races = [Human.get_name(), Demon.get_name()]
#     required_archetypes = [Player.get_name()]
#     lineage = SwordmanLineage()
