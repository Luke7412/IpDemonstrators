from enum import IntEnum
from typing import Tuple
from time import sleep

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
        self.div = None

    def get_module_id(self) -> int:
        return self.bus.read_i32(self.Registers.ModuleId)

    def set_div(self, div) -> None:
        if div not in range(0, 6):
            return
        self.bus.write_i32(self.Registers.DivSel, div)
        self.div = div

    def get_div(self) -> int:
        self.div = self.bus.read_i32(self.Registers.DivSel)
        return self.div

    def get_frequency(self) -> Tuple[float, bool, bool]:
        if self.div is None:
            self.get_div()

        for i in range(2):
            freq_cnt, overflow, updated = self.get_next_value()
            if updated:
                break
            sleep(1e-6 * 2**(4*self.div))

        freq = freq_cnt/(0.000001 * 2**(4*self.div))
        return freq, overflow, updated

    def get_next_value(self) -> Tuple[int, bool, bool]:
        value = self.bus.read_i32(self.Registers.Status)
        freq_cnt = value & 0xFFFF
        overflow = value >> 16 & 0x1
        updated = value >> 17 & 0x1
        return freq_cnt, bool(overflow), bool(updated)
