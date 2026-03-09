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
    n, x1, y1, x2, y2 = MI()
    ans = []
    y = y1
    if x1 == x2:
        if abs(y1 - y2 + 1) & 1:
            exit(print(-1))
        if y1 < y2:
            ans.append("L" * (y - 1))
            y = 1
            ans.append("U" if x1 == 2 else "D")
            ans.append("R" * (y1 - y + 1))
            y = y1
            if x1 == 2:
                ans.append("DRUR" * ((y2 - y) // 2))
            else:
                ans.append("URDR" * ((y2 - y) // 2))
            y = y2
            ans.append("R" * (n - y))
            y = n
            ans.append("D" if x1 == 2 else "U")
            ans.append("L" * (n - y2))
        else:
            ans.append("R" * (n - y))
            y = n
            ans.append("U" if x1 == 2 else "D")
            ans.append("L" * (y - y1 + 1))
            y = y1
            if x1 == 2:
                ans.append("DLUL" * ((y - y2) // 2))
            else:
                ans.append("ULDL" * ((y- y2) // 2))
            y = y2
            ans.append("L" * (y - 1))
            y = 1
            ans.append("D" if x1 == 2 else "U")
            ans.append("R" * (y2 - 1))
    if x1 != x2:
        if y1 == y2:
            if y1 != 1 and y1 != n:
                exit(print(-1))
            elif y1 == 1:
                exit(print("R" * (n - 1) + ("U" if x1 == 2 else "D") + "L" * (n - 1)))
            else:
                exit(print("L" * (n - 1) + ("U" if x1 == 2 else "D") + "R" * (n - 1)))
        if abs(y1 - y2) & 1:
            exit(print(-1))
        if y1 < y2:
            ans.append("L" * (y - 1))
            y = 1
            ans.append("U" if x1 == 2 else "D")
            ans.append("R" * (y1 - y + 1))
            ans.append("U" if x1 == 1 else "D")
            ans.append("R")
            y = y1 + 2
            if x1 == 1:
                ans.append("DRUR" * ((y2 - y) // 2))
            else:
                ans.append("URDR" * ((y2 - y) // 2))
            y = y2
            ans.append("R" * (n - y))
            y = n
            ans.append("D" if x1 == 1 else "U")
            ans.append("L" * (n - y2))
        else:
            ans.append("R" * (n - y))
            y = n
            ans.append("U" if x1 == 2 else "D")
            ans.append("L" * (y - y1 + 1))
            ans.append("U" if x1 == 1 else "D")
            ans.append("L")
            y = y1 - 2
            if x1 == 1:
                ans.append("DLUL" * ((y - y2) // 2))
            else:
                ans.append("ULDL" * ((y - y2) // 2))
            y = y2
            ans.append("L" * (y - 1))
            y = 1
            ans.append("D" if x1 == 1 else "U")
            ans.append("R" * (y2 - 1))
    print("".join(ans))


        

for testcase in range(II()):
    solve(testcase)