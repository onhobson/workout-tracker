from enum import Enum


class MuscleRole(str, Enum):
    primary = "primary"
    secondary = "secondary"
    stabilizer = "stabilizer"


class InputMode(str, Enum):
    single = "single"
    double = "double"
    barbell = "barbell"
    band = "band"
