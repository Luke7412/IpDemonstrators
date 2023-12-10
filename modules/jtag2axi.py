from typing import List
from pysct.core import *

from modules.axi import Bus
from modules.utils import int2bytes


################################################################################
class Jtag2Axi(Bus):
    def __init__(self, xsct=None):
        if xsct is None:
            xsct = Xsct('localhost', 3010)
        self.xsct = xsct
        self.connect()

    def connect(self):
        self.xsct.do("connect")
        self.xsct.do("targets")
        self.xsct.do("target 3")

    def read(self, address: int, length: int) -> List[int]:
        data = self.xsct.do(f'mrd -value {address} {length//4}')
        data = [int(x) for x in data.split(' ')]
        data = [int2bytes(x, 4) for x in data]
        return [byte for bytes in data for byte in bytes]

    def read_i32(self, address: int) -> int:
        return self.xsct.do(f'mrd -value {address}')

    def write_i32(self, address: int, data: int) -> None:
        self.xsct.do(f'mwr {address} {data}')
