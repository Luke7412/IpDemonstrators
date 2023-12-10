from enum import IntEnum
from .module import Module

from dataclasses import dataclass
from math import ceil, floor


################################################################################
@dataclass
class TimingLimits:
    f_in_min:  float
    f_in_max:  float
    f_pfd_min: float
    f_pfd_max: float
    f_vco_min: float
    f_vco_max: float
    f_out_min: float
    f_out_max: float


@dataclass
class ParamLimits:
    d_min: int
    d_max: int
    o_min: int
    o_max: int
    m_min: int
    m_max: int


class Limits(TimingLimits, ParamLimits):
    def __init__(self, t:TimingLimits, p:ParamLimits):
        self.f_in_min = t.f_in_min
        self.f_in_max = t.f_in_max
        self.f_pfd_min = t.f_pfd_min
        self.f_pfd_max = t.f_pfd_max
        self.f_vco_min = t.f_vco_min
        self.f_vco_max = t.f_vco_max
        self.f_out_min = t.f_out_min
        self.f_out_max = t.f_out_max
        self.d_min = p.d_min
        self.d_max = p.d_max
        self.o_min = p.o_min
        self.o_max = p.o_max
        self.m_min = p.m_min
        self.m_max = p.m_max


limits = {
    'Artix7': {
        'PLL': {
            'param_limits': ParamLimits(d_min=1, d_max=56, m_min=2, m_max=64, o_min=1, o_max=128),
            'timing_limits': {
                '1.00v-3':      TimingLimits(f_in_min=19.00e6, f_in_max=800.00e6, f_vco_min=800.00e6, f_vco_max=2133.00e6, f_out_min=6.25e6, f_out_max=800.00e6, f_pfd_min=19.00e6, f_pfd_max=550.00e6),
                '1.00v-2/-2LE': TimingLimits(f_in_min=19.00e6, f_in_max=800.00e6, f_vco_min=800.00e6, f_vco_max=1866.00e6, f_out_min=6.25e6, f_out_max=800.00e6, f_pfd_min=19.00e6, f_pfd_max=500.00e6),
                '1.00v-1':      TimingLimits(f_in_min=19.00e6, f_in_max=800.00e6, f_vco_min=800.00e6, f_vco_max=1600.00e6, f_out_min=6.25e6, f_out_max=800.00e6, f_pfd_min=19.00e6, f_pfd_max=450.00e6),
                '0.95v-1LI':    TimingLimits(f_in_min=19.00e6, f_in_max=800.00e6, f_vco_min=800.00e6, f_vco_max=1600.00e6, f_out_min=6.25e6, f_out_max=800.00e6, f_pfd_min=19.00e6, f_pfd_max=450.00e6),
                '0.90v-2LE':    TimingLimits(f_in_min=19.00e6, f_in_max=800.00e6, f_vco_min=800.00e6, f_vco_max=1600.00e6, f_out_min=6.25e6, f_out_max=800.00e6, f_pfd_min=19.00e6, f_pfd_max=450.00e6),
        }},
        'MMCM': {
            'param_limits': ParamLimits(d_min=1, d_max=106, m_min=2, m_max=64, o_min=1, o_max=128),
            'timing_limits': {
                '1.00v-3':      TimingLimits(f_in_min=10.00e6, f_in_max=800.00e6, f_vco_min=600.00e6, f_vco_max=1600.00e6, f_out_min=4.69e6, f_out_max=800.00e6, f_pfd_min=10.00e6, f_pfd_max=550.00e6),
                '1.00v-2/-2LE': TimingLimits(f_in_min=10.00e6, f_in_max=800.00e6, f_vco_min=600.00e6, f_vco_max=1440.00e6, f_out_min=4.69e6, f_out_max=800.00e6, f_pfd_min=10.00e6, f_pfd_max=500.00e6),
                '1.00v-1':      TimingLimits(f_in_min=10.00e6, f_in_max=800.00e6, f_vco_min=600.00e6, f_vco_max=1200.00e6, f_out_min=4.69e6, f_out_max=800.00e6, f_pfd_min=10.00e6, f_pfd_max=450.00e6),
                '0.95v-1LI':    TimingLimits(f_in_min=10.00e6, f_in_max=800.00e6, f_vco_min=600.00e6, f_vco_max=1200.00e6, f_out_min=4.69e6, f_out_max=800.00e6, f_pfd_min=10.00e6, f_pfd_max=450.00e6),
                '0.90v-2LE':    TimingLimits(f_in_min=10.00e6, f_in_max=800.00e6, f_vco_min=600.00e6, f_vco_max=1200.00e6, f_out_min=4.69e6, f_out_max=800.00e6, f_pfd_min=10.00e6, f_pfd_max=450.00e6),
        }}
    },
    'Kintex7': {
        'PLL': {
            'param_limits': ParamLimits(d_min=1, d_max=56, m_min=2, m_max=64, o_min=1, o_max=128),
            'timing_limits': {
                '1.00v-3':      TimingLimits(f_in_min=19.00e6, f_in_max=1066.00e6, f_vco_min=800.00e6, f_vco_max=2133.00e6, f_out_min=6.25e6, f_out_max=1066.00e6, f_pfd_min=19.00e6, f_pfd_max=550.00e6),
                '1.00v-2/-2LE': TimingLimits(f_in_min=19.00e6, f_in_max=933.00e6, f_vco_min=800.00e6, f_vco_max=1866.00e6, f_out_min=6.25e6, f_out_max=933.00e6, f_pfd_min=19.00e6, f_pfd_max=500.00e6),
                '1.00v-1':      TimingLimits(f_in_min=19.00e6, f_in_max=800.00e6, f_vco_min=800.00e6, f_vco_max=1600.00e6, f_out_min=6.25e6, f_out_max=800.00e6, f_pfd_min=19.00e6, f_pfd_max=450.00e6),
                '1.00v-1M/-1LM':TimingLimits(f_in_min=19.00e6, f_in_max=800.00e6, f_vco_min=800.00e6, f_vco_max=1600.00e6, f_out_min=6.25e6, f_out_max=800.00e6, f_pfd_min=19.00e6, f_pfd_max=450.00e6),
                '0.95v-2LI':    TimingLimits(f_in_min=19.00e6, f_in_max=933.00e6, f_vco_min=800.00e6, f_vco_max=1866.00e6, f_out_min=6.25e6, f_out_max=933.00e6, f_pfd_min=19.00e6, f_pfd_max=500.00e6),
                '0.90v-2LE':    TimingLimits(f_in_min=19.00e6, f_in_max=800.00e6, f_vco_min=800.00e6, f_vco_max=1600.00e6, f_out_min=6.25e6, f_out_max=800.00e6, f_pfd_min=19.00e6, f_pfd_max=450.00e6),
        }}
    }
}


def get_limits(type: str, family:str, speed_grade:str):
    return Limits(
        t=limits[family][type]['timing_limits'][speed_grade],
        p=limits[family][type]['param_limits']
    )


################################################################################
class ClkWizard(Module):
    """
        Class to represent clk wizard IP (See PG065)
        Functionality depends on hardware config e.g.:phase control, clock monitoring, ...
    """
    class Registers(IntEnum):
        SRR =           0x000
        SR =            0x004
        ClkMonErrSts =  0x008
        ISR =           0x00C
        IER =           0x010
        ClkCfgReg0 =    0x200
        ClkCfgReg1 =    0x204
        ClkCfgReg2 =    0x208
        ClkCfgReg3 =    0x20C
        ClkCfgReg4 =    0x210
        ClkCfgReg5 =    0x214
        ClkCfgReg6 =    0x218
        ClkCfgReg7 =    0x21C
        ClkCfgReg8 =    0x220
        ClkCfgReg9 =    0x224
        ClkCfgReg10 =   0x228
        ClkCfgReg11 =   0x22C
        ClkCfgReg12 =   0x230
        ClkCfgReg13 =   0x234
        ClkCfgReg14 =   0x238
        ClkCfgReg15 =   0x23C
        ClkCfgReg16 =   0x240
        ClkCfgReg17 =   0x244
        ClkCfgReg18 =   0x248
        ClkCfgReg19 =   0x24C
        ClkCfgReg20 =   0x250
        ClkCfgReg21 =   0x254
        ClkCfgReg22 =   0x258
        ClkCfgReg23 =   0x25C
        #dynamic config regs, direct DRP copies
        PowerReg =      0x300
        Clkout0Reg1 =   0x304
        Clkout0Reg2 =   0x308
        Clkout1Reg1 =   0x30C
        Clkout1Reg2 =   0x310
        Clkout2Reg1 =   0x314
        Clkout2Reg2 =   0x318
        Clkout3Reg1 =   0x31C
        Clkout3Reg2 =   0x320
        Clkout4Reg1 =   0x324
        Clkout4Reg2 =   0x328
        Clkout5Reg1 =   0x32C
        Clkout5Reg2 =   0x330
        Clkout6Reg1 =   0x334
        Clkout6Reg2 =   0x338
        DivclkReg =     0x33C
        ClkFBoutReg1 =  0x340
        ClkFBoutReg2 =  0x344
        LockReg1 =      0x348
        LockReg2 =      0x34C
        LockReg3 =      0x350
        FilterReg1 =    0x354
        FilterReg2 =    0x358
        ClkCfgReg24 =   0x35C

    def __init__(self, bus, type:str, family:str, speed_grade:str):
        super().__init__(bus)
        self.limits = get_limits(type, family, speed_grade)

    def get_clk_status(self) -> dict:
        """
            Clock status dump, most registers only exists when clock monitoring is enabled.
            :return Dict: A dictionary containing the status
        """
        value = self.bus.read_i32(self.Registers.ClkMonErrSts)

        status = dict()
        status['locked'] = self.get_locked()
        status['clk0_greaterthan'] = (value >> 0) & 0b1
        status['clk1_greaterthan'] = (value >> 1) & 0b1
        status['clk2_greaterthan'] = (value >> 2) & 0b1
        status['clk3_greaterthan'] = (value >> 3) & 0b1
        status['clk0_lowerthan'] = (value >> 4) & 0b1
        status['clk1_lowerthan'] = (value >> 5) & 0b1
        status['clk2_lowerthan'] = (value >> 6) & 0b1
        status['clk3_lowerthan'] = (value >> 7) & 0b1
        status['clk0_glitch'] = (value >> 8) & 0b1
        status['clk1_glitch'] = (value >> 9) & 0b1
        status['clk2_glitch'] = (value >> 10) & 0b1
        status['clk3_glitch'] = (value >> 11) & 0b1
        status['clk0_stop'] = (value >> 12) & 0b1
        status['clk1_stop'] = (value >> 13) & 0b1
        status['clk2_stop'] = (value >> 14) & 0b1
        status['clk3_stop'] = (value >> 15) & 0b1

        return status

    def get_locked(self) -> bool:
        """
            Get lock status of PLL
            :return bool: Lock status of PLL
        """
        locked = self.bus.read_i32(self.Registers.SR)
        locked = (locked >> 0) & 0b1
        return bool(locked)

    def config_output(self, output=0, divider=1.0, phase=0.0, duty=50) -> None:
        """
            Config output path
            :param output: index of output clock
            :param divider: output clock divider
            :param phase: output clock phase
            :param duty: ouput clock duty cycle
        """
        # output 0: reg2/3/4
        # output 1: reg5/6/7
        # output 2: reg8/9/10
        # output 3: reg11/12/13
        # output 4: reg14/15/16
        # output 5: reg17/18/19
        # output 6: reg20/21/22

        assert (0 <= output <= 6), ("Output {} is invalid".format(output))
        assert (-360 < phase < 360), ("Phase {} is invalid".format(phase))
        assert (0 < duty < 100), ("Duty cycle {} is invalid".format(duty))

        # divider
        divider_int = (int(divider*8) >> 3) & 0xFF
        divider_frac = (int(divider*8) & 0b111)*125
        divide_value = divider_int + (divider_frac << 8)

        # phase
        phase_value = int(phase * 1000) & 0xFFFFFFFF

        # duty
        duty_value = (duty * 1000) & 0xFFFFFFFF

        # write config
        self.bus.write_i32(self.Registers['ClkCfgReg' + str(2 + output*3)], divide_value)
        self.bus.write_i32(self.Registers['ClkCfgReg' + str(3 + output*3)], phase_value)
        self.bus.write_i32(self.Registers['ClkCfgReg' + str(4 + output*3)], duty_value)

    def config_vco(self, mult=4.0, div=1, f_in=250000000.0, phase=0.0) -> None:
        """
            Config VCO frequency
            Needs to end up within allowable limits Fvco = f_in * mult / div
            Mult can have a fraction of 0.125, depending on the technology used.
            For some technologies mult is minimum 2.
            :param mult:
            :param div:
            :param f_in: input clock frequency
            :param phase: phase in degrees
        """
        # calculate frequency
        f_vco = f_in * (mult / div)

        assert (f_vco <= self.limits.f_vco_max), \
            ("Configured VCO frequency {} Hz greater than max allowed frequency {} Hz".format(f_vco, self.limits.f_vco_max))
        assert (f_vco >= self.limits.f_vco_min), \
            ("Configured VCO frequency {} Hz smaller than min allowed frequency {} Hz".format(f_vco, self.limits.f_vco_min))

        # do uploads
        vco_mult_int = (int(mult*8) >> 3) & 0xFF
        vco_mult_frac = (int(mult*8) & 0b111)*125
        vco_div = div

        clk_cfg_reg0 = (vco_mult_frac << 16) + (vco_mult_int << 8) + (vco_div & 0xFF)
        self.bus.write_i32(self.Registers.ClkCfgReg0, clk_cfg_reg0)

        # phase
        # signed integer, has to be entered as x1000
        clk_cfg_reg1 = int(phase * 1000) & 0xFFFFFFFF
        self.bus.write_i32(self.Registers.ClkCfgReg1, clk_cfg_reg1)

    def commit(self, use_default=False) -> None:
        """
            Sends a start command to start clock reconfiguration.
            :param use_default: Selects between default config from hardware GUI wizard, or custom config
        """
        load_value = 0x1 if use_default else 0x03
        self.bus.write_i32(self.Registers.ClkCfgReg23, load_value)

    def calculate_params(self, f_in:float=25e6, f_req:float=38.4e6):
        """
            Calculate ideal multiply/dividersettings on a given input and output frequency
            Based on MMCM programming of UG572
            :param f_in: input frequency of PLL
            :param f_req: requested output frequency
            :returns
        """
        assert (self.limits.f_out_min <= f_req <= self.limits.f_out_max), \
            "Requested Frequency not in valid range. [{:.3e}, {:.3e}] Hz".format(self.limits.f_out_max, self.limits.f_out_min)

        # fixme, add fractional support
        d_min = max(int(ceil(f_in / self.limits.f_pfd_max)), self.limits.d_min)
        d_max = min(int(floor(f_in / self.limits.f_pfd_min)), self.limits.d_max)
        o_min = max(int(floor(self.limits.f_vco_min / f_req)), self.limits.o_min)
        o_max = min(int(ceil(self.limits.f_vco_max / f_req)), self.limits.o_max)

        # defaults
        best_err = float("inf")
        best_f_vco = 0
        best_f_out = 0
        best_d = None
        best_m = None
        best_o = None

        for d in range(d_min, d_max+1):
            f_pfd = f_in / d
            if self.limits.f_pfd_min <= f_pfd <= self.limits.f_pfd_max:
                m_min = max(int(ceil(self.limits.f_vco_min / f_pfd)), self.limits.m_min)
                m_max = min(int(floor(self.limits.f_vco_max / f_pfd)), self.limits.m_max)

                for m in range(m_max, m_min-1, -1):
                    f_vco = f_pfd * m
                    if self.limits.f_vco_min <= f_vco <= self.limits.f_vco_max:

                        for o in range(o_min, o_max+1):
                            f_vco = f_in * m / d
                            f_out = f_vco / o
                            error = abs(f_req - f_out)
                            if (error < best_err) or (error == best_err and d <= best_d and f_vco >= best_f_vco):
                                best_err = error
                                best_f_vco = f_vco
                                best_f_out = f_out
                                best_d = d
                                best_m = m
                                best_o = o

        return best_m, best_d, best_o, best_f_out, best_f_vco

    def reconfigure_clock(self, f_in:float=100e6, f_req:float=20.0e6, phase:float=0.0, duty:int=50, output:int=0):
        """
            Function to reconfigure only !!!one!!! clock . Will change VCO frequency,
            do not use this function when more than one clock output on PLL is used.
            :param f_in: input clock frequency
            :param f_req: requested output frequency
            :param phase: phase of requested output clock
            :param duty: duty cycle of requested output clock
            :param output: output to configure
            :return actual frequency of output clock and VCO frequency.
        """
        # calculate settings
        vco_mult, vco_div, output_div, f_out, f_vco = self.calculate_params(f_in=f_in, f_req=f_req)

        # apply settings
        self.config_vco(mult=vco_mult, div=vco_div, f_in=f_in, phase=0)
        self.config_output(output=output, divider=output_div, phase=phase, duty=duty)
        self.commit()

        return f_out, f_vco
