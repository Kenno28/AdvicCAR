from enum import Enum

class Makes(Enum):
    """Enumerates all supported vehicle manufacturers used in the project."""
    AUDI = 0


class Models(Enum):
    """Enumerates all supported vehicle models currently available in the project."""
    A7 = 0

class FuelType(Enum):
    """Enumerates the supported fuel categories for a vehicle."""

    DIESEL = 0
    GASOLINE = 1
    HYBRID = 2
    OTHER = 3

class MotorType(Enum):
    """Enumerates the supported motor categories for a vehicle."""

    # Diesel
    TDI_40 = 0
    TDI_45 = 1
    TDI_50 = 2

    # Gasoline
    TFSI_45 = 3
    TFSI_55 = 4

    # Hybrid
    TFSI_55_e_quattro = 5


