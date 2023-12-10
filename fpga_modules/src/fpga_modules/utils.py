from typing import List


################################################################################
def int2bytes(x: int, length) -> List[int]:
    return [x >> 8 * i & 0xFF for i in range(0, length)]


def bytes2int(x: List[int]) -> int:
    return sum([x[i] << 8 * i for i in range(len(x))])
