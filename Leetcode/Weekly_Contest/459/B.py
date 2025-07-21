from typing import *
from collections import *

class Solution:
    def countTrapezoids(self, points: List[List[int]]) -> int:
        MOD = 1_000_000_007
        cnt = Counter(p[1] for p in points) 
        ans = s = 0
        for c in cnt.values():
            k = c * (c - 1) // 2
            ans += s * k
            s += k
        return ans % MOD