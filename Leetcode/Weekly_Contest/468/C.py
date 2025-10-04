from typing import *
from collections import deque

class Solution:
    def minSplitMerge(self, A: List[int], B: List[int]) -> int:
        n = len(A)
        A = tuple(A)
        B = tuple(B)
        vis = set()
        q = deque()
        res = 0

        q.append(A)
        vis.add(A)

        while q:
            k = len(q)
            for _ in range(k):
                cur = q.popleft()

                if cur == B:
                    return res
    
                # c = list(cur)
                c = cur
                for l in range(n):
                    for r in range(l, n):
                        add = c[l: r + 1]
                        remaining = c[:l] + c[r + 1:]
                        # print('add, remain', add, remaining)
                        m = len(remaining)
                        for i in range(m + 1):
                            new = remaining[:i] + add + remaining[i:]
                            # new = tuple(new)
                            if new not in vis:
                                vis.add(new)
                                q.append(new)
                            # print('cur, new', cur, new)
            res += 1

        return -1