from enum import IntEnum
from typing import List, Dict
from abc import ABC
from serial import Serial


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
def int2bytes(x: int, length) -> List[int]:
    return [x >> 8 * i & 0xFF for i in range(0, length)]


def bytes2int(x: List[int]) -> int:
    return sum([x[i] << 8 * i for i in range(len(x))])


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


################################################################################
class UartMaster(Bus):
    class PacketId(IntEnum):
        READ_ADDR = 2
        READ_RESP = 3
        WRITE_ADDR = 1
        WRITE_DATA = 4
        WRITE_RESP = 0

    def __init__(self, name, baud_rate, timeout=1.0):
        self.serial: Serial = Serial(name, baud_rate, timeout=timeout)

        self.start_byte = 0x7D
        self.stop_byte = 0x7E
        self.escape_byte = 0x7F

        self.axi_prot = 0
        self.axi_size = 0b010
        self.axi_burst = 0b01
        self.axi_cache = 0
        self.axi_lock = 0
        self.axi_id = 0

        self.bytes_per_beat = 2**self.axi_size

    ############################################################################
    def make_address_packet(self, packet_id: PacketId, address: int, length: int) -> List[int]:
        pkt = [packet_id]
        pkt.extend(int2bytes(address, 4))

        val = (self.axi_id & 0x01) << 21 | (self.axi_lock & 0x01) << 20 | \
              (length - 1 & 0xFF) << 12 | (self.axi_cache & 0x0F) << 8 | \
              (self.axi_burst & 0x03) << 6 | (self.axi_size & 0x07) << 3 | \
              (self.axi_prot & 0x07) << 0
        # val += qos & 0xF << 25
        pkt.extend(int2bytes(val, 4))
        return pkt

    def pack_data(self, packet_id: PacketId, data: List[int], offset) -> List[List[int]]:
        # Realign data
        valid = [0] * offset + [1] * len(data)
        data = [0] * offset + data

        # Add Padding bytes
        nof_beats = int((len(data) + self.bytes_per_beat-1) / self.bytes_per_beat)
        bytes_to_add = self.bytes_per_beat * nof_beats - len(data)
        valid = valid + [0] * bytes_to_add
        data = data + [0] * bytes_to_add

        # Split data and valid vector in beats
        valid_queue = [valid[i:i + self.bytes_per_beat] for i in range(0, len(valid), self.bytes_per_beat)]
        data_beats = [data[i:i + self.bytes_per_beat] for i in range(0, len(data), self.bytes_per_beat)]

        # Create a packet for each data beat
        pkt_queue = []
        for index, data_beat in enumerate(data_beats):
            valid = valid_queue[index]
            data_msg = [packet_id]
            axi_strb = sum([2**index for index in range(len(valid)) if valid[index]])
            axi_last = int(index == len(data_beats)-1)
            data_msg.extend(data_beat)
            val = (axi_last & 0x01) << 4 | (axi_strb & 0x0F) << 0
            data_msg.extend(int2bytes(val, 1))
            pkt_queue.append(data_msg)

        return pkt_queue

    def unpack_write_response(self, data: List[int]):
        if data.pop(0) != self.PacketId.WRITE_RESP:
            raise ResponsePacketException()

        val = bytes2int(data)
        axi_resp = (val >> 0) & 0x3
        axi_id = (val >> 2) & 0x1
        return axi_resp

    def unpack_read_response(self, data: List[List[int]]):
        data_bytes = []
        axi_resp = 0
        for beat in data:
            if beat.pop(0) != self.PacketId.READ_RESP:
                raise ResponsePacketException()

            data_bytes.extend(beat[0:4])
            val = bytes2int(beat[4:5])
            axi_resp = (val >> 0) & 0x3
            # axi_last = (val >> 2) & 0x1
            # axi_id = (val >> 3) & 0xF
            # axi_user = (val >> 6) & 0xF
        return data_bytes, axi_resp

    ############################################################################
    def add_escape_chars(self, data_bytes: List[int]) -> List[int]:
        new_byte_list = list()
        for data_byte in data_bytes:
            if data_byte in (self.start_byte, self.stop_byte, self.escape_byte):
                new_byte_list.append(self.escape_byte)
            new_byte_list.append(data_byte)

        return new_byte_list

    def remove_escape_chars(self, data_bytes: List[int]) -> List[int]:
        new_byte_list = list()
        prev_was_escape = False
        for data_byte in data_bytes:
            if data_byte == self.escape_byte and not prev_was_escape:
                prev_was_escape = True
            else:
                new_byte_list.append(data_byte)
                prev_was_escape = False

        return new_byte_list

    def add_framing(self, data_bytes: List[int]) -> List[int]:
        return [self.start_byte] + data_bytes + [self.stop_byte]

    ############################################################################
    def fetch_response(self, nof_packets: int = 1) -> List[List[int]]:
        resp_queue = []
        for i in range(nof_packets):
            resp_pkt = []
            running = False
            while True:
                resp_byte = list(self.serial.read(1))
                if len(resp_byte) == 0:
                    break
                else:
                    resp_byte = resp_byte[0]
                if resp_byte == self.start_byte:
                    running = True
                if running:
                    resp_pkt.append(resp_byte)
                if resp_byte == self.stop_byte:
                    break
            resp_queue.append(resp_pkt)

        return resp_queue

    def start_transaction(self, pkt_queue: List[List[int]], resp_length: int = 1) -> List[List[int]]:
        # pack each message in message queue
        pkt_queue = [self.add_escape_chars(x) for x in pkt_queue]
        pkt_queue = [self.add_framing(x) for x in pkt_queue]

        # flatten message queue
        pkt_bytes = [val for msg in pkt_queue for val in msg]

        # send bytes in pkt_bytes
        self.serial.write(pkt_bytes)

        # Fetch response packet
        resp_queue = self.fetch_response(resp_length)

        # Remove framing and escape characters from response packets
        resp_queue = [resp_pkt[1:-1] for resp_pkt in resp_queue]
        resp_queue = [self.remove_escape_chars(resp_pkt) for resp_pkt in resp_queue]
        return resp_queue

    def write(self, address: int, data: List[int]) -> None:
        pkt_queue = []

        offset = address % self.bytes_per_beat
        aligned_address = address - offset

        # Add write address packet to queue
        nof_packets = int((len(data)+offset-1) / self.bytes_per_beat) + 1
        addr_pkt = self.make_address_packet(self.PacketId.WRITE_ADDR, aligned_address, nof_packets)
        pkt_queue.append(addr_pkt)

        # Add write data packet to queue
        data_pkt = self.pack_data(self.PacketId.WRITE_DATA, data, offset)
        pkt_queue.extend(data_pkt)

        # Send pkt_queue and receive resp_queue
        resp_queue = self.start_transaction(pkt_queue)

        resp_pkt = resp_queue[0]
        resp = self.unpack_write_response(resp_pkt)
        if resp:
            raise AxiResponseError()

    def read(self, address: int, length: int = 4) -> List[int]:
        pkt_queue = []

        offset = address % self.bytes_per_beat
        aligned_address = address - offset

        # Add write address pck to queue
        nof_packets = int((length+offset-1) / self.bytes_per_beat) + 1
        addr_pkt = self.make_address_packet(self.PacketId.READ_ADDR, aligned_address, nof_packets)
        pkt_queue.append(addr_pkt)

        # Send pkt_queue and receive resp_queue
        resp_queue = self.start_transaction(pkt_queue, nof_packets)

        value, resp = self.unpack_read_response(resp_queue)
        value = value[offset:offset + length]

        if resp:
            raise AxiResponseError()
        return value
