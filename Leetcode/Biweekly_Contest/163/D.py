fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

from typing import List
inf = float('inf')

class Solution:
    def minCost(self, A: List[List[int]], k: int) -> int:
        n = len(A)
        m = len(A[0])
        dist = [
            [[inf for _ in range(m)] for _ in range(n)] for _ in range(k + 1)
        ]

        nodes = []
        for i in range(n):
            for j in range(m):
                nodes.append((i, j))

        dist[0][0][0] = 0

        for kk in range(k + 1):
            if kk:
                nodes.sort(key = lambda x: (-A[x[0]][x[1]], dist[kk - 1][x[0]][x[1]]))
                mm = inf

                for x, y in nodes:
                    mm = fmin(mm, dist[kk - 1][x][y])
                    dist[kk][x][y] = fmin(dist[kk][x][y], mm)
            
                # print('fuck', kk, dist[kk])

            for xx in range(n):
                for yy in range(m):
                    if xx:
                        dist[kk][xx][yy] = fmin(dist[kk][xx][yy], dist[kk][xx - 1][yy] + A[xx][yy])
                    if yy:
                        dist[kk][xx][yy] = fmin(dist[kk][xx][yy], dist[kk][xx][yy - 1] + A[xx][yy])

        res = inf

        # print(dist[0])
        # print(dist[1])

        for kk in range(k + 1):
            # print(kk, dist[kk][n - 1][m - 1])
            res = fmin(res, dist[kk][n - 1][m - 1])

        return res