from modules.axi import BasicBus, Bus
from modules.axi_gpio import AxiGpio
from modules.bram import BRAM
from modules.identifier import Identifier
from modules.jtag2axi import Jtag2Axi

from pysct.core import *
from time import perf_counter


################################################################################
class CustomGpio:
    def __init__(self, bus: Bus):
        self.gpio = AxiGpio(bus)
        self.setup()

    def setup(self):
        self.gpio.set_tristate(channel=0, value=0xFFFFFFF0)
        self.gpio.set_tristate(channel=1, value=0xFFFFFFFF)

    def set_leds(self, value:int):
        self.gpio.write(channel=0, value=value & 0x0000000F)

    def get_leds(self):
        value = self.gpio.read(channel=0)
        return value & 0x0000000F

    def get_switches(self):
        value = self.gpio.read(channel=1)
        return value & 0x0000000F


class System:
    def __init__(self, xsct):
        self.bus_axi = Jtag2Axi(xsct)

        bus_identifier = BasicBus(self.bus_axi, offset=0x4000_0000, range=12)
        bus_gpio = BasicBus(self.bus_axi, offset=0x4000_1000, range=12)
        bus_bram = BasicBus(self.bus_axi, offset=0x4000_2000, range=12)

        self.identifier = Identifier(bus_identifier)
        self.gpio = CustomGpio(bus_gpio)
        self.bram = BRAM(bus_bram)


################################################################################
def main():

    win_xsct_executable = r'C:\Xilinx\Vivado\2022.2\bin\xsdb.bat'
    xsct_server = XsctServer(win_xsct_executable, port=PORT, verbose=False)
    xsct = Xsct('localhost', PORT)

    system = System(xsct)

    # Identifier
    print()
    print('Identifier:')
    print(f'\tID: {hex(system.identifier.get_module_id())}')
    print(f'\tName: {system.identifier.get_name()}')
    print('\tVersion: v%d.%d' % system.identifier.get_version())

    # GPIO
    print()
    print('GPIO')
    system.gpio.set_leds(15)
    print(f'Leds: {system.gpio.get_leds()}')
    print(f'Switches: {system.gpio.get_switches()}')

    # BRAM
    print()
    print('BRAM Performance')
    repeats = 200
    sizes = [2**x for x in range(2, 11)]
    points = []

    print('\tWrite')
    for nof_bytes in sizes:
        data = nof_bytes * [0]
        t_deltas = []
        for i in range(repeats):
            t_start = perf_counter()
            system.bram.write(address=0, data=data)
            t_deltas.append(perf_counter() - t_start)
        points.append({'size': nof_bytes, 't_delta': sum(t_deltas)/len(t_deltas)})

    for point in points:
        print(f'\t\tSize: {point["size"]:4d}, duration: {point["t_delta"]:.6f} s, bitrate: {8*point["size"]/point["t_delta"]/1000000:.2f} Mbit/s')

    print()
    print('\tRead')
    points = []
    for nof_bytes in sizes:
        t_deltas = []
        for i in range(repeats):
            t_start = perf_counter()
            system.bram.read(address=0, length=nof_bytes)
            t_deltas.append(perf_counter() - t_start)
        points.append({'size': nof_bytes, 't_delta': sum(t_deltas)/len(t_deltas)})

    for point in points:
        print(f'\t\tSize: {point["size"]:4d}, duration: {point["t_delta"]:.6f} s, bitrate: {8*point["size"]/point["t_delta"]/1000000:.2f} Mbit/s')


################################################################################
if __name__ == "__main__":
    main()
