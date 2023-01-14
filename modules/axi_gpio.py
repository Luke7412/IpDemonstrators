from enum import IntEnum
from typing import List
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
    
    #example of gpiobits fields that are used by set_field and get_field functions
    #GPIOBITS = {
    ##         gpiobank, bitrange
    #'sys_id': [0, [2,0], "r"],
    #'sys_type': [0, [6,4], "r"],
    #'retimer_reset': [0, 8, "rw"],
    #'sensor_ldo_en:': [0, 9, "rw"],
    #'mod_reset:': [0, 10, "rw"],
    #'mod_prog:': [0, 11, "rw"],
    #'mod_por:': [0, 12, "rw"],
    #'mod_srst:': [0, 13, "rw"],
    #'pll_lol': [0, 14, "r"],
    #'pll_sel': [0, [16,15], "w"],
    #'pll_rst:': [0, 17, "w"],
    #'pll_finc:': [0, 18, "w"],
    #'pll_fdec:': [0, 19, "w"],
    #'pxi_wake:': [0, 20, "w"],
    #'build_version_low:': [0, [23,16], "r"],
    #'build_version_high:': [0, [31,24], "r"],
    #}

    def __init__(self, bus):
        super().__init__(bus)
        self.gpio_width = 32
        self.gpio2_width = 32

    def set_gpio_field(self, field:List, value:int, tri_value:int=0) -> None:
        gpio_bank = field[0]
        bits = field[1]
        access = field[2]

        if access == "r":
            print("Field is read only!")
            return

        if type(bits) is list:
            shift = bits[1]
            size = 2**(bits[0]-bits[1]+1)-1
        else:
            shift = bits
            size = 1

        mask = size << shift
        
        if gpio_bank > 0:
            data_address = self.Registers.gpio2_data
            tri_address = self.Registers.gpio2_tri
        else:
            data_address = self.Registers.gpio_data
            tri_address = self.Registers.gpio_tri
        
        prev_data = self.bus.read_i32(data_address)
        new_data = prev_data & (~mask & 0xFFFFFFFF)
        new_data = new_data + ((value & size) << shift)
        self.bus.write_i32(data_address, new_data)
        
        prev_tri = self.bus.read_i32(tri_address)
        new_tri = prev_tri & (~mask & 0xFFFFFFFF)
        new_tri = new_tri + ((tri_value & size) << shift)
        self.bus.write_i32(tri_address, new_tri)
        
    def get_gpio_field(self, field:List) -> int:
        gpio_bank = field[0]
        bits = field[1]
        access = field[2]
        
        if access == "w":
            print("Field is write only!")
            return
        
        if type(bits) is list:
            shift = bits[1]
            size = 2**((bits[0]-bits[1])+1)-1
        else:
            shift = bits
            size = 1
        
        mask = size << shift
        
        if gpio_bank > 0:
            address = self.Registers.gpio2_data
        else:
            address = self.Registers.gpio_data
            
        register_data = self.bus.read_i32(address)
        field_data = (register_data & mask) >> shift
        
        return field_data

    def set_tristate(self, channel:int, value:int) -> None:
        """
            Set GPIO Tristate
            Configure the ports dynamically as input or output: 
              - When a bit within this register is set, the corresponding I/O port is configured as an input port. 
              - When a bit is cleared, the corresponding I/O port is configured as an output port.
            :param int channel: 0 - gpio_tri; 1 - gpio2_tri
            :param int value:   tristate word (32 bit wide)
        """
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
        """
            Read GPIO Tristate
            Read the ports tristate status: 
              - When a bit within this register is set, the corresponding I/O port is configured as an input port. 
              - When a bit is cleared, the corresponding I/O port is configured as an output port.
            channel = 0: gpio_tri; 1: gpio2_tri
        """
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

    def write(self, channel:int, tristate_value:int, gpio_value:int) -> None:
        """
            Write GPIO Data
            The AXI GPIO data register is used to write to the general purpose output ports. 
            When a port is configured as input, writing to the AXI GPIO data register has no effect.
            channel        = 0: gpio_data; 1: gpio2_data
            tristate_value = tristate word (32 bit wide)
            gpio_value     = gpio data word (32 bit wide)
        """
        # 1. Set tristate
        self.set_tristate(channel, tristate_value)

        # 2. Set gpio
        if channel == 0:
            # write to gpio_data
            self.bus.write_i32(self.Registers.gpio_data, gpio_value)
        elif channel == 1:
            # write to gpio2_data
            self.bus.write_i32(self.Registers.gpio2_data, gpio_value)
        else:
            raise ValueError(
                "Wrong channel selected. Please select between channel '0' or '1'.")

    def read(self, channel:int, tristate_value:int) -> int:
        """
            Read GPIO Data
            The AXI GPIO data register is used to read from the general purpose input ports. 
            When a port is configured as output, reading from the AXI GPIO data register always returns zeros.
            channel        = 0: gpio_data; 1: gpio2_data
            tristate_value = tri-state word (32 bit wide)
        """
        # 1. Set tri-state
        self.set_tristate(channel, tristate_value)

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

    def reset(self, channel:int) -> None:
        """
            Reset AXI GPIO to default values
        """
        default_gpio_val = 0x00000000
        default_tristate_val = 0xFFFFFFFF

        self.set_tristate(channel, 0)
        self.write(channel, default_tristate_val, default_gpio_val)
