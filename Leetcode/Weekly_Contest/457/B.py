from typing import *
from collections import *

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Solution:
    def processQueries(self, n: int, A: List[List[int]], Q: List[List[int]]) -> List[int]:
        adj = [[] for _ in range(n)]
        for u, v in A:
            u -= 1
            v -= 1
            adj[u].append(v)
            adj[v].append(u)

        state = [0 for _ in range(n)]

        for op, x in Q:
            if op == 2:
                state[x - 1] += 1

        uf = UnionFind(n)

        for u in range(n):
            for v in adj[u]:
                uf.Union(u, v)

        mp = defaultdict(lambda: inf)
        # mp2 = defaultdict(int)

        groups = uf.all_group_members()
        # print('groups', groups)

        for rt in groups:
            for o in groups[rt]:
                if not state[o]:
                    # mp2[rt] += 1
                    mp[rt] = fmin(mp[rt], o)

        # print('mp', mp)

        res = []
        for op, x in reversed(Q):
            x -= 1
            if op == 1:
                if not state[x]:
                    res.append(x + 1)
                else:
                    rt = uf.Find(x)
                    ans = mp[rt]
                    if ans == inf:
                        res.append(-1)
                    else:
                        res.append(ans + 1)
            else:
                state[x] -= 1
                if not state[x]:
                    rt = uf.Find(x)
                    mp[rt] = fmin(mp[rt], x)

            # print('mp', mp)

        return res[::-1]
        

class UnionFind:
    def __init__(self, n: int):
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.setCount = n
        # self.m = [x for x in range(n)]
    
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
        # self.m[root_y] = fmin(self.m[root_y], self.m[root_x])
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