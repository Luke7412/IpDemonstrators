from modules.axi import BasicBus
from modules.axi_gpio import AxiGpio
from modules.identifier import Identifier
from modules.uart2axi import Uart2Axi


################################################################################
class System:
    def __init__(self, port):
        bus_axi = Uart2Axi(port, 1000000)
        bus_identifier = BasicBus(bus_axi, offset=0x4000_0000, range=12)
        bus_gpio = BasicBus(bus_axi, offset=0x4000_1000, range=12)

        self.identifier = Identifier(bus_identifier)
        self.gpio = AxiGpio(bus_gpio)


################################################################################
def main():
    system = System('COM6')

    print('Identifier:')
    print(f'\tID: {hex(system.identifier.get_module_id())}')
    print(f'\tName: {system.identifier.get_name()}')
    print('\tVersion: v%d.%d' % system.identifier.get_version())
    print()


################################################################################
if __name__ == "__main__":
    main()
