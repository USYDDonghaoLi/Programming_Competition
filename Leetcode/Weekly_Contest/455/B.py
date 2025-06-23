from typing import *

class Solution:
    def findCoins(self, numWays: List[int]) -> List[int]:
        mx = max(numWays)
        n = len(numWays)
        f = [1] + [0] * n
        ans = []
        for i, ways in enumerate(numWays, 1):
            if ways == f[i]:
                continue
            if ways - 1 != f[i]:
                return []
            ans.append(i)
            for j in range(i, n + 1):
                f[j] += f[j - i]
        return ans