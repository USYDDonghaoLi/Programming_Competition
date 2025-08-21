fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

from collections import defaultdict, deque
from typing import List

inf = float('inf')

class Solution:
    def minArraySum(self, A: List[int], k: int) -> int:
        mp = defaultdict(lambda: inf)
        mp[0] = 0
        n = len(A)

        s = 0

        for i, v in enumerate(A, 1):
            cur = mp[s % k] + v
            s += v

            cur = fmin(cur, mp[s % k])

            mp[s % k] = cur

            if i == n:
                return cur