from typing import *
from collections import *
from heapq import *
from math import floor

inf = float('inf')

class Solution:
    def minTime(self, n: int, k: int, m: int, time: List[int], mul: List[float]) -> float:
        u = 1 << n
        max_time = [0] * u
        for i, t in enumerate(time):
            high_bit = 1 << i
            for mask in range(high_bit):
                max_time[high_bit | mask] = max(max_time[mask], t)

        sub_masks = [[] for _ in range(u)]
        for i in range(u):
            sub = i
            while sub:
                if sub.bit_count() <= k:
                    sub_masks[i].append(sub)
                sub = (sub - 1) & i

        dis = [[[inf, inf] for _ in range(u)] for _ in range(m)]
        h = []

        def push(d: float, stage: int, mask: int, state: int) -> None:
            if d < dis[stage][mask][state]:
                dis[stage][mask][state] = d
                heappush(h, (d, stage, mask, state))

        push(0, 0, u - 1, 0)

        while h:
            d, stage, left, state = heappop(h)
            if left == 0:
                return d
            if d > dis[stage][left][state]:
                continue
            if state == 0:
                for sub in sub_masks[left]:
                    cost = max_time[sub] * mul[stage]
                    push(d + cost, (stage + floor(cost)) % m, left ^ sub, 1)
            else:
                s = (u - 1) ^ left
                while s:
                    lb = s & -s
                    cost = max_time[lb] * mul[stage]
                    push(d + cost, (stage + floor(cost)) % m, left ^ lb, 0)
                    s ^= lb

        return -1