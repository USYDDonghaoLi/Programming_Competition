'''

差分约束
xi1 - xj1 <= y1
xi2 - xj2 <= y2
...

'''

from collections import *

class differenceconstraint:

    def __init__(self, n, w = 0) -> None:
        '''
        因为需要添加虚拟源点，所以下标从1开始。
        '''
        self.n = n
        self.dist = [float('inf') for _ in range(self.n + 1)]
        self.graph = defaultdict(list)
        self.in_queue = [False for _ in range(self.n + 1)]
        self.cnt = [0 for _ in range(self.n + 1)]

        '''
        满足x1,x2,...,xn <= w 的最大解
        '''
        for i in range(1, self.n + 1):
            self.graph[0].append((i, w))
    
    def add(self, FROM, TO, w):
        '''
        xi - yi < ci
        则add(yi, xi, ci)
        '''
        self.graph[FROM].append((TO, w))
        pass

    def SPFA(self, s, n):
        q = deque()
        self.dist[s] = 0
        q.append(s)

        while q:
            p = q.popleft()
            '''
            有负环，不等式无解
            '''
            if self.cnt[p] > n:
                return False
            self.in_queue[p] = False

            for o, w in self.graph[p]:
                if self.dist[p] + w < self.dist[o]:
                    self.dist[o] = self.dist[p] + w
                    if not self.in_queue[o]:
                        q.append(o)
                        self.in_queue[o] = True
                        self.cnt[o] += 1
        return True

    def go(self):
        '''
        True, 则dist为解。
        '''
        return self.SPFA(0, self.n)