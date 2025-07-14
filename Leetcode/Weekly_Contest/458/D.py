fmax = lambda a, b: b if b > a else a

from typing import *
from functools import *

class Solution:
    def maxLen(self, n: int, edges: List[List[int]], label: str) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        @cache
        def dfs(x: int, y: int, vis: int) -> int:
            res = 0
            for v in g[x]:
                if vis >> v & 1:
                    continue
                for w in g[y]:
                    if vis >> w & 1 == 0 and v != w and label[w] == label[v]:
                        tv, tw = v, w
                        if tv > tw:
                            tv, tw = tw, tv
                        res = max(res, dfs(tv, tw, vis | 1 << v | 1 << w) + 2)
            return res

        ans = 0
        for x, to in enumerate(g):

            ans = max(ans, dfs(x, x, 1 << x) + 1)
            if ans == n:
                return n

            for y in to:

                if x < y and label[x] == label[y]:
                    ans = max(ans, dfs(x, y, 1 << x | 1 << y) + 2)
                    if ans == n:
                        return n
        return ans