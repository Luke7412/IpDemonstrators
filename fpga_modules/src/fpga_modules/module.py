from abc import ABC, abstractmethod
from enum import IntEnum

from .axi import Bus


################################################################################
class Module(ABC):
    @abstractmethod
    class Registers(IntEnum):
        pass

    def __init__(self, bus: Bus):
        self.bus = bus


