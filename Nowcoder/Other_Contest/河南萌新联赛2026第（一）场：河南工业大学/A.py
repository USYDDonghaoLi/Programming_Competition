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

# @TIME
def solve(testcase):
    n, m = MI()

    C = LII()
    q = deque()
    for i in range(n):
        q.append((i, 0, 0))

    A = [0 for _ in range(m)]
    P = [0 for _ in range(m)]
    T = [0 for _ in range(m)]

    for i in range(m):
        a = LII()
        A[i] = a[0]
        if a[0] == 1:
            P[i] = a[1]
            T[i] = a[2]
    
    bankrupt = set()

    k = II()
    D = LII()

    COIN = [C[i] for i in range(n)]
    HOUSE = [0 for _ in range(n)]
    BELONG = [-1 for _ in range(m)]
    mp = defaultdict(list)

    idx = 0

    while idx < k:
        if len(q) == 1:
            break
        user, where, state = q.popleft()
        if state == 1:
            q.append((user, where, 0))
            continue

        d = D[idx]

        newplace = (where + d) % m
        what = A[newplace]

        if what == 0:
            COIN[user] += 200
            q.append((user, newplace, 0))
        elif what == 1:
            owner = BELONG[newplace]
            if owner == -1:
                price = P[newplace]
                if COIN[user] >= price:
                    COIN[user] -= price
                    BELONG[newplace] = user
                    HOUSE[user] += 1
                    mp[user].append(newplace)

                q.append((user, newplace, 0))

            elif owner == user:
                q.append((user, newplace, 0))

            else:
                toll = T[newplace]
                if COIN[user] >= toll:
                    COIN[user] -= toll
                    COIN[owner] += toll
                    q.append((user, newplace, 0))
                else:
                    COIN[owner] += COIN[user]
                    COIN[user] -= toll
                    HOUSE[user] = 0
                    for house in mp[user]:
                        BELONG[house] = -1

        elif what == 2:
            COIN[user] += 150
            q.append((user, newplace, 0))
        elif what == 3:
            COIN[user] -= 100
            if COIN[user] >= 0:
                q.append((user, newplace, 0))
            else:
                HOUSE[user] = 0
                for house in mp[user]:
                    BELONG[house] = -1
        else:
            assert what == 4
            q.append((user, newplace, 1))
        
        idx += 1
        
    for i in range(n):
        if COIN[i] >= 0:
            print(COIN[i], HOUSE[i])
        else:
            print("bankrupt 0")


for testcase in range(1):
    solve(testcase)