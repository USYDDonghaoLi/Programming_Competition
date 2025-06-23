from typing import *

class Solution:
    def minIncrease(self, n: int, edges: List[List[int]], cost: List[int]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        g[0].append(-1)

        def dfs(x: int, fa: int, path_sum: int) -> int:
            path_sum += cost[x]
            if len(g[x]) == 1:
                return path_sum

            max_s = cnt = 0
            for y in g[x]:
                if y == fa:
                    continue
                mx = dfs(y, x, path_sum)
                if mx > max_s:
                    max_s = mx
                    cnt = 1
                elif mx == max_s:
                    cnt += 1

            nonlocal ans
            ans += len(g[x]) - 1 - cnt
            return max_s

        ans = 0
        dfs(0, -1, 0)
        return ans