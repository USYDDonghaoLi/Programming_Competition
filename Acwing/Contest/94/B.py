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
    n, m = MI()
    adj = defaultdict(list)
    for _ in range(m):
        a, b, c = MI()
        adj[a].append((b, c))
        adj[b].append((a, c))
    stop = defaultdict(set)
    for i in range(1, n):
        _, *nums = LII()
        for t in nums:
            stop[i].add(t)
    _ = LII()
    
    dist = [float('inf') for _ in range(n + 1)]
    q = deque()
    time = 0
    while time in stop[1]:
        time += 1
    q.append(1)
    dist[1] = time

    # d = dict()
    # @bootstrap
    # def calc(where, time):
    #     if time in where:
    #         if (where, time + 1) not in d:
    #             yield calc(where, time + 1)
    #         d[(where, time)] = d[(where, time + 1)]
    #     else:
    #         d[(where, time)] = time

    while q:
        cur = q.popleft()
        for o, c in adj[cur]:
            nc = dist[cur] + c
            while nc in stop[o]:
                nc += 1
            if nc < dist[o]:
                dist[o] = nc
                q.append(o)
    
    if dist[n] == float('inf'):
        print(-1)
    else:
        print(dist[n])

for testcase in range(1):
    solve(testcase)