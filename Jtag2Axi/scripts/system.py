from modules.axi import BasicBus
from modules.axi_gpio import AxiGpio
from modules.identifier import Identifier
from modules.jtag2axi import Jtag2Axi

from pysct.core import *


################################################################################
class System:
    def __init__(self, xsct):
        bus_axi = Jtag2Axi(xsct)

        bus_identifier = BasicBus(bus_axi, offset=0x4000_0000, range=12)
        bus_gpio = BasicBus(bus_axi, offset=0x4000_1000, range=12)

        self.identifier = Identifier(bus_identifier)
        self.gpio = AxiGpio(bus_gpio)


################################################################################
def main():

    win_xsct_executable = r'C:\Xilinx\Vivado\2022.2\bin\xsdb.bat'
    xsct_server = XsctServer(win_xsct_executable, port=PORT, verbose=False)
    xsct = Xsct('localhost', PORT)

    system = System(xsct)
    print('Identifier:')
    print(f'\tID: {hex(system.identifier.get_module_id())}')
    print(f'\tName: {system.identifier.get_name()}')
    print('\tVersion: v%d.%d' % system.identifier.get_version())
    print()


################################################################################
if __name__ == "__main__":
    main()
