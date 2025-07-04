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
#dfs - stack#
#check top!#

def solve():
    n, m = MI()
    adj = defaultdict(set)
    d = dict()
    res = ['-1' for _ in range(m)]
    degree = [0 for _ in range(n)]

    for i in range(m):
        a, b = MI()
        a -= 1
        b -= 1
        adj[a].add(b)
        adj[b].add(a)
        d[(a, b)] = i
        d[(b, a)] = i
        degree[a] += 1
        degree[b] += 1

    zero = [False for _ in range(n)]
    q = deque()
    for i in range(n):
        if degree[i] == 1:
            q.append(i)

    while q:
        cur = q.popleft()
        for e in adj[cur]:
            if not zero[e]:
                degree[cur] -= 1
                degree[e] -= 1
                if degree[cur] == 0:
                    zero[cur] = True
                if degree[e] == 0:
                    zero[e] = True
                if degree[e] == 1:
                    q.append(e)

                idx = d[(cur, e)]
                res[idx] = '0'
    #print(res)
    
    def calc(node):
        nodes = []
        q = deque()
        v = set()
        q.append(node)
        v.add(node)
        ee = set()

        while q:
            cur = q.popleft()
            nodes.append(cur)
            for e in adj[cur]:
                if not zero[e] and e not in v:
                    v.add(e)
                    q.append(e)
                    ee.add((cur, e))
                    ee.add((e, cur))
                    break
        #print('ee', ee)

        q = deque()
        v = set()
        q.append(node)
        v.add(node)

        while q:
            cur = q.popleft()
            nodes.append(cur)
            for e in adj[cur]:
                if not zero[e]:
                    idx = d[(cur, e)]
                    
                    if (cur, e) in ee:
                        #print('y', cur, e, idx)
                        res[idx] = '0'
                    else:
                        #print('n', cur, e, idx)
                        res[idx] = '1'
                    if e not in v:
                        v.add(e)
                        q.append(e)

        for node in nodes:
            zero[node] = True


    for i in range(n):
        if not zero[i]:
            calc(i)

    print(''.join(res))
            

for _ in range(II()):solve()