from enum import IntEnum
from typing import List

from .axi import Bus
from .module import Module


################################################################################
class BRAM(Module):
    class Registers(IntEnum):
        ...

    def __init__(self, bus: Bus):
        super().__init__(bus)

    def read(self, address: int, length: int) -> List[int]:
        return self.bus.read(address, length)

    def write(self, address: int, data: List[int]) -> None:
        self.bus.write(address, data)
