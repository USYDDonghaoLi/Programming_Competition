from typing import List
from collections import defaultdict

class Solution:
    def maxTotal(self, A: List[int], B: List[int]) -> int:
        mp = defaultdict(list)
        for a, b in zip(B, A):
            mp[a].append(b)

        res = 0
        for key in mp:
            mp[key].sort(reverse = True)
            res += sum(mp[key][:key])

        return res