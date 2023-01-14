from enum import IntEnum
from typing import Tuple

from .axi import Bus
from .module import Module


################################################################################
class AxiTimer(Module):
    class Registers(IntEnum):
        TCSR0 = 0x00
        TLR0 = 0x04
        TCR0 = 0x08
        TCSR1 = 0x10
        TLR1 = 0x14
        TCR1 = 0x18

    def __init__(self, bus: Bus):
        super().__init__(bus)

    def get_module_id(self) -> int:
        return self.bus.read_i32(self.Registers.ModuleId)

    def get_name(self) -> str:
        print([chr(x) for x in self.bus.read(self.Registers.Name, 16)])
        return ''.join([chr(x) for x in self.bus.read(self.Registers.Name, 16)])

    def get_version(self) -> Tuple[int, int]:
        value = self.bus.read_i32(self.Registers.Version)
        major_version = value >> 16 & 0xFFFF
        minor_version = value >> 0 & 0xFFFF
        return major_version, minor_version

