from fpga_modules import BasicBus, ClkWizard, Identifier, Uart2Axi, VGA, VideoTPG


################################################################################
class System:
    def __init__(self, port):
        bus_axi = Uart2Axi(port, 1000000)

        bus_identifier = BasicBus(bus_axi, offset=0x4000_0000, range=12)
        bus_vga = BasicBus(bus_axi, offset=0x4000_1000, range=12)
        bus_clk_wiz = BasicBus(bus_axi, offset=0x4000_2000, range=13)
        bus_video_tpg = BasicBus(bus_axi, offset=0x4001_0000, range=16)

        self.identifier = Identifier(bus_identifier)
        self.vga = VGA(bus_vga)
        self.clk_wiz = ClkWizard(bus_clk_wiz, 'MMCM', 'Artix7', '1.00v-1')
        self.video_tpg = VideoTPG(bus_video_tpg)


################################################################################
def main():
    system = System('COM4')

    print('Identifier:')
    print(f'\tID: {hex(system.identifier.get_module_id())}')
    print(f'\tName: {system.identifier.get_name()}')
    print('\tVersion: v%d.%d' % system.identifier.get_version())
    print()


    mode = "1280x1024p60"

    if mode == "640x480p60":
        system.clk_wiz.reconfigure_clock(f_req=25.125e6)
        print(f'\tFreq: {system.freq_counter.get_frequency()}')
        system.regbank.set_reg_out(8, 1)        # init
        system.regbank.set_reg_out(0, 640)      # h_res
        system.regbank.set_reg_out(1, 16)       # h_front_porch
        system.regbank.set_reg_out(2, 96)       # h_sync_pulse
        system.regbank.set_reg_out(3, 48)       # h_back_porch
        system.regbank.set_reg_out(4, 480)      # v_res
        system.regbank.set_reg_out(5, 10)       # v_front_porch
        system.regbank.set_reg_out(6, 2)        # v_sync_pulse
        system.regbank.set_reg_out(7, 33)       # v_back_porch
        system.regbank.set_reg_out(8, 0)        # init

    elif mode == "800x600p60":
        system.clk_wiz.reconfigure_clock(f_req=40.00e6)
        print(f'\tFreq: {system.freq_counter.get_frequency()}')
        system.regbank.set_reg_out(8, 1)        # init
        system.regbank.set_reg_out(0, 800)      # h_res
        system.regbank.set_reg_out(1, 40)       # h_front_porch
        system.regbank.set_reg_out(2, 128)      # h_sync_pulse
        system.regbank.set_reg_out(3, 88)       # h_back_porch
        system.regbank.set_reg_out(4, 600)      # v_res
        system.regbank.set_reg_out(5, 1)        # v_front_porch
        system.regbank.set_reg_out(6, 3)        # v_sync_pulse
        system.regbank.set_reg_out(7, 23)       # v_back_porch
        system.regbank.set_reg_out(8, 0)        # init

    elif mode == "1024x768p60":
        system.clk_wiz.reconfigure_clock(f_req=65.00e6)
        print(f'\tFreq: {system.freq_counter.get_frequency()}')
        system.regbank.set_reg_out(8, 1)        # init
        system.regbank.set_reg_out(0, 1024)     # h_res
        system.regbank.set_reg_out(1, 24)       # h_front_porch
        system.regbank.set_reg_out(2, 136)      # h_sync_pulse
        system.regbank.set_reg_out(3, 160)      # h_back_porch
        system.regbank.set_reg_out(4, 768)      # v_res
        system.regbank.set_reg_out(5, 3)        # v_front_porch
        system.regbank.set_reg_out(6, 6)        # v_sync_pulse
        system.regbank.set_reg_out(7, 29)       # v_back_porch
        system.regbank.set_reg_out(8, 0)        # init

    elif mode == "1280x1024p60":
        system.clk_wiz.reconfigure_clock(f_req=108.00e6)
        print(f'\tFreq: {system.freq_counter.get_frequency()}')
        system.regbank.set_reg_out(8, 1)        # init
        system.regbank.set_reg_out(0, 1280)     # h_res
        system.regbank.set_reg_out(1, 48)       # h_front_porch
        system.regbank.set_reg_out(2, 112)      # h_sync_pulse
        system.regbank.set_reg_out(3, 248)      # h_back_porch
        system.regbank.set_reg_out(4, 1024)     # v_res
        system.regbank.set_reg_out(5, 1)        # v_front_porch
        system.regbank.set_reg_out(6, 3)        # v_sync_pulse
        system.regbank.set_reg_out(7, 38)       # v_back_porch
        system.regbank.set_reg_out(8, 0)        # init


################################################################################
if __name__ == "__main__":
    main()
