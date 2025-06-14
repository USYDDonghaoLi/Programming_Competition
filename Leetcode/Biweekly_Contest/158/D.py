from typing import *
from collections import *

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Solution:
    def goodSubtreeSum(self, val: List[int], par: List[int]) -> int:
        n = len(val)
        adj = defaultdict(list)
        dp = [defaultdict(int) for _ in range(n)]
        # A = [0 for _ in range(n)]

        for i, v in enumerate(val):
            dp[i][0] = 0
            state = 0
            vv = v
            while v:
                t = v % 10
                v //= 10
                if state >> t & 1:
                    break
                else:
                    state |= 1 << t
            else:
                dp[i][state] = vv

        # print('dp', dp)

        for i, v in enumerate(par):
            if v != -1:
                adj[v].append(i)

        res = 0
        mod = 10 ** 9 + 7
        
        def dfs(u):
            nonlocal res
            ans = 0
            for v in adj[u]:
                dfs(v)
                newdp = defaultdict(int)
                newdp[0] = 0
                for uv in dp[u]:
                    newdp[uv] = fmax(newdp[uv], dp[u][uv])
                    for vv in dp[v]:
                        if vv & uv == 0:
                            newdp[vv ^ uv] = fmax(newdp[uv ^ vv], dp[u][uv] + dp[v][vv])
                dp[u] = newdp

                # print('dp', dp[u])

            for v in dp[u]:
                ans = fmax(ans, dp[u][v])

            # print('ans', u, ans)

            res = (res + ans) % mod

        dfs(0)

        return res