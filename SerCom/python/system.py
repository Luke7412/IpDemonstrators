from modules.axi import UartMaster, BasicBus
from modules.frequency_counter import FrequencyCounter
from modules.identifier import Identifier


################################################################################
class System:
    def __init__(self, port):
        bus_axi = UartMaster(port, 1000000)
        bus_identifier = BasicBus(bus_axi, offset=0x44a0_0000, range=32)
        bus_freq_cnt = BasicBus(bus_axi, offset=0x00000000, range=32)

        self.identifier = Identifier(bus_identifier)
        self.freq_counter = FrequencyCounter(bus_freq_cnt)


################################################################################
def main():
    system = System('COM4')
    print('Identifier:')
    print(f'\tName: {system.identifier.get_name()}')
    print('\tVersion: v%d.%d' % system.identifier.get_version())
    print()
    print("Frequency Counter:")
    print(f'\tID: {hex(system.freq_counter.get_module_id())}')
    print(f'\tFreq: {system.freq_counter.get_frequency()}')


################################################################################
if __name__ == "__main__":
    main()
