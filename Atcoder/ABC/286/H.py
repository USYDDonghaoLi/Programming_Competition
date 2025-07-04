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

class ConvexHull:
    def __init__(self, points) -> None:
        self.points = sorted(points)
    
    #whether o -> a -> b in convex hull or not#
    def cross(self, o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    #Build lower hull
    def lower(self):
        lowerhull = []
        for p in self.points:
            while len(lowerhull) >= 2 and self.cross(lowerhull[-2], lowerhull[-1], p) <= 0:
                lowerhull.pop()
            lowerhull.append(p)
        return lowerhull
    
    #Build upper hull#
    def upper(self):
        upperhull = []
        for p in reversed(self.points):
            while len(upperhull) >= 2 and self.cross(upperhull[-2], upperhull[-1], p) <= 0:
                upperhull.pop()
            upperhull.append(p)
        return upperhull
    
def solve(testcase):
    n = II()
    points = []
    for _ in range(n):
        a, b = MI()
        points.append((a, b))
    sx, sy = MI()
    points.append((sx, sy))
    tx, ty = MI()
    points.append((tx, ty))

    CH = ConvexHull(points)
    L = CH.lower()
    R = CH.upper()
    #print(L, R)
    TOT = L[:-1] + R[:-1]
    #print(TOT)

    try:
        l = TOT.index((sx, sy))
        r = TOT.index((tx, ty))

        if l > r:
            l, r = r, l
        t1, t2 = 0, 0
        for i in range(l + 1, r + 1):
            t1 += sqrt((TOT[i][0] - TOT[i - 1][0]) ** 2 + (TOT[i][1] - TOT[i - 1][1]) ** 2)
        for i in range(r + 1 - len(TOT), l + 1):
            t2 += sqrt((TOT[i][0] - TOT[i - 1][0]) ** 2 + (TOT[i][1] - TOT[i - 1][1]) ** 2)
        #print(t1, t2)
        res = min(t1, t2)
    except:
        res = sqrt((sx - tx) ** 2 + (sy - ty) ** 2)
    
    print(res)

for testcase in range(1):
    solve(testcase)