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
from time import *
from random import *
from math import log, gcd
#dfs - stack#
#check top!#

def solve():
    n, m, k = MI()
    edges = []
    for i in range(1, m + 1):
        a, b, c = MI()
        edges.append((a - 1, b - 1, c, i))
    E = LII()

    mp = defaultdict(list)
    for i, v in enumerate(E):
        mp[v].append(i)
    
    adj = defaultdict(list)
    for a, b, c, idx in edges:
        if idx in mp:
            adj[a].append((b, c, idx))
    
    pq = []
    dist = [-1 for _ in range(n)]
    dist[0] = 0
    for b, c, idx in adj[0]:
        heappush(pq, (c, b, idx, mp[idx][0]))
    
    while pq:
        c, b, idx, cur = heappop(pq)
        if dist[b] == -1:
            dist[b] = c
            for bb, cc, idxx in adj[b]:
                if dist[bb] == -1:
                    j = bisect_right(mp[idxx], cur)
                    if j == len(mp[idxx]):
                        continue
                    else:
                        heappush(pq, (c + cc, bb, idxx, mp[idxx][j]))
    
    print(dist[-1])

for _ in range(1):solve()

