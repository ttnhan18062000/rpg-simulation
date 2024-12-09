from components.attribute.attribute import Attribute

from data.logs.logger import logger


class CharacterAttribute:
    def __init__(self, base_attrs=None):
        # base_attrs = {attr_name: attr}
        # additional_attrs = {source.get_name(): attr}
        if base_attrs:
            self.base_attrs = base_attrs
        else:
            self.base_attrs = {}
        self.additional_attrs = {}

    def get_base_attrs(self):
        return self.base_attrs

    def get_base_attr(self, attr_name: str) -> Attribute:
        if attr_name not in self.base_attrs:
            raise Exception(
                f"Attribute {attr_name} not found in base attr {list(self.base_attrs.keys())}"
            )
        return self.base_attrs[attr_name]

    def modify_cap(self, attr_name: str, value: int):
        self.get_base_attr(attr_name).modify_cap(value)

    def modify_caps(self, attr_name_to_value):
        for attr_name, value in attr_name_to_value.items():
            self.modify_cap(attr_name, value)

    # Return a dictionary attr_name: cap_value
    def get_caps(self):
        return {
            attr_name: attr.get_cap() for attr_name, attr in self.base_attrs.items()
        }

    def get_info(self):
        return {
            attr_name: f"{attr.get_value()}/{attr.get_cap()}"
            for attr_name, attr in self.base_attrs.items()
        }

    def get_final_attributes(self):
        final_attrs = {}
        for attr_name, base_attr in self.base_attrs.items():
            final_attrs[attr_name] = base_attr.clone()

        for additional_attr in self.additional_attrs.values():
            additional_attr_name = additional_attr.get_name()
            if additional_attr_name in final_attrs:
                final_attrs[additional_attr_name] += additional_attr
            else:
                final_attrs[additional_attr_name] = additional_attr.clone()

        return final_attrs

    def add_base_attribute(self, attr: Attribute):
        attr_name = attr.get_name()
        if attr_name in self.base_attrs:
            logger.debug(f"Overide the base {self.base_attrs[attr_name]} with {attr}")
        self.base_attrs[attr_name] = attr
        self.on_attribute_change()

    def modify_base_attribute(self, attr: str, value: int):
        if isinstance(attr, str):
            self.base_attrs[attr].modify_value(value)
        else:
            self.base_attrs[attr.get_name()].modify_value(value)
        self.on_attribute_change()

    # attr_identity is often the name of the attribute modification source
    def add_additional_attribute(self, attr_identity: str, attr: Attribute):
        if attr_identity in self.additional_attrs:
            self.additional_attrs[attr_identity] = attr
            logger.debug(f"Override the attribute effect from {attr_identity}: {attr}")
        else:
            self.additional_attrs[attr_identity] = attr
            logger.debug(f"Add the attribute effect from {attr_identity}: {attr}")
        self.on_attribute_change()

    # attr_identity is often the name of the attribute modification source
    def remove_additional_attribute(self, attr_identity: str):
        if attr_identity in self.additional_attrs:
            logger.debug(
                f"Removing the attribute {self.additional_attrs[attr_identity]} affected by {attr_identity}"
            )
            self.additional_attrs.pop(attr_identity)
        else:
            logger.debug(f"Cannot find the attribute affected by {attr_identity}")
        self.on_attribute_change()

    # TODO: This should placed in the character class, since we don't need to pass the character to every function above
    def on_attribute_change(self):
        # TODO: Update the total affect or optimization (update latest change attr only)on the character
        pass

    def __str__(self):
        return " | ".join(
            [f"{attr}" for attr_name, attr in self.get_base_attrs().items()]
        )
