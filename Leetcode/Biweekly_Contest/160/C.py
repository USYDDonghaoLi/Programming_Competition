from typing import *
from heapq import *

inf = float('inf')

class Solution:
    def minTime(self, n: int, edges: List[List[int]]) -> int:
        adj = [[] for _ in range(n)]
        for u, v, s, e in edges:
            adj[u].append((v, s, e))
        
        pq = []
        heappush(pq, (0, 0))

        A = [inf for _ in range(n)]
        A[0] = 0

        while pq:
            t, u = heappop(pq)
            if A[u] < t:
                continue

            for v, s, e in adj[u]:
                if t > e:
                    pass
                elif t >= s:
                    nt = t + 1
                    if A[v] > nt:
                        A[v] = nt
                        heappush(pq, (nt, v))
                else:
                    nt = s + 1
                    if A[v] > nt:
                        A[v] = nt
                        heappush(pq, (nt, v))
        
        res = A[-1]

        return -1 if res == inf else res