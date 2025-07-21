from typing import *
from collections import *

inf = float('inf')

class Solution:
    def countTrapezoids(self, points: List[List[int]]) -> int:
        cnt = defaultdict(lambda: defaultdict(int))
        cnt2 = defaultdict(lambda: defaultdict(int))

        for i, (x, y) in enumerate(points):
            for j in range(i):
                x2, y2 = points[j]
                dy = y - y2
                dx = x - x2
                k = dy / dx if dx else inf
                b = (y * dx - x * dy) / dx if dx else x
                cnt[k][b] += 1
                cnt2[(x + x2, y + y2)][k] += 1

        ans = 0
        for m in cnt.values():
            s = 0
            for c in m.values():
                ans += s * c
                s += c

        for m in cnt2.values():
            s = 0
            for c in m.values():
                ans -= s * c
                s += c

        return ans