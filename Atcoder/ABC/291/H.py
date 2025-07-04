'''
Hala Madrid!
https://www.zhihu.com/people/li-dong-hao-78-74
'''

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
from math import log, gcd, sqrt, ceil

'''
手写栈防止recursion limit
注意要用yield 不要用return
函数结尾要写yield None
'''
from types import GeneratorType
def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc

RANDOM = getrandbits(32)
 
class Wrapper(int):
    def __init__(self, x):
        int.__init__(x)
 
    def __hash__(self):
        return super(Wrapper, self).__hash__() ^ RANDOM

def solve(testcase):
    n = II()
    adj = defaultdict(set)
    for _ in range(n - 1):
        a, b = MI()
        adj[a].add(b)
        adj[b].add(a)
    
    sz = defaultdict(int)
    weight = defaultdict(int)
    centroid = 0
    res = [-1 for _ in range(n + 1)]
    visited = [False for _ in range(n + 1)]

    @bootstrap
    def GetCentroid(cur, fa, tot):
        nonlocal centroid
        sz[cur] = 1
        weight[cur] = 0
        for o in adj[cur]:
            if o == fa or visited[o]:
                continue
            else:
                yield GetCentroid(o, cur, tot)
                sz[cur] += sz[o]
                weight[cur] = max(weight[cur], sz[o])
        weight[cur] = max(weight[cur], tot - sz[cur])
        if weight[cur] <= tot // 2:
            centroid  = cur
        yield None
    
    GetCentroid(1, 0, n)

    res = [-1 for _ in range(n + 1)]
    q = deque()
    q.append((centroid, -1))

    while q:
        # print('q', q)
        cur, fa = q.popleft()
        visited[cur] = True
        res[cur] = fa
        for o in adj[cur]:
            if o == fa:
                continue
            else:
                adj[o].discard(cur)

                tot = 0
                qt = deque()
                qt.append((o, 0))
                while qt:
                    ccur, fa = qt.popleft()
                    tot += 1
                    for oo in adj[ccur]:
                        if visited[oo] or oo == fa:
                            continue
                        else:
                            qt.append((oo, ccur))

                sz.clear()
                weight.clear()
                GetCentroid(o, cur, tot)
                q.append((centroid, cur))
        # adj[cur].clear()

    print(*res[1:])


for testcase in range(1):
    solve(testcase)