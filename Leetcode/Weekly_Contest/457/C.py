from typing import *
from collections import *

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Solution:
    def minTime(self, n: int, A: List[List[int]], k: int) -> int:
        mp = defaultdict(list)
        for u, v, t in A:
            mp[t].append((u, v))

        res = inf

        uf = UnionFind(n)
        for t in sorted(list(mp.keys()), reverse = True):
            for u, v in mp[t]:
                uf.Union(u, v)

            # print('t', t, uf.setCount)
            if uf.setCount < k:
                res = t
                break

        return 0 if res == inf else res
        

class UnionFind:
    def __init__(self, n: int):
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.setCount = n
    
    def Find(self, a: int) -> int:
        a = self.parent[a]
        acopy = a
        while a != self.parent[a]:
            a = self.parent[a]
        while acopy != a:
            self.parent[acopy], acopy = a, self.parent[acopy]
        return a
    
    def Union(self, x: int, y: int) -> bool:
        root_x = self.Find(x)
        root_y = self.Find(y)
        if root_x == root_y:
            return False
        if self.size[root_x] > self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_x] = root_y
        self.size[root_y] += self.size[root_x]
        self.setCount -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.Find(x) == self.Find(y)

    def members(self, x):
        root = self.Find(x)
        return [i for i in range(self.n) if self.Find(i) == root]
    
    def roots(self):
        return [i for i, x in enumerate(self.parent) if i == x]
    
    def group_count(self):
        return len(self.roots())
    
    def all_group_members(self):
        mp = defaultdict(list)
        for member in range(self.n):
            mp[self.Find(member)].append(member)
        return mp

class Recoverable_UnionFind:

    def __init__(self, n):
        self.n = n
        self.parent = [i for i in range(self.n)]
        self.size = [1 for _ in range(self.n)]
        self.operation = []
        self.setCount = n
    
    def Find(self, a: int) -> int:
        a = self.parent[a]
        acopy = a
        while a != self.parent[a]:
            a = self.parent[a]
        while acopy != a:
            self.parent[acopy], acopy = a, self.parent[acopy]
        return a
    
    def Union(self, x: int, y: int) -> bool:
        root_x = self.Find(x)
        root_y = self.Find(y)
        if root_x == root_y:
            return False
        if self.size[root_x] > self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_x] = root_y
        self.size[root_y] += self.size[root_x]
        self.operation.append((root_y, root_x))
        self.setCount -= 1
        return True

    def current(self):
        return len(self.operation)

    def rollback(self, history):
        while len(self.operation) > history:
            a, b = self.operation.pop()
            self.parent[b] = b
            self.size[a] -= self.size[b]
            self.setCount += 1