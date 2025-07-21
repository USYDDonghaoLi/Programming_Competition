from typing import *
from collections import *

class Solution:
    def countIslands(self, A: List[List[int]], k: int) -> int:
        n, m = len(A), len(A[0])
        vis = [[False for _ in range(m)] for _ in range(n)]
        res = 0

        d = ((1, 0), (-1, 0), (0, 1), (0, -1))

        def bfs(x, y):
            vis[x][y] = True
            ans = 0
            q = deque()
            q.append((x, y))

            while q:
                x, y = q.popleft()
                ans += A[x][y]

                for dx, dy in d:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < m and A[nx][ny] != 0 and not vis[nx][ny]:
                        vis[nx][ny] = True
                        q.append((nx, ny))

            return ans % k == 0

        for i in range(n):
            for j in range(m):
                if A[i][j]:
                    if not vis[i][j]:
                        res += bfs(i, j)

        return res