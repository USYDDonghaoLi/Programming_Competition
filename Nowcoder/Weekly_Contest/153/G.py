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
    n, m, k = MI()

    if k == 0:
        if n >= 2 and m >= 2:
            print("No")
        else:
            print("Yes")
            res = [['0' for _ in range(m)] for _ in range(n)]
            for r in res:
                print(''.join(r))
        return

    lim1 = (n >> 1) * (m >> 1)
    if k <= lim1:
        res = [['0' for _ in range(m)] for _ in range(n)]
        ok = []
        for i in range(1, n, 2):
            for j in range(1, m, 2):
                res[i][j] = '1'
                if j + 2 < m:
                    ok.append((i, j + 1))
                if i + 2 < n and j == 1:
                    ok.append((i + 1, j))
        
        cur = lim1
        idx = 0
        while cur > k and idx < len(ok):
            x, y = ok[idx]
            res[x][y] = '1'
            cur -= 1
            idx += 1
        
        print("Yes")
        for r in res:
            print(''.join(r))
    
        return
    
    lim2 = 0
    res = [['0' for _ in range(m)] for _ in range(n)]
    ok = []
    for i in range(n):
        for j in range(i & 1, m, 2):
            res[i][j] = '1'
            lim2 += 1
    for i in range(0, n, 2):
        for j in range(m):
            if res[i][j] == '1':
                ok.append((i, j))
    
    if k > lim2:
        print("No")
    else:
        cur = lim2
        idx = 0
        while cur > k and idx < len(ok):
            x, y = ok[idx]
            res[x][y] = '0'
            cur -= 1
            idx += 1
        
        print("Yes")
        for r in res:
            print(''.join(r))

for testcase in range(1):
    solve(testcase)