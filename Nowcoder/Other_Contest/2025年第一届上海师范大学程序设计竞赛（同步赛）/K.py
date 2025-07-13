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

# from types import GeneratorType
# def bootstrap(f, stack=[]):
#     def wrappedfunc(*args, **kwargs):
#         if stack:
#             return f(*args, **kwargs)
#         else:
#             to = f(*args, **kwargs)
#             while True:
#                 if type(to) is GeneratorType:
#                     stack.append(to)
#                     to = next(to)
#                 else:
#                     stack.pop()
#                     if not stack:
#                         break
#                     to = stack[-1].send(to)
#             return to
#     return wrappedfunc

# seed(19981220)
# RANDOM = getrandbits(64)
 
# class Wrapper(int):
#     def __init__(self, x):
#         int.__init__(x)

#     def __hash__(self):
#         return super(Wrapper, self).__hash__() ^ RANDOM

# def TIME(f):

#     def wrap(*args, **kwargs):
#         s = perf_counter()
#         ret = f(*args, **kwargs)
#         e = perf_counter()

#         print(e - s, 'sec')
#         return ret
    
#     return wrap

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

cnt = [0 for _ in range(3)]
ccnt = [0 for _ in range(10)]
t = [0 for _ in range(10)]

def work(x, y, z, m):
    if cnt[1] < x or cnt[2] < y or cnt[0] < z or x + y + z > m:
        return '-1'
    
    g = [0 for _ in range(3)]
    for i in range(3):
        g[i] = cnt[i]
    
    while g[1] % 3 != x:
        g[1] -= 1
    
    while g[2] % 3 != y:
        g[2] -= 1
    
    for i in range(9, -1, -1):
        t[i] = 0

    res = m - x - y - z

    i = 9
    while i >= 0:
        tt = fmin(z, ccnt[i] - t[i])
        z -= tt
        t[i] += tt
        g[i % 3] -= tt
        i -= 3
    
    i = 8
    while i >= 0:
        tt = fmin(y, ccnt[i] - t[i])
        y -= tt
        t[i] += tt
        g[i % 3] -= tt
        i -= 3
    
    i = 7
    while i >= 0:
        tt = fmin(x, ccnt[i] - t[i])
        x -= tt
        t[i] += tt
        g[i % 3] -= tt
        i -= 3
    
    while res >= 3:

        px, py, pz = -1, -1, -1

        if g[0] >= 3:

            i = 9
            while i >= 0:
                if t[i] != ccnt[i]:
                    pz = i
                    break
                i -= 3
            
        if g[2] >= 3:

            i = 8
            while i >= 0:
                if t[i] != ccnt[i]:
                    py = i
                    break
                i -= 3
        
        if g[1] >= 3:

            i = 7
            while i >= 0:
                if t[i] != ccnt[i]:
                    px = i
                    break
                i -= 3
        
        if pz > px and pz > py:
            z = 3
            i = 9
            while i >= 0:
                tt = fmin(z, ccnt[i] - t[i])
                z -= tt
                t[i] += tt
                g[i % 3] -= tt
                i -= 3
            
        if py > px and py > pz:
            y = 3
            i = 8
            while i >= 0:
                tt = fmin(y, ccnt[i] - t[i])
                y -= tt
                t[i] += tt
                g[i % 3] -= tt
                i -= 3
        
        if px > pz and py > pz:
            x = 3
            i = 7
            while i >= 0:
                tt = fmin(x, ccnt[i] - t[i])
                x -= tt
                t[i] += tt
                g[i % 3] -= tt
                i -= 3
        
        res -= 3
    
    now = []
    for i in range(9, -1, -1):
        for _ in range(t[i]):
            now.append(str(i))

    if len(now) == 0:
        return '-1'
    if now[0] == '0':
        return '0'

    return ''.join(now) 

# @TIME
def solve(testcase):
    n, m = MI()
    s = LII()

    for c in s:
        cnt[c % 3] += 1
        ccnt[c] += 1
    
    ans = '-1'

    for x in range(3):
        for y in range(3):
            for z in range(3):
                if (x + 2 * y) % 3 == 0:
                    now = work(x, y, z, m)
                    if now != '-1':
                        if ans == '-1':
                            ans = now

                        else:
                            ans = max(ans, now, key=lambda x: (len(x), x))
    
    print(ans)

    for i in range(3):
        cnt[i] = 0 
    for i in range(9):
        ccnt[i] = 0

for testcase in range(II()):
    solve(testcase)