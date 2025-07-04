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
from math import ceil
#dfs - stack#

def solve():
    n, m = MI()
    adj = defaultdict(set)
    for _ in range(m):
        s, e = MI()
        adj[s].add(e)
        adj[e].add(s)
    
    def bfs(node):
        distance = [float('inf') for _ in range(n + 1)]
        q = deque()
        v = set()
        q.append(node)
        v.add(node)
        step = 0

        while q:
            k = len(q)
            for _ in range(k):
                cur = q.popleft()
                distance[cur] = step
                for e in adj[cur]:
                    if e != 0 and e not in v:
                        q.append(e)
                        v.add(e)
            step += 1
        return distance

    d1 = bfs(1)
    d2 = bfs(n)

    lstart, rstart = -1, -1
    lval, rval = float('inf'), float('inf')

    for edge in adj[0]:
        if d1[edge] < lval:
            lstart = edge
            lval = d1[edge]
        if d2[edge] < rval:
            rstart = edge
            rval = d2[edge]

    res = [d1[n] for _ in range(n + 1)]
    for edge in range(1, n + 1):
        l, r = d1[edge], d2[edge]
        if lstart != -1:
            l = min(l, d1[lstart] + 1)
        if rstart != -1:
            r = min(r, d2[rstart] + 1)
        res[edge] = min(res[edge], l + r)

    for i in range(1, n + 1):
        if res[i] == float('inf'):
            res[i] = -1
    
    print(*res[1:])
solve()