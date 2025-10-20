from typing import *

class Solution:
    def missingMultiple(self, nums: List[int], k: int) -> int:
        S = set(nums)
        for i in range(1, 1001):
            if i * k not in S:
                return i * k