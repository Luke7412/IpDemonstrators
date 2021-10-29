
from abc import ABC, abstractmethod

from modules.axi import Bus, StubBus
from enum import IntEnum


class Module(ABC):
    @abstractmethod
    class Registers(IntEnum):
        pass

    def __init__(self, bus: Bus):
        self.bus = bus


