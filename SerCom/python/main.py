from axi import UartMaster, BasicBus


###############################################################################
def main():
    uart_master = UartMaster('COM5', 9600)

    bus_identifier = BasicBus(uart_master, offset=0x00000000, range=32)
    bus_regbank = BasicBus(uart_master, offset=0x00010000, range=32)

    bus_regbank.write(address=0x00000000, data=[0]*8)
    bus_regbank.write(address=0x00000003, data=[0xFF])
    print([hex(x) for x in bus_regbank.read(0x00000000, 8)])


###############################################################################
if __name__ == "__main__":
    main()
