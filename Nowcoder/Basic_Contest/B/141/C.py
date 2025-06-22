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

# @TIME
def solve(testcase):
    s, x = LI()
    x = int(x)

    s = [ord(c) - 97 for c in s]
    n = len(s)

    cnt = [
        [0 for _ in range(26)] for _ in range(n + 1)
    ]

    A = [0 for _ in range(n + 1)]

    for i, v in enumerate(s, 1):
        for j in range(26):
            if j == v:
                cnt[i][j] = cnt[i - 1][j] + 1
            else:
                cnt[i][j] = cnt[i - 1][j]
        A[i] = A[i - 1]
        for j in range(v + 1, 26):
            A[i] += cnt[i][j]
    
    # print('A', A)

    def calc(mid, r):
        mid += 1
        r += 1

        tot = [cnt[r][j] for j in range(26)]
        left = [cnt[mid - 1][j] for j in range(26)]
        right = [t - l for t, l in zip(tot, left)]

        sub = 0
        cur = 0
        for j in range(24, -1, -1):
            cur += left[j + 1]
            sub += right[j] * cur

        print('check', mid, r, A[r] - sub)
        return A[r] - sub

    # print(calc(1, 2))
    # print(calc(0, 2))
    
    res = inf

    for r in range(n):
        left, right = 0, r
        while left < right:
            mid = left + right >> 1
            # print(mid, r, calc(mid, r), left, right)
            if calc(mid, r) < x:
                left = mid + 1
            else:
                right = mid
        # print('r, left: ', r, left)
        
        for i in range(left - 1, left + 2):
            if 0 <= i <= r:
                res = fmin(res, abs(calc(i, r) - x))
                print(i, r, calc(i, r))
                
    
    print(res)
    

for testcase in range(1):
    solve(testcase)