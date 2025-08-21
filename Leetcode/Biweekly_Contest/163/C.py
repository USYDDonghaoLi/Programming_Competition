from typing import List
from heapq import heappop, heappush
inf = float('inf') 

class Solution:
    def minCost(self, n: int, edges: List[List[int]]) -> int:
        D = Dijkstra(n)

        for u, v, w in edges:
            D.addedge(u, v, w)
            D.addedge(v, u, w << 1)

        D.sol(0)

        res = D.distance[-1]

        return -1 if res == inf else res
        
class Dijkstra:
    def __init__(self, n) -> None:
        self.n = n
        self.graph = [[] for _ in range(self.n)]
    
    
    def addedge(self, e1, e2, weight = 1):
        self.graph[e1].append((e2, weight))
        # self.graph[e2].append((e1, weight))
    
    def f(self, u, v):
        return u << 20 ^ v
    
    def sol(self, src):
        self.prev = [-1 for _ in range(self.n)]
        self.distance = [float('inf') for _ in range(self.n)]
        pq = []
        self.distance[src] = 0
        heappush(pq, self.f(0, src))
        
        while pq:
            z = heappop(pq)
            cost, cur = z >> 20, z & 0xfffff
            if cost > self.distance[cur]:
                continue
            for o, c in self.graph[cur]:
                if cost + c < self.distance[o]:
                    heappush(pq, self.f(cost + c, o))
                    self.distance[o] = cost + c
                    self.prev[o] = cur

    def check(self, start, end, flag = False):
        self.sol(start)
        routes = []
        if flag:
            routes = self.checkroute(end)
        return self.distance[end], routes
    
    def checkroute(self, end):
        cur = end
        routes = []
        while cur != -1:
            routes.append(cur)
            cur = self.prev[cur]
        return routes[::-1]