from typing import *
from collections import *

class Solution:
    def sumDivisibleByK(self, nums: List[int], k: int) -> int:
        c = Counter(nums)
        res = 0

        for key, val in c.items():
            if val % k == 0:
                res += key * val

        return res