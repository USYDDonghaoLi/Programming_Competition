from typing import *
from collections import *

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Solution:
    def minOperations(self, s: str, t: str) -> int:
        n = len(s)

        def calc(l, r, rev):

            LEN = r - l + 1
            ss = s[l: l + LEN]
            if rev:
                ss = ss[::-1]
            tt = t[l: l + LEN]

            mp = defaultdict(lambda: defaultdict(lambda: [0, 0]))

            for i in range(LEN):
                x, y = ss[i], tt[i]
                if x < y:
                    mp[x][y][0] += 1
                elif x > y:
                    mp[y][x][1] += 1

            res = 0
            for x in mp:
                for y in mp[x]:
                    res += fmax(mp[x][y][0], mp[x][y][1])

            return res

        f = [inf for _ in range(n + 1)]
        g = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

        for i in range(1, n + 1):
            for j in range(i, n + 1):
                g[i][j] = fmin(calc(i - 1, j - 1, False), calc(i - 1, j - 1, True) + 1)

        f[0] = 0
        for i in range(1, n + 1):
            for j in range(i - 1, -1, -1):
                f[i] = fmin(f[i], f[j] + g[j + 1][i])

        return f[n]