from enum import IntEnum
from dataclasses import dataclass

from .axi import Bus
from .module import Module


################################################################################
@dataclass
class VGA_Config:
    index : int
    h_res: int
    h_front_porch: int
    h_sync_pulse: int
    h_back_porch: int
    v_res: int
    v_front_porch: int
    v_sync_pulse: int
    v_back_porch: int
    pix_clk: float

vga_configs = {
   "640x350p70": VGA_Config (
        index = 0,
        h_res = 640,
        h_front_porch = 16,
        h_sync_pulse = 96,
        h_back_porch = 48,
        v_res = 350,
        v_front_porch = 37,
        v_sync_pulse = 2,
        v_back_porch = 60,
        pix_clk = 25.175e6
    ),
    "640x400p60": VGA_Config (
        index = 1,
        h_res = 640,
        h_front_porch = 16,
        h_sync_pulse = 96,
        h_back_porch = 48,
        v_res = 400,
        v_front_porch = 12,
        v_sync_pulse = 2,
        v_back_porch = 35,
        pix_clk = 25.175e6
    ),
    "640x480p60": VGA_Config (
        index = 2,
        h_res = 640,
        h_front_porch = 16,
        h_sync_pulse = 96,
        h_back_porch = 48,
        v_res = 480,
        v_front_porch = 10,
        v_sync_pulse = 2,
        v_back_porch = 33,
        pix_clk = 25.175e6
    ),
    "800x600p60": VGA_Config (
        index = 3,
        h_res = 800,
        h_front_porch = 40,
        h_sync_pulse = 128,
        h_back_porch = 88,
        v_res = 600,
        v_front_porch = 1,
        v_sync_pulse = 4,
        v_back_porch = 23,
        pix_clk = 40.000e6
    ),
    "1024x768p60": VGA_Config (
        index = 4,
        h_res = 1024,
        h_front_porch = 24,
        h_sync_pulse = 136,
        h_back_porch = 160,
        v_res = 768,
        v_front_porch = 3,
        v_sync_pulse = 6,
        v_back_porch = 29,
        pix_clk = 65.000e6
    ),
    "1280x1024p60": VGA_Config (
        index = 5,
        h_res = 1280,
        h_front_porch = 48,
        h_sync_pulse = 112,
        h_back_porch = 248,
        v_res = 1024,
        v_front_porch = 1,
        v_sync_pulse = 3,
        v_back_porch = 39,
        pix_clk = 108.000e6
    )
  }


class VGA(Module):
    class Registers(IntEnum):
      ModuleId = 0x000
      enable = 0x004
      h_res = 0x010
      h_front_porch = 0x014
      h_sync_pulse = 0x018
      h_back_porch = 0x01C
      v_res = 0x020
      v_front_porch = 0x024
      v_sync_pulse = 0x028
      v_back_porch = 0x02C

    def __init__(self, bus: Bus):
        super().__init__(bus)

    def get_module_id(self) -> int:
        return self.bus.read_i32(self.Registers.ModuleId)

    def enable(self, div) -> None:
        self.bus.write_i32(self.Registers.enable, 1)

    def disable(self, div) -> None:
        self.bus.write_i32(self.Registers.enable, 0)

    def set_config(self, name:str):
        config = vga_configs[name]
        self.bus.write_i32(self.Registers.h_res, config.h_res)
        self.bus.write_i32(self.Registers.h_front_porch, config.h_front_porch)
        self.bus.write_i32(self.Registers.h_sync_pulse, config.h_sync_pulse)
        self.bus.write_i32(self.Registers.h_back_porch, config.h_back_porch)
        self.bus.write_i32(self.Registers.v_res, config.v_res)
        self.bus.write_i32(self.Registers.v_front_porch, config.v_front_porch)
        self.bus.write_i32(self.Registers.v_sync_pulse, config.v_sync_pulse)
        self.bus.write_i32(self.Registers.v_back_porch, config.v_back_porch)
  

  
                          