import sys
import os
from io import BytesIO, IOBase
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

def I():
    return input()
def II():
    return int(input())
def MI():
    return map(int, input().split())
def LI():
    return list(input().split())
def LII():
    return list(map(int, input().split()))
def GMI():
    return map(lambda x: int(x) - 1, input().split())

#------------------------------FastIO---------------------------------

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
#dfs - stack#

class UnionFind:
    def __init__(self, n: int):
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.setCount = n
    
    def Find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.Find(self.parent[x])
        return self.parent[x]
    
    def Union(self, x: int, y: int) -> bool:
        root_x = self.Find(x)
        root_y = self.Find(y)
        if root_x == root_y:
            return False
        if self.size[root_x] > self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_x] = root_y
        self.size[root_y] += self.size[root_x]
        self.setCount -=1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.Find(x) == self.Find(y)

def solve():
    n, m = MI()
    grid = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        line = LII()
        for j in range(m):
            grid[i][j] = line[j]
    
    
    d = ((1, 0), (0, 1), (-1, 0), (0, -1))
    uf = UnionFind(m * n)
    roots = []
    
    cur = 1    
    while cur < m * n + 1:
        root = mp[cur]
        x, y = divmod(root, m)
        roots.append(cur)
        cur += 1
        while cur < m * n + 1:
            flag = False
            nxt = mp[cur]
            x, y = divmod(nxt, m)
            for dx, dy in d:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m:
                    if uf.connected(root, nx * m + ny):
                        flag = True
                        uf.Union(root, x * m + y)
                        cur += 1
                        break
            if not flag:
                break
    print(uf.setCount)
    
    if len(roots) > 3:
        print(2)
    elif len(roots) == 3:
        alone = 0
        for root in roots:
            if uf.size[uf.Find(root)] == 1:
                alone = root
        if not alone:
            print(2)
        else:
            print(1)
    elif len(roots) == 2:
        if n == 1 or m == 1:
            print(2)
        else:
            print(1)
    else:
        print(0)
solve()