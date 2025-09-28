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

d = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}
dd = {'U': 0, 'D': 1, 'L': 2, 'R': 3}

# @TIME
def solve(testcase):
    n, q = MI()
    s = I()

    pos = [[0 for _ in range(2)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        v = d[s[i - 1]]
        pos[i][0] = pos[i - 1][0] + v[0]
        pos[i][1] = pos[i - 1][1] + v[1]
    
    mp = defaultdict(int)
    mp2 = defaultdict(int)

    for i in range(1, n + 1):
        p = pos[i]
        if p not in mp:
            mp[p] = i
        mp2[p] = i
    
    A = [[] for _ in range(4)]

    for j in range(1, n + 1):
        A[dd[s[j - 1]]].append(j)
    
    cnt = [0 for _ in range(4)]

    for c in s:
        cnt[dd[c]] += 1
    
    dx = cnt[3] - cnt[2]
    dy = cnt[0] - cnt[1]

    has_h = cnt[2] + cnt[3] > 0
    has_v = cnt[0] + cnt[1] > 0

    for i in range(q):
        px, py = MI()

        if (px, py) not in mp:
            print(0)
            continue
        
        k_min = mp[(px, py)]

        flag = False

        if not has_v:
            if py:
                flag = False
            else:
                flag = (px > 0 and dx >= px) or (px < 0 and dx <= px)
        elif not has_h:
            if px:
                flag = False
            else:
                flag = (py > 0 and dy >= py) or (py < 0 and dy <= py)
        else:
            flag = px == dx and py == dy
        
        if not flag:
            print(1)
            continue
            
        
        flag2 = False

        for oc in 'UDLR':
            for nc in 'UDLR':
                if oc != nc:
                    dv = d[nc]
                    ov = d[oc]
                    delta = (dv[0] - ov[0], dv[1] - ov[1])
                    t = (px - delta[0], py - delta[1])

                    last = 0
                    

for testcase in range(1):
    solve(testcase)