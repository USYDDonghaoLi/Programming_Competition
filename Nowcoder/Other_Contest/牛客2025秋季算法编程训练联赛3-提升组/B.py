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
    n = II()

    # mp = defaultdict(int)

    # def f(n, a, b, c):
    #     if n == 1:
    #         mp[a + c] += 1
    #     else:
    #         f(n - 1, a, c, b)
    #         mp[a + c] += 1
    #         f(n - 1, b, a, c)
    
    for i in range(n, n + 1):
        # mp.clear()
        # f(i, "a", "b", "c")
        # print('mp', mp)

        k = (i >> 1) - 1
        if i == 1:
            ab = 0
        else:
            ab = (3 * k + 1 + pow(2, 2 * k + 3)) // 9
        # assert ab == mp["ab"], f"{i} {ab} {mp["ab"]}"

        kk = i - 1 >> 1
        ac = (pow(4, kk + 1) + 6 * kk + 5) // 9
        # assert ac == mp["ac"], f"{i} {ac} {mp["ac"]}"

        kba = i - 1 >> 1
        ba = (pow(4, kba + 1) - 3 * kba - 4) // 9
        # assert ba == mp["ba"], f"{i} {ba} {mp["ba"]}"

        kbc = i - 2 >> 1
        bc = (3 * kbc + 1 + pow(2, 2 * kbc + 3)) // 9
        # assert bc == mp["bc"], f"{i} {bc} {mp["bc"]}"

        kca = i - 2 >> 1
        ca = 2 * (pow(4, kca + 1) - 3 * kca - 4) // 9
        # assert ca == mp["ca"], f"{i} {ca} {mp["ca"]}"

        kcb = i - 1 >> 1
        cb = (pow(4, kcb + 1) - 3 * kcb - 4) // 9
        # assert cb == mp["cb"], f"{i} {cb} {mp["cb"]}"

        print(f"A->B:{ab}")
        print(f"A->C:{ac}")
        print(f"B->A:{ba}")
        print(f"B->C:{bc}")
        print(f"C->A:{ca}")
        print(f"C->B:{cb}")

        print(f"SUM:{pow(2,i) - 1}")


for testcase in range(1):
    solve(testcase)