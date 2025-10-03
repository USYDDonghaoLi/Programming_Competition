from typing import *

class Solution:
    def decimalRepresentation(self, n: int) -> List[int]:
        res = []
        mul = 1

        while n:
            t = n % 10
            if t:
                res.append(t * mul)
            mul *= 10
            n //= 10

        return res[::-1]