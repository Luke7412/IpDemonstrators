from enum import IntEnum
from typing import Tuple

from .axi import Bus
from .module import Module


################################################################################
class FrequencyCounter(Module):
    class Registers(IntEnum):
        ModuleId = 0x00
        DivSel = 0x04
        Status = 0x08

    def __init__(self, bus: Bus):
        super().__init__(bus)

    def get_module_id(self) -> int:
        return self.bus.read_i32(self.Registers.ModuleId)

    def set_div(self, div) -> None:
        if div not in range(1,4):
            return
        self.bus.write_i32(self.Registers.DivSel, div)

    def get_frequency(self) -> Tuple[int, int, int]:
        value = self.bus.read_i32(self.Registers.Status)
        freq_cnt = value & 0xFFFF
        overflow = value >> 16 & 0x1
        updated = value >> 17 & 0x1
        return freq_cnt, overflow, updated


