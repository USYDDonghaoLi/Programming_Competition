from typing import *
from collections import *
inf = float('inf')

class Solution:
    def findMaxPathScore(self, E: List[List[int]], B: List[bool], k: int) -> int:
        n = len(B)

        edges = []

        for u, v, c in E:
            if B[u] and B[v]:
                edges.append((u, v, c))

        edges.sort(key = lambda x: -x[2])

        adj = [[] for _ in range(n)]
        dist = [inf for _ in range(n)]
        dist[0] = 0

        for u, v, c in edges:
            adj[u].append((v, c))

            if dist[u] + c < dist[v]:
                dist[v] = dist[u] + c
                q = deque()
                q.append(v)

                while q:
                    cur = q.popleft()
                    for o, cc in adj[cur]:
                        if dist[cur] + cc < dist[o]:
                            dist[o] = dist[cur] + cc
                            q.append(o)
                
            # print(u, v, c, k, dist)
            
            if dist[n - 1] <= k:
                return c

        return -1