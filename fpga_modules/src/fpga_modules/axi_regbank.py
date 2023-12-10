from enum import IntEnum

from .axi import Bus
from .module import Module


################################################################################
class AxiRegbank(Module):
    class Registers(IntEnum):
        ...

    def __init__(self, bus: Bus):
        super().__init__(bus)

    def get_reg_in(self, index: int) -> int:
        return self.bus.read_i32(8*index)

    def get_reg_out(self, index: int) -> int:
        return self.bus.read_i32(8*index+4)

    def set_reg_out(self, index: int, value: int) -> None:
        self.bus.write_i32(8*index+4, value)
