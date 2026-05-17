from enum import Enum
from eytelwein.main.units import get_unit_registry

# Use the centralized UnitRegistry singleton
unit_reg = get_unit_registry()


class PulleyGroups(Enum):
    A = 1
    B = 2
    C = 3

    def to_int(self) -> int:
        return self.value

    @classmethod
    def from_string(self, string: str):
        if string.lower() == "a":
            return self.A
        elif string.lower() == "b":
            return self.B
        elif string.lower() == "c":
            return self.C
        else:
            raise ValueError("Invalid string for PulleyGroups.")


class MinimumPulleyDiameterCoefficient(Enum):
    B = 80
    P = 90
    E = 108
    St = 145

    def to_int(self) -> int:
        return self.value

    @classmethod
    def from_string(self, string: str):
        if string.lower() == "b" or string.lower() == "cotton":
            return self.B
        elif string.lower() == "p" or string.lower() == "polyamide":
            return self.P
        elif string.lower() == "e" or string.lower() == "polyester":
            return self.E
        elif (
            string.lower() == "st"
            or string.lower() == "steel"
            or string.lower() == "steel cords"
            or string.lower() == "steel cord"
            or string.lower() == "steel_cord"
            or string.lower() == "steel_cords"
            or string.lower() == "steelcord"
        ):
            return self.St
        else:
            raise ValueError("Invalid string for MinimumPulleyDiameterCoefficient.")


class PulleyLoadFactor(Enum):
    above_100 = "above_100"
    above_60_up_to_100 = "above_60_up_to_100"
    above_30_up_to_60 = "above_30_up_to_60"
    up_to_30 = "up_to_30"

    def __str__(self):
        return self.value

    @classmethod
    def from_percent_value(self, value: float):
        if value > 100:
            return self.above_100
        elif value > 60:
            return self.above_60_up_to_100
        elif value > 30:
            return self.above_30_up_to_60
        else:
            return self.up_to_30

    def get_max_value(self):
        if self == PulleyLoadFactor.above_100:
            return 140
        elif self == PulleyLoadFactor.above_60_up_to_100:
            return 100
        elif self == PulleyLoadFactor.above_30_up_to_60:
            return 60
        elif self == PulleyLoadFactor.up_to_30:
            return 30
        else:
            raise ValueError("Invalid PulleyLoadFactor")


class IdlerSets(Enum):
    FLAT_TROUGH = 1
    V_TROUGH = 2
    THREE_TROUGH = 3
    DEEP_TROUGH = 4
    FIVE_TROUGH = 5

    def to_int(self) -> int:
        return self.value


class BeltCoverCharacteristicsAssessments(Enum):
    FAVOURABLE = 1
    AVERAGE = 2
    UNFAVOURABLE = 3

    def to_int(self) -> int:
        return self.value

    @classmethod
    def from_string(self, string: str):
        if (
            string.lower() == "favourable"
            or string.lower() == "fav"
            or string.lower() == "f"
        ):
            return self.FAVOURABLE
        elif (
            string.lower() == "average"
            or string.lower() == "avg"
            or string.lower() == "a"
        ):
            return self.AVERAGE
        elif (
            string.lower() == "unfavourable"
            or string.lower() == "unfav"
            or string.lower() == "unf"
            or string.lower() == "u"
        ):
            return self.UNFAVOURABLE
        else:
            raise ValueError("Invalid string for BeltCoverCharacteristicsAssessments.")

    @classmethod
    def from_int(self, integer: int):
        if integer == 1:
            return self.FAVOURABLE
        elif integer == 2:
            return self.AVERAGE
        elif integer == 3:
            return self.UNFAVOURABLE
        else:
            raise ValueError("Invalid integer for BeltCoverCharacteristicsAssessments.")


class CoefficientMinimumTransitionLength(Enum):
    EP = 8.5
    ST = 14


class BeltCarcassType(Enum):
    TEXTILE = 1
    STEEL_CORD = 2

    @classmethod
    def from_string(cls, string):
        if (
            string.lower() == "textile"
            or string.lower() == "fabric"
            or string.lower() == "ep"
        ):
            return cls.TEXTILE
        elif (
            string.lower() == "steel cord"
            or string.lower() == "steel-cord"
            or string.lower() == "steelcord"
            or string.lower() == "steel"
            or string.lower() == "st"
            or string.lower() == "steel_cord"
        ):
            return cls.STEEL_CORD
        else:
            raise ValueError("Invalid string for BeltCarcassType.")

    # Add a string method for better representation
    def __str__(self):
        if self == BeltCarcassType.TEXTILE:
            return "Textile"
        elif self == BeltCarcassType.STEEL_CORD:
            return "Steel Cord"
        else:
            raise ValueError("Invalid BeltCarcassType.")
