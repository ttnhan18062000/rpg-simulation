from enum import Enum

from components.archetype.lineage import Lineage

from data.logs.logger import logger


class Archetype(Lineage):
    required_attributes = []
    required_races = []
    required_archetypes = []
    lineage = Lineage()
    learnable_skills = []

    class UnlockType(Enum):
        REQUIRE_ARCHETYPES = 1
        REQUIRE_ATTRIBUTES = 2
        REQUIRE_RACES = 3

    def __init__(self):
        self.mastery = 0
        pass

    def get_mastery(self):
        return self.mastery

    @classmethod
    def get_learnable_skills(cls):
        return cls.learnable_skills

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def get_required_attributes(cls):
        return cls.required_attributes

    @classmethod
    def is_able_to_unlock(cls, character):
        character_attr = character.get_character_attributes()
        character_race = character.get_race()
        character_archetype_names = character.get_archetype_names()

        requires = {
            Archetype.UnlockType.REQUIRE_ARCHETYPES: [],
            Archetype.UnlockType.REQUIRE_ATTRIBUTES: [],
            Archetype.UnlockType.REQUIRE_RACES: [],
        }

        if cls.required_attributes is not None:
            for attr in cls.required_attributes:
                attr_name = attr.get_name()
                req_value = attr.get_value()
                cur_value = character_attr.get_base_attr(attr_name).get_value()
                if cur_value < req_value:
                    requires[Archetype.UnlockType.REQUIRE_ATTRIBUTES].append(
                        attr.clone()
                    )
        if cls.required_races is not None and character_race not in cls.required_races:
            requires[Archetype.UnlockType.REQUIRE_ATTRIBUTES] = cls.required_races
        if cls.required_archetypes is not None:
            for req_archetype in cls.required_archetypes:
                if req_archetype.get_name() not in character_archetype_names:
                    requires[Archetype.UnlockType.REQUIRE_ARCHETYPES].append(
                        req_archetype
                    )
        requires = {key: value for key, value in requires.items() if value}
        if requires:
            return (
                False,
                requires,
            )
        return True, {}

    @classmethod
    def get_lineage(cls):
        return cls.lineage

    def __str__(self):
        return f"{self.get_name()}({self.get_lineage()})"

    def __eq__(self, other):
        return self.get_name() == other.get_name()


class Mob(Archetype):
    required_attributes = None
    required_races = None
    required_archetypes = None


class Player(Archetype):
    required_attributes = None
    required_races = None
    required_archetypes = None


# Require specific conditions to be unlocked:
# - Pre-archetypes
# - Enough base attributes (core like Insight, etc) (Common attributes OR its own attribute like swordman-sword mastery, both very hard to increase since the character is created, by using extremely rare resource))
# - Match character infomation (race, etc)

# Can learn multiple archetypes, take ALL effects (or primary and support archetype)
# But can improve only one archetype at a time
# Need to complete specific trials or consume specific item/resource to be significantly improve the archetype
# Combinations of archetypes
