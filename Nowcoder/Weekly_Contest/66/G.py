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

def solve(testcase):
    x, k = MI()
    L, R = x, x + k

    lowers = list(map(int, str(L - 1)))
    uppers = list(map(int, str(R)))

    if len(lowers) < len(uppers):
        lowers = [0] * (len(uppers) - len(lowers)) + lowers

    def calc(num, mex):
        if not num:
            return 0
        tar = (1 << mex) - 1
        n = len(num)

        @lru_cache(None)
        def dfs(pos, limit, started, mask):
            if pos == n:
                if not started:
                    mask = 1 << 0
                has_all = (mask & tar) == tar
                no_mex  = (mask >> mex & 1) == 0
                return 1 if has_all and no_mex else 0

            res = 0
            up = num[pos] if limit else 9
            for d in range(up + 1):
                if d == mex:
                    continue
                nlimit = limit and (d == up)
                if started:
                    res += dfs(pos + 1, nlimit, True, mask | (1 << d))
                else:
                    if d == 0:           
                        res += dfs(pos + 1, nlimit, False, mask)
                    else:                
                        res += dfs(pos + 1, nlimit, True, 1 << d)
            return res

        ans = dfs(0, True, False, 0)
        dfs.cache_clear()
        return ans

    for m in range(10, 0, -1):
        cnt = calc(uppers, m) - calc(lowers, m)
        if cnt > 0:
            print(m, cnt)
            return

    print(0, R - L + 1)

for testcase in range(II()):
    solve(testcase)