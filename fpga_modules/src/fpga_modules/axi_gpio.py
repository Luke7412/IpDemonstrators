from enum import IntEnum
from .module import Module


class AxiGpio(Module):
    class Registers(IntEnum):
        gpio_data =  0x0000     # R/W   | Channel 1 AXI GPIO Data Register
        gpio_tri =   0x0004     # R/W   | Channel 1 AXI GPIO 3-state Control Register
        gpio2_data = 0x0008     # R/W   | Channel 2 AXI GPIO Data Register (not available)
        gpio2_tri =  0x000C     # R/W   | Channel 2 AXI GPIO 3-state Control Register (not available)
        gier =       0x011C     # R/W   | Global Interrupt Enable Register (not available)
        ip_ier =     0x0128     # R/W   | IP Interrupt Enable Register (not available)
        ip_isr =     0x0120     # R/TOW | IP Interrupt Status Register (not available)
    
    def __init__(self, bus):
        super().__init__(bus)
        self.gpio_width = 32
        self.gpio2_width = 32

    def reset(self, channel:int) -> None:
        default_gpio_val = 0x00000000
        default_tristate_val = 0xFFFFFFFF
        self.set_tristate(channel, default_tristate_val)
        self.write(channel, default_gpio_val)

    def set_tristate(self, channel:int, value:int) -> None:
        if channel == 0:
            # write to gpio_tri
            self.bus.write_i32(self.Registers.gpio_tri, value)
        elif channel == 1:
            # write to gpio2_tri
            self.bus.write_i32(self.Registers.gpio2_tri, value)
        else:
            raise ValueError(
                "Wrong channel selected. Please select between channel '0' or '1'.")

    def read_tristate(self, channel:int) -> int:
        if channel == 0:
            # read from gpio_tri
            value = self.bus.read_i32(self.Registers.gpio_tri)
        elif channel == 1:
            # read from gpio2_tri
            value = self.bus.read_i32(self.Registers.gpio2_tri)
        else:
            raise ValueError(
                "Wrong channel selected. Please select between channel '0' or '1'.")
        return value

    def write(self, channel:int, value:int) -> None:
        # 2. Set gpio
        if channel == 0:
            # write to gpio_data
            self.bus.write_i32(self.Registers.gpio_data, value)
        elif channel == 1:
            # write to gpio2_data
            self.bus.write_i32(self.Registers.gpio2_data, value)
        else:
            raise ValueError(
                "Wrong channel selected. Please select between channel '0' or '1'.")

    def read(self, channel:int) -> int:
        # 2. Read gpio
        if channel == 0:
            # read from gpio_data
            value = self.bus.read_i32(self.Registers.gpio_data)
        elif channel == 1:
            # read from gpio2_data
            value = self.bus.read_i32(self.Registers.gpio2_data)
        else:
            raise ValueError(
                "Wrong channel selected. Please select between channel '0' or '1'.")

        return value
