from typing import *
from collections import *

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Solution:
    def maxSumDistinctTriplet(self, x: List[int], y: List[int]) -> int:
        mp = defaultdict(int)
        for a, b in zip(x, y):
            mp[a] = fmax(mp[a], b)

        if len(mp) < 3:
            return -1
        else:
            return sum(sorted(mp.values(), reverse = True)[:3])