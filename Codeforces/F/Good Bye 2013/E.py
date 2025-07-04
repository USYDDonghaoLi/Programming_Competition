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

eps = 1e-10

def solve(testcase):
    N, M = MI()
    py = [LII() for _ in range(N)]
    res = [0.0 for _ in range(N)]
    x = [0 for _ in range(5005)]
    y = [0 for _ in range(5005)]
    xx = [0 for _ in range(5005)]
    yy = [0 for _ in range(5005)]
    print('py', py)

    for w in range(M):
        n = 4
        x[0] = 0; y[0] = 5005
        x[1] = 0; y[1] = 0
        x[2] = 1; y[2] = 0
        x[3] = 1; y[3] = 5005

        old_area = 0.0
        for id in range(N):
            #print('check', id, w, w + 1)
            xa = 0; ya = py[id][w]
            xb = 1; yb = py[id][w + 1]
            a = yb - ya
            b = xa - xb
            c = -a * xa - b * ya
            nn = 0
            for i in range(n):
                z = a * x[i] + b * y[i] + c
                if z < eps:
                    xx[nn] = x[i]
                    yy[nn] = y[i]
                    nn += 1
                if i < n - 1:
                    zz = a * x[i + 1] + b * y[i + 1] + c
                    if (z < -eps and zz > eps) or (zz < -eps and z > eps):
                        aa = y[i + 1] - y[i]
                        bb = x[i] - x[i + 1]
                        cc = -aa * x[i] - bb * y[i]
                        d = a * bb - b * aa
                        dx = (b * cc - c * bb) / d
                        dy = (c * aa - a * cc) / d
                        xx[nn] = dx
                        yy[nn] = dy
                        nn += 1
            
            n = nn
            for i in range(n):
                x[i] = xx[i]
                y[i] = yy[i]
        
        area = 0.0
        for i in range(n - 1):
            area += (x[i + 1] - x[i]) * (y[i + 1] + y[i])
            area *= 0.5
            res[id] += area - old_area
            old_area = area
    
    print(*res)

for testcase in range(1):
    solve(testcase)