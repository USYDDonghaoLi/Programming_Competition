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

# @TIME
# def solve(testcase):
#     n = II()
#     nums = LII()
    
#     cnt = [0 for _ in range(n + 1)]
#     for num in nums:
#         cnt[num] += 1
    
#     unique = [num for num in range(n + 1) if cnt[num]]
#     m = len(unique)
#     # print(unique, cnt[4], cnt[unique[-1]])
    
#     '''
#     到第几个数字，剩多少次数
#     '''
#     dp = [[inf for _ in range(m + 2)] for _ in range(m + 1)]
#     dp[0][0] = 0
    
#     for i in range(m):
#         for j in range(m + 1):
#             if dp[i][j] != inf:
#                 if j >= cnt[unique[i]]:
#                     dp[i + 1][j - cnt[unique[i]]] = min(dp[i + 1][j - cnt[unique[i]]], dp[i][j])
#                 dp[i + 1][j + 1] = min(dp[i + 1][j + 1], dp[i][j] + 1)
#                 dp[i + 1][j] = min(dp[i + 1][j], dp[i][j])
    
#     for i in range(1, m + 1):
#         print(unique[i - 1], dp[i])
#     print(min(dp[-1]))

    # res = 0
    # for i in range(m, m + 1):
    #     for j in range(m + 1):
    #         # if dp[i][j] != -inf:
    #         if j < cnt[unique[-1]] + 1:
    #             res = max(res, dp[i][j])
    #             # print('res', res)
    #             # break
    
    # print(res)

def solve(testcase):

    n = II()
    A = LII()
    A.sort()
    cnt = Counter(A)
    dp = {}
    dp[1] = 0
    for a in sorted(set(A))[1:]:
        c = cnt[a]
        ndp = {}
        for j, c1 in sorted(dp.items()):
            if (j - 1) - c1 >= c - 1:
                if j in ndp:
                    ndp[j] = min(ndp[j], c + c1)
                else:
                    ndp[j] = c+c1
            ndp[j + 1] = c1
        dp = ndp
    print(min(dp))

    # n = II()
    # nums = LII()
    
    # cnt = [0 for _ in range(n + 1)]
    # for num in nums:
    #     cnt[num] += 1
    
    # unique = [num for num in range(n + 1) if cnt[num]]
    # m = len(unique)
    
    # dp = [[(None, None) for _ in range(m + 1)] for _ in range(m + 1)]
    
    # def merge(i, j, l, r):
    #     if dp[i][j] == (None, None):
    #         dp[i][j] = (l, r)
    #     else:
    #         left, right = dp[i][j]
    #         dp[i][j] = (min(left, l), max(right, r))
    
    # # '''
    # # 到第几个数字，剩多少次数
    # # '''
    # dp = [[-inf for _ in range(m + 1)] for _ in range(m + 1)]
    # dp[0][0] = (0, 0)
    
    # for i in range(m):
    #     for j in range(m + 1):
    #         if dp[i][j] != (None, None):
    #             l, r = dp[i][j]
    #             merge(i + 1, j + 1, l + 1, r + 1)
    #             merge(i + 1, j, l, r)
    #             dp[i + 1][j + 1] = max(dp[i + 1][j + 1], dp[i][j] + 1)
        
    #     # for j in range(m + 1):
    #         if j >= cnt[unique[i]]:
    #             merge(i + 1, j - cnt[unique[i]], l, r)
                    # dp[i + 1][j - cnt[unique[i]]] = max(dp[i + 1][j - cnt[unique[i]]], dp[i][j])
                # dp[i + 1][j] = max(dp[i + 1][j], dp[i][j])
    
    # for i in range(1, m + 1):
    #     print(unique[i - 1], dp[i])
 
    # res = 0
    # for i in range(m + 1):
    #     for j in range(m + 1):
    #         if dp[i][j] > 0:
    #             res = max(res, dp[i][j])
    #             break
    
    # print(res)
    
    # print(dp[-1])

for testcase in range(II()):
    solve(testcase)