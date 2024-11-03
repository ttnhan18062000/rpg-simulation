class Stat:
    def __init__(self, value) -> None:
        self.value = value

    def assign(self, value):
        self.value = value


class NumericalStat(Stat):

    def __sub__(self, other):
        if isinstance(other, NumericalStat):
            return NumericalStat(self.value - other.value)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, NumericalStat):
            return NumericalStat(self.value + other.value)
        return NotImplemented


class CategoricalStat(Stat):
    pass
