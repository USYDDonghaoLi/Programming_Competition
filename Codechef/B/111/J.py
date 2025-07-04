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

# RANDOM = getrandbits(32)
 
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

maxA = 10 ** 7 + 10
mod = 998244353

spf = [0 for _ in range(maxA)]
sqfree = [0 for _ in range(maxA)]

for i in range(2, maxA):
    if spf[i]:
        continue
    else:
        for j in range(i, maxA, i):
            if not spf[j]:
                spf[j] = i
    
sqfree[1] = 1
for i in range(2, maxA):
    p = spf[i]
    if spf[i // p] == p:
        sqfree[i] = sqfree[(i // p) // p]
    else:
        sqfree[i] = p * sqfree[i // p]

lensum = [0 for _ in range(maxA)]
# @TIME
def solve(testcase):
    n = II()
    nums = LII()

    end_gcd = [defaultdict(int) for _ in range(n)]
    start_gcd = [defaultdict(int) for _ in range(n)]

    res = 0
    for i in range(n):
        end_gcd[i][nums[i]] = 0
        if i:
            for x in end_gcd[i - 1]:
                g = gcd(x, nums[i])
                end_gcd[i][g] = max(end_gcd[i][g], end_gcd[i - 1][x] + 1)
        print(end_gcd[i])
    
    for i in range(n - 1, -1, -1):
        tmp = list(end_gcd[i].keys())
        m = len(tmp)
        idx = 0
        while idx < m:
            x = tmp[idx]
            y = end_gcd[i][x]
            pos = sqfree[x]

            LEN = 0
            if idx != m - 1:
                x2 = tmp[idx + 1]
                y2 = end_gcd[idx][x2]
                LEN = y - y2
            else:
                LEN = y + 1
            
            res = LEN * lensum[pos] % mod
            res %= mod
            idx += 1
        
        start_gcd[i][nums[i]] = 0
        if i + 1 < n:
            for x in start_gcd[i + 1]:
                y = start_gcd[i + 1][x]
                g = gcd(x, nums[i])
                start_gcd[i][g] = max(start_gcd[i][g], y + 1)
        
        tmp = list(start_gcd[i].keys())
        m = len(tmp)
        idx = 0
        while idx < m:
            x = tmp[idx]
            y = start_gcd[i][x]
            pos = sqfree[x]

            if idx + 1 != m:
                x2 = tmp[idx + 1]
                y2 = start_gcd[i][x2]
                lensum[pos] += y - y2
            else:
                lensum[pos] += y + 1

            idx += 1

    for i in range(n):
        for x in start_gcd[i]:
            lensum[sqfree[x]] = 0
    
    print(res)

for testcase in range(II()):
    solve(testcase)