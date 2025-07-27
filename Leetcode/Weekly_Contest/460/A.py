from typing import *
from collections import *

class Solution:
    def maximumMedianSum(self, A: List[int]) -> int:
        A.sort()
        res = 0
        q = deque(A)

        while q:
            a, c, b = q.popleft(), q.pop(), q.pop()
            res += b

        return res