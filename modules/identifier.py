from enum import IntEnum
from typing import Tuple

from .axi import Bus
from .module import Module


################################################################################
from enum import Enum
# from collections import namedtuple
#
# Color = namedtuple('Color', ['value', 'displayString'])
#
# class Register:



class Identifier(Module):
    class Registers(IntEnum):
        ModuleId = 0x00
        Name = 0x04
        Version = 0x14

    def __init__(self, bus: Bus):
        super().__init__(bus)

    def get_module_id(self) -> int:
        return self.bus.read_i32(self.Registers.ModuleId)

    def get_name(self) -> str:
        bytes = self.bus.read(self.Registers.Name, 16)
        quads = [reversed(bytes[4*i:4*(i+1)]) for i in range(4)]
        bytes = [x for quad in quads for x in quad]
        bytes = [x for x in bytes if x != 0]
        return ''.join([chr(x) for x in bytes]).strip()

    def get_version(self) -> Tuple[int, int]:
        value = self.bus.read_i32(self.Registers.Version)
        major_version = value >> 16 & 0xFFFF
        minor_version = value >> 0 & 0xFFFF
        return major_version, minor_version

