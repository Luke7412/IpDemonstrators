from typing import List
from pysct.core import *

from .axi import Bus
from .utils import bytes2int


################################################################################
def check_address(address):
    if address % 4 != 0:
        raise ValueError(f'address must be multiple of 4')


class Jtag2Axi(Bus):
    def __init__(self, xsct=None):
        if xsct is None:
            xsct = Xsct('localhost', 3010)
        self.xsct = xsct
        self.connect()

    def connect(self):
        self.xsct.do('connect')
        self.xsct.do(f'target {self.get_target_index()}')

    def get_target_index(self):
        data = self.xsct.do('targets')
        match = re.search(r'(\d+)\s+JTAG2AXI', data)
        if match is None:
            raise Exception('JTAG2AXI target not found')

        idx = match.group(1)
        return idx

    def write(self, address: int, data: List[int]) -> None:
        check_address(address)
        data = [bytes2int(data[i:i+4]) for i in range(0, len(data), 4)]
        data = ' '.join(map(str, data))
        self.xsct.do(f'mwr -size w {address} {{ {data} }}')

    def read(self, address: int, length: int) -> List[int]:
        check_address(address)
        data = self.xsct.do(f'mrd -size b -value {address} {length}')
        return [int(x) for x in data.split(' ')]

    def read_i32(self, address: int) -> int:
        check_address(address)
        return self.xsct.do(f'mrd -size w -value {address}')

    def write_i32(self, address: int, data: int) -> None:
        check_address(address)
        self.xsct.do(f'mwr -size w {address} {data}')
