from enum import IntEnum

from .axi import Bus
from .module import Module


################################################################################
class BackgroundPattern (IntEnum):
    PASSTHROUGH              = 0x00
    HORIZONTAL_RAMP          = 0x01
    VERTIAL_RAMP             = 0x02
    TEMPORAL_RAMP            = 0x03
    SOLID_RED                = 0x04
    SOLID_GREEN              = 0x05
    SOLID_BLUE               = 0x06
    SOLID_BLACK              = 0x07
    SOLID_WHITE              = 0x08
    COLOR_BARS               = 0x09
    ZONE_PLATE               = 0x0A
    TARTAN_COLOR_BARS        = 0x0B
    CROSS_HATCH              = 0x0C
    COLOR_SWEEP              = 0x0D
    DIAGONAL_RAMP            = 0x0E
    CHECKERBOARD             = 0x0F
    PRBS                     = 0x10
    DISPLAYPORT_COLOR_RAMP   = 0x11
    DISPLAYPORT_STRIPES      = 0x12
    DISPLAYPORT_COLOR_SQUARE = 0x13


class Overlay (IntEnum):
    NONE        = 0x0
    MOVING_BOX  = 0x1
    CROSS_HAIRS = 0x2


class ColorMask (IntEnum):
    NONE  = 0x0
    RED   = 0x1
    GREEN = 0x2
    BLUE  = 0x3


class ColorFormat (IntEnum):
    RGB    = 0x0
    YUV444 = 0x1
    YUV422 = 0x2
    YUV420 = 0x3



class VideoTGP(Module):
    class Registers(IntEnum):
        Control                          = 0x0000
        Global_Interrupt_Enable          = 0x0004
        Ip_Interrupt_Enable_Register     = 0x0010
        Ip_Interrupt_Status_Register     = 0x0014
        Active_height                    = 0x0010
        Active_width                     = 0x0018
        Background_pattern_ID            = 0x0020
        Overlay_ID                       = 0x0028
        Mask_ID                          = 0x0030
        Motion_speed                     = 0x0038   # [7:0]
        Color_format                     = 0x0040
        Cross_hair_horizontal            = 0x0048
        Cross_hair_vertical              = 0x0050
        zplate_horizontal_starting_point = 0x0058
        zplate_horizontal_delta          = 0x0060
        zplate_vertical_starting_point   = 0x0068
        zplate_vertical_delta            = 0x0070
        Box_size                         = 0x0078
        Box_Color_R_and_Y                = 0x0080
        Box_Color_G_and_U                = 0x0088
        Box_Color_B_and_V                = 0x0090
        Enable_input                     = 0x0098
        Pass_through_left_boundary       = 0x00A0
        Pass_through_right_boundary      = 0x00A8
        Pass_through_upper_boundary      = 0x00B0
        Pass_through_lower_boundary      = 0x00B8
        Display_port_dynamic_change      = 0x00C0
        Display_port_YUV_coefficients    = 0x00C8
        Field_ID                         = 0x00D0
        Back_Motion_Enable               = 0x00D8

    def __init__(self, bus: Bus):
        super().__init__(bus)

    def configure_size(self, height, width):
        self.bus.write_i32(self.Registers.Active_height, height)
        self.bus.write_i32(self.Registers.Active_width, width)

    def set_background(self, pattern:BackgroundPattern):
        self.bus.write_i32(self.Registers.Background_pattern_ID, pattern)

    def set_overlay(self, overlay:Overlay):
        self.bus.write_i32(self.Registers.Overlay_ID, overlay)

    def set_color_mask(self, mask:ColorMask):
        self.bus.write_i32(self.Registers.Mask_ID, mask)

    def set_motion_speed(self, speed):
        speed = max(speed, 255)
        self.bus.write_i32(self.Registers.Motion_speed, speed)

    def set_color_format(self, color_format:ColorFormat):
        self.bus.write_i32(self.Registers.Color_format, color_format)

    def set_cross_hair(self, horizontal:int, vertical:int):
        self.bus.write_i32(self.Registers.Cross_hair_horizontal, horizontal)
        self.bus.write_i32(self.Registers.Cross_hair_vertical, vertical)
        self.set_overlay(Overlay.CROSS_HAIRS)

    def configure_box(self, size:int, r_y:int, g_u:int, b_v:int):
        self.bus.write_i32(self.Registers.Box_size, size)
        self.bus.write_i32(self.Registers.Box_Color_R_and_Y, r_y)
        self.bus.write_i32(self.Registers.Box_Color_G_and_U, g_u)
        self.bus.write_i32(self.Registers.Box_Color_B_and_V, b_v)
        self.set_overlay(Overlay.MOVING_BOX)

    def configure_pass_through(self, left:int, right:int, upper:int, lower:int):
        self.bus.write_i32(self.Registers.Pass_through_left_boundary, left)
        self.bus.write_i32(self.Registers.Pass_through_right_boundary, right)
        self.bus.write_i32(self.Registers.Pass_through_upper_boundary, upper)
        self.bus.write_i32(self.Registers.Pass_through_lower_boundary, lower)

    def start(self, auto_restart:bool=False):
        ctrl = 1    #start
        ctrl |= auto_restart << 7
        self.bus.write_i32(self.Registers.Control, ctrl)

    def stop(self):
        self.bus.write_i32(self.Registers.Control, 0)

    

 