from modules.axi import UartMaster, BasicBus
from modules.identifier import Identifier


################################################################################
class System:
    def __init__(self, port):
        bus_axi = UartMaster(port, 9600)
        bus_identifier = BasicBus(bus_axi, offset=0x00000000, range=32)
        bus_regbank = BasicBus(bus_axi, offset=0x00010000, range=32)

        self.identifier = Identifier(bus_identifier)


################################################################################
def main():
    system = System('COM5')
    print('ModuleId: 0x%08X' % system.identifier.get_module_id())
    print(f'Name:     {system.identifier.get_name()}')
    print('Version:  v%d.%d' % system.identifier.get_version())


################################################################################
if __name__ == "__main__":
    main()
