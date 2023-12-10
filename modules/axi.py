from typing import List, Dict
from abc import ABC

from modules.utils import bytes2int, int2bytes


################################################################################
class AddressOutOfRangeException(Exception):
    def __init__(self):
        self.message = f'Address out of range.'
        super().__init__(self.message)


class ResponsePacketException(Exception):
    def __init__(self):
        self.message = f'Response packet has wrong ID. Must be 0 or 3'
        super().__init__(self.message)


class AxiResponseError(Exception):
    def __init__(self):
        self.message = f'Transaction ended with AXI response error'
        super().__init__(self.message)


################################################################################
class Bus(ABC):
    def read(self, address: int, length: int) -> List[int]:
        raise NotImplementedError(f'Function "read" not implemented in class "{self.__class__.__name__}"')

    def write(self, address: int, data: List[int]) -> None:
        raise NotImplementedError(f'Function "write" not implemented in class "{self.__class__.__name__}"')

    def read_i32(self, address: int) -> int:
        raise NotImplementedError(f'Function "read_i32" not implemented in class "{self.__class__.__name__}"')

    def write_i32(self, address: int, data: int) -> None:
        raise NotImplementedError(f'Function "write_i32" not implemented in class "{self.__class__.__name__}"')


################################################################################
class StubBus(Bus):
    def __init__(self):
        self.memory_map: Dict[int, int] = dict()

    def read(self, address: int, length: int) -> List[int]:
        data_bytes = []
        for key in range(address, address+length):
            if key in self.memory_map:
                data_bytes.append(self.memory_map[address])
            else:
                data_bytes.append(0)
        return data_bytes

    def write(self, address: int, data: List[int]) -> None:
        for index, el in enumerate(data):
            self.memory_map[address + index] = el

    def read_i32(self, address: int) -> int:
        data_bytes = self.read(address, 4)
        return bytes2int(data_bytes)

    def write_i32(self, address: int, data: int) -> None:
        self.write(address, int2bytes(data, 4))


################################################################################
class BasicBus(Bus):
    def __init__(self, bus: Bus, offset: int, range: int):
        self.bus = bus
        self.offset = offset
        self.range = range

    def read(self, address: int, length: int) -> List[int]:
        self.check_transaction(address, length)
        data = self.bus.read(self.update_address(address), length)
        return data

    def write(self, address: int, data: List[int]) -> None:
        self.check_transaction(address, len(data))
        self.bus.write(self.update_address(address), data)

    def read_i32(self, address: int) -> int:
        return bytes2int(self.read(address, 4))

    def write_i32(self, address: int, data: int) -> None:
        self.write(address, int2bytes(data, 4))

    def check_transaction(self, address: int, length: int) -> None:
        if not 0 <= address and address + length < self.range:
            raise AddressOutOfRangeException()

    def update_address(self, address: int) -> int:
        return address + self.offset
