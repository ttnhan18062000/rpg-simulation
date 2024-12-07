from components.item.equipment import Equipment, EquipmentType


from data.logs.logger import logger


class CharacterEquipment:
    def __init__(self) -> None:
        self.weapon: Equipment = None
        self.armor: Equipment = None

    def get_weapon(self):
        return self.weapon

    def get_armor(self):
        return self.armor

    def equip(self, equipment: Equipment):
        if equipment.get_equipment_type() is EquipmentType.WEAPON:
            self.equip_weapon(equipment)
        elif equipment.get_equipment_type() is EquipmentType.ARMOR:
            self.equip_armor(equipment)

    def equip_weapon(self, weapon: Equipment):
        self.weapon = weapon

    def equip_armor(self, armor: Equipment):
        self.armor = armor

    def __str__(self):
        weapon_name = self.weapon.get_name() if self.weapon else ""
        armor_name = self.armor.get_name() if self.armor else ""
        return f"Weapon: {weapon_name} | Armor: {armor_name}"
