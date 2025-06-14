from typing import *
from collections import *
from math import gcd

class Solution:
    def maxGCDScore(self, nums: List[int], k: int) -> int:
        lowbit_pos = defaultdict(list)

        ans = 0
        intervals = []
        for i, x in enumerate(nums):
            lowbit_pos[x & -x].append(i)

            for p in intervals:
                p[0] = gcd(p[0], x)
            intervals.append([x, i - 1, i])

            idx = 1
            for j in range(1, len(intervals)):
                if intervals[j][0] != intervals[j - 1][0]:
                    intervals[idx] = intervals[j]
                    idx += 1
                else:
                    intervals[idx - 1][2] = intervals[j][2]
            del intervals[idx:]

            for g, l, r in intervals:

                ans = max(ans, g * (i - l))

                pos = lowbit_pos[g & -g]
                min_l = max(l, pos[-k - 1]) if len(pos) > k else l
                if min_l < r: 
                    ans = max(ans, g * 2 * (i - min_l))

        return ans