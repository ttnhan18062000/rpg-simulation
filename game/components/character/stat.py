from enum import Enum


class Stat:
    def __init__(self, value) -> None:
        self.value = value

    def set(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        return self.value


class NumericalStat(Stat):
    numerical_type_key = "numerical_type"

    class NumericalType(Enum):
        REAL = 1
        PERCENTAGE = 2

    def __init__(self, value, **kwargs) -> None:
        super().__init__(value)
        if NumericalStat.numerical_type_key in kwargs:
            numerical_type = kwargs.get(NumericalStat.numerical_type_key)
            if not isinstance(numerical_type, NumericalStat.NumericalType):
                raise Exception(
                    f"Failed creating a NumericalStat, provided wrong NumericalType, receive type '{numerical_type.__class__.__name__}'"
                )
            self.numerical_type = numerical_type
        else:
            self.numerical_type = NumericalStat.NumericalType.REAL

    def __sub__(self, other: "NumericalStat"):
        if isinstance(other, NumericalStat):
            if self.numerical_type != other.numerical_type:
                raise Exception(f"NumericalType need to be the same to use subtraction")
            return NumericalStat(self.value - other.value)
        return NotImplemented

    def __add__(self, other: "NumericalStat"):
        if isinstance(other, NumericalStat):
            if self.numerical_type != other.numerical_type:
                raise Exception(f"NumericalType need to be the same to use addition")
            return NumericalStat(self.value + other.value)
        return NotImplemented

    def __str__(self):
        return f"{self.value}{'%' if self.numerical_type is NumericalStat.NumericalType.PERCENTAGE else ''}"

    def modify(self, other: "NumericalStat"):
        if other.numerical_type is NumericalStat.NumericalType.REAL:
            self.value += other.value
        elif other.numerical_type is NumericalStat.NumericalType.PERCENTAGE:
            self.value += self.value * other.value

    def modify_with_value(self, value, numerical_type: "NumericalStat.NumericalType"):
        if numerical_type is NumericalStat.NumericalType.REAL:
            self.value += value
        elif numerical_type is NumericalStat.NumericalType.PERCENTAGE:
            self.value += self.value * value

    def clone(self):
        return NumericalStat(
            self.value, **{NumericalStat.numerical_type_key: self.numerical_type}
        )


class CategoricalStat(Stat):
    pass
