'''
Hala Madrid!
https://github.com/USYDDonghaoLi/Programming_Competition
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
def LGMI():
    return list(map(lambda x: int(x) - 1, input().split()))

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

D1 = 669 * 4
D2 = 669 * 2

def INRANGE(x, y):
    return 0 <= x <= 4 and -2 <= y <= 2

def DAMAGE(x, y):
    if INRANGE(x, y):
        return D1
    else:
        return D2

def ATTACKRANGE(x, y):
    res = []

    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if abs(dx) + abs(dy) <= 2:
                res.append((x + dx, y + dy))
    
    return res

d = ((1, 0), (0, 1), (-1, 0), (0, -1))

# @TIME
def solve(testcase):

    mp = defaultdict(set)
    mp2 = defaultdict(list)
    mp3 = defaultdict(bool)

    n = II()
    for _ in range(n):
        x, y = MI()
        ar = ATTACKRANGE(x, y)
        for xx, yy in ar:
            mp[(xx, yy)].add((x, y))
            mp2[(x, y)].append((xx, yy))
        mp3[(x, y)] = True

    m = II()
    for _ in range(m):
        x, y = MI()

        if (x, y) in mp3 and mp3[(x, y)]:
            continue
        
        ar = ATTACKRANGE(x, y)
        for xx, yy in ar:
            mp[(xx, yy)].add((x, y))
            mp2[(x, y)].append((xx, yy))
        mp3[(x, y)] = True
        
        if INRANGE(x, y):
            for dx, dy in d:
                nx, ny = x + dx, y + dy
                if not (nx == 0 and ny == 0) and (nx, ny) not in mp3:

                    ar2 = ATTACKRANGE(nx, ny)
                    for xx, yy in ar2:
                        mp[(xx, yy)].add((nx, ny))
                        mp2[(nx, ny)].append((xx, yy))
                    mp3[(nx, ny)] = True
    
        # print('mp3', mp3)
    
    q = II()
    for _ in range(q):
        x, y = MI()
        # print('attack', x, y, mp[(x, y)])

        res = 0
        for ax, ay in mp[(x, y)]:
            if mp3[(ax, ay)]:
                res += DAMAGE(ax, ay)
                mp3[(ax, ay)] = False
        
        print(res)


for testcase in range(1):
    solve(testcase)