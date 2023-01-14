from modules.axi import UartMaster, BasicBus
from modules.axi_gpio import AxiGpio
from modules.clk_wizard import ClkWizard
from modules.frequency_counter import FrequencyCounter
from modules.identifier import Identifier


################################################################################
class System:
    def __init__(self, port):
        bus_axi = UartMaster(port, 1000000)
        bus_identifier = BasicBus(bus_axi, offset=0x4000_0000, range=12)
        bus_freq_cnt = BasicBus(bus_axi, offset=0x4000_1000, range=12)
        bus_gpio = BasicBus(bus_axi, offset=0x4000_2000, range=12)
        bus_clk_wiz = BasicBus(bus_axi, offset=0x4001_0000, range=16)

        self.identifier = Identifier(bus_identifier)
        self.freq_counter = FrequencyCounter(bus_freq_cnt)
        self.gpio = AxiGpio(bus_gpio)
        self.clk_wiz = ClkWizard(bus_clk_wiz, 'MMCM', 'Artix7', '1.00v-1')


################################################################################
def main():
    system = System('COM4')

    print('Identifier:')
    print(f'\tID: {hex(system.identifier.get_module_id())}')
    print(f'\tName: {system.identifier.get_name()}')
    print('\tVersion: v%d.%d' % system.identifier.get_version())
    print()
    print("Frequency Counter:")
    print(f'\tID: {hex(system.freq_counter.get_module_id())}')
    print(f'\tFreq: {system.freq_counter.get_frequency()}')

    system.clk_wiz.reconfigure_clock(f_req=20.0e6)
    print(f'\tFreq: {system.freq_counter.get_frequency()}')


################################################################################
if __name__ == "__main__":
    main()
