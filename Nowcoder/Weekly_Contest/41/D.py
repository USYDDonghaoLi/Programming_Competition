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

# '''
# 手写栈防止recursion limit
# 注意要用yield 不要用return
# 函数结尾要写yield None
# '''
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

# RANDOM = getrandbits(32, seed = 19981220)
 
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



# @TIME
def solve(testcase):
    n, q = MI()
    s = I()

    rc, ec, dc = [0 for _ in range(n + 1)], [0 for _ in range(n + 1)], [0 for _ in range(n + 1)]

    for i, v in enumerate(s, 1):
        rc[i] = rc[i - 1]
        ec[i] = ec[i - 1]
        dc[i] = dc[i - 1]

        if v == 'r':
            rc[i] += 1
        elif v == 'e':
            ec[i] += 1
        else:
            dc[i] += 1
    
    def getr(l, r):
        return rc[r + 1] - rc[l]
    
    def gete(l, r):
        return ec[r + 1] - ec[l]

    def getd(l, r):
        return dc[r + 1] - dc[l]


    def calc(l, r, a, b, c):
        return (a - getr(l, l + a - 1)) + (b - gete(l + a, l + a + b - 1) + (c - getd(l + a + b, l + a + b + c - 1)))

    for _ in range(q):
        l, r = MI()
        l -= 1
        r -= 1

        res = inf
        LEN = r - l + 1
        if LEN < 3:
            print(0)
            continue
        
        a = LEN // 3
        if LEN % 3 == 0:
            res = min(res, calc(l, r, a, a, a))
        elif LEN % 3 == 1:
            res = min(res, calc(l, r, a + 1, a, a))
            res = min(res, calc(l, r, a, a + 1, a))
            res = min(res, calc(l, r, a, a, a + 1))
        else:
            res = min(res, calc(l, r, a + 1, a + 1, a))
            res = min(res, calc(l, r, a + 1, a, a + 1))
            res = min(res, calc(l, r, a, a + 1, a + 1))
        
        print(res)

for testcase in range(1):
    solve(testcase)