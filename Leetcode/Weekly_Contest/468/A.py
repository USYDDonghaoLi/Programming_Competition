from typing import *

class Solution:
    def evenNumberBitwiseORs(self, A: List[int]) -> int:
        res = 0
        for a in A:
            if not a & 1:
                res |= a
        return res