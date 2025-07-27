# 线性基模板
class XorBasis:
    def __init__(self, n: int):
        self.b = [0] * n

    def insert(self, x: int) -> None:
        b = self.b
        while x:
            i = x.bit_length() - 1  # x 的最高位
            if b[i] == 0:  # x 和之前的基是线性无关的
                b[i] = x  # 新增一个基，最高位为 i
                
                return
            x ^= b[i]  # 保证参与 max_xor 的基的最高位是互不相同的，方便我们贪心
        # 正常循环结束，此时 x=0，说明一开始的 x 可以被已有基表出，不是一个线性无关基

    def max_xor(self) -> int:
        b = self.b
        res = 0
        # 从高到低贪心：越高的位，越必须是 1
        # 由于每个位的基至多一个，所以每个位只需考虑异或一个基，若能变大，则异或之
        for i in range(len(b) - 1, -1, -1):
            if res ^ b[i] > res:
                res ^= b[i]
        return res

from typing import *

class Solution:
    def maximizeXorAndXor(self, nums: List[int]) -> int:
        n = len(nums)
        sz = max(nums).bit_length()

        # 多算一个子集 OR，用于剪枝
        u = 1 << n
        sub_and = [0] * u
        sub_xor = [0] * u
        sub_or = [0] * u
        sub_and[0] = -1
        for i, x in enumerate(nums):
            high_bit = 1 << i
            for mask in range(high_bit):
                sub_and[high_bit | mask] = sub_and[mask] & x
                sub_xor[high_bit | mask] = sub_xor[mask] ^ x
                sub_or[high_bit | mask] = sub_or[mask] | x
        sub_and[0] = 0

        def max_xor2(sub: int) -> int:
            b = XorBasis(sz)
            xor = sub_xor[sub]
            for i, x in enumerate(nums):
                if sub >> i & 1:
                    b.insert(x & ~xor)
            return xor + b.max_xor() * 2

        ans = 0
        for i in range(u):
            if sub_and[i] + sub_or[(u - 1) ^ i] * 2 > ans:  # 有机会让 ans 变得更大
                ans = max(ans, sub_and[i] + max_xor2((u - 1) ^ i))
        return ans