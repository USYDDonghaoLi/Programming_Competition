"""
Fast IO（快速输入输出）

用于竞争编程的高性能 I/O 模板。

特点：
- 使用缓冲减少系统调用
- 快速读写整数和字符串
- 适合输入输出量大的题目

使用：
- input() / readline() 读取
- 自定义输出函数
"""

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

# @TIME
def solve(testcase):
    n, x, y = MI()
    A = LII()

    if n == 1:
        res = inf
        for s in range(51):
            tmp = fmax(0, A[0] - 2 * s)
            res = fmin(res, y * s + x * tmp)
        print(res)
        return

    dp = [[inf for _ in range(51)] for _ in range(51)]
    for i in range(51):
        for j in range(51):
            tmp = fmax(0, A[0] - 2 * i - j)
            dp[i][j] = y * (i + j) + x * tmp

    for i in range(2, n):
        ndp = [[inf] * 51 for _ in range(51)]

        for cur in range(51):
            d = [dp[prev][cur] for prev in range(51)]

            SU = [inf for _ in range(52)]
            for j in range(50, -1, -1):
                SU[j] = fmin(d[j], SU[j + 1])

            s = SU[0]

            PS = [inf for _ in range(52)]
            for j in range(51):
                val = d[j] - x * j
                PS[j + 1] = fmin(PS[j], val)

            for nxt in range(51):
                tmp = A[i - 1] - 2 * cur - nxt

                if tmp <= 0:
                    vval = s
                else:
                    if tmp <= 50:
                        vval1 = SU[tmp]
                    else:
                        vval1 = inf

                    vval2 = x * tmp + PS[fmin(tmp, 51)]

                    vval = fmin(vval1, vval2)

                if vval == inf:
                    continue

                cost = vval + y * nxt
                if cost < ndp[cur][nxt]:
                    ndp[cur][nxt] = cost

        dp = ndp

    res = inf
    for prev in range(51):
        for cur in range(51):
            if dp[prev][cur] == inf:
                continue

            tmp = fmax(0, A[n - 1] - prev - 2 * cur)
            cost = dp[prev][cur] + x * tmp
            if cost < res:
                res = cost

    print(res)



for testcase in range(1):
    solve(testcase)