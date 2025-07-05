'''
Hala Madrid!
https://www.zhihu.com/people/li-dong-hao-78-74
'''

import sys
import os
# from io import BytesIO, IOBase
# BUFSIZE = 8192
# class FastIO(IOBase):
#     newlines = 0
#     def __init__(self, file):
#         self._fd = file.fileno()
#         self.buffer = BytesIO()
#         self.writable = "x" in file.mode or "r" not in file.mode
#         self.write = self.buffer.write if self.writable else None
#     def read(self):
#         while True:
#             b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
#             if not b:
#                 break
#             ptr = self.buffer.tell()
#             self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
#         self.newlines = 0
#         return self.buffer.read()
#     def readline(self):
#         while self.newlines == 0:
#             b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
#             self.newlines = b.count(b"\n") + (not b)
#             ptr = self.buffer.tell()
#             self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
#         self.newlines -= 1
#         return self.buffer.readline()
#     def flush(self):
#         if self.writable:
#             os.write(self._fd, self.buffer.getvalue())
#             self.buffer.truncate(0), self.buffer.seek(0)
# class IOWrapper(IOBase):
#     def __init__(self, file):
#         self.buffer = FastIO(file)
#         self.flush = self.buffer.flush
#         self.writable = self.buffer.writable
#         self.write = lambda s: self.buffer.write(s.encode("ascii"))
#         self.read = lambda: self.buffer.read().decode("ascii")
#         self.readline = lambda: self.buffer.readline().decode("ascii")
# sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
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

# ans = 0
# for i in range(114514, 1919180 + 1):
#     if '4931' in str(i):
#         # print('i', i)
#         ans += i

# print(ans)

# @TIME
def solve(testcase):
    a, b = MI()
    target = [4, 9, 3, 1]

    def calc(num):
        if num < 4931:
            return 0
        s = [int(c) for c in str(num)]
        n = len(s)

        dp = [[[[defaultdict(lambda : -1) for _ in range(2)] for _ in range(2)] for _ in range(5)] for _ in range(12)]

        # @lru_cache(None)
        def dfs(idx, tidx, isStart, isLim, cur):

            # print(idx, tidx, isStart, isLim, cur)
            # print(dp[idx][tidx][isStart][isLim][cur])
            
            if dp[idx][tidx][isStart][isLim][cur] != -1:
                return dp[idx][tidx][isStart][isLim][cur]

            if idx == n:
                if tidx == 4:
                    # print('ok', cur)
                    dp[idx][tidx][isStart][isLim][cur] = cur
                else:
                    dp[idx][tidx][isStart][isLim][cur] = 0
                return dp[idx][tidx][isStart][isLim][cur]
            
            if tidx == 4:
                if isLim:
                    t = 0
                    for i in range(idx, n):
                        t = t * 10 + s[i]
                    t += 1
                    # print('ok', idx, tidx, isStart, isLim, cur, t, cur * 10 ** (n - idx) * t + t * (t - 1) // 2)
                    dp[idx][tidx][isStart][isLim][cur] = cur * 10 ** (n - idx) * t + t * (t - 1) // 2
                else:
                    t = 10 ** (n - idx)
                    # print('ok', cur, t, cur * t * t + t * (t - 1) // 2)
                    dp[idx][tidx][isStart][isLim][cur] = cur * t * t + t * (t - 1) // 2
                return dp[idx][tidx][isStart][isLim][cur]
            
            if n - idx < 4 - tidx:
                dp[idx][tidx][isStart][isLim][cur] = 0
                return dp[idx][tidx][isStart][isLim][cur]
            
            res = 0

            if isStart:
                if isLim:
                    for i in range(s[idx]):
                        if i == target[tidx]:
                            res += dfs(idx + 1, tidx + 1, True, False, cur * 10 + i)
                        else:
                            res += dfs(idx + 1, int(i == target[0]), True, False, cur * 10 + i)
                    
                    if s[idx] == target[tidx]:
                        # print('check', idx + 1, tidx + 1, isStart, isLim, cur * 10 + s[idx], dfs(idx + 1, tidx + 1, True, True, cur * 10 + s[idx]))
                        res += dfs(idx + 1, tidx + 1, True, True, cur * 10 + s[idx])
                    else:
                        res += dfs(idx + 1, int(s[idx] == target[0]), True, True, cur * 10 + s[idx])
                else:
                    for i in range(10):
                        if i == target[tidx]:
                            res += dfs(idx + 1, tidx + 1, True, False, cur * 10 + i)
                        else:
                            res += dfs(idx + 1, int(i == target[0]), True, False, cur * 10 + i)
            else:
                if idx == 0:
                    for i in range(1, s[0]):
                        if i == target[tidx]:
                            res += dfs(idx + 1, tidx + 1, True, False, cur * 10 + i)
                        else:
                            res += dfs(idx + 1, int(i == target[0]), True, False, cur * 10 + i)
                    
                    if s[0] == target[tidx]:
                        res += dfs(idx + 1, tidx + 1, True, True, cur * 10 + s[0])
                    else:
                        res += dfs(idx + 1, int(s[idx] == target[0]), True, True, cur * 10 + s[0])
                else:
                    for i in range(1, 10):
                        if i == target[tidx]:
                            res += dfs(idx + 1, tidx + 1, True, False, cur * 10 + i)
                        else:
                            res += dfs(idx + 1, int(i == target[0]), True, False, cur * 10 + i)
                
                res += dfs(idx + 1, 0, False, False, 0)
            
            # print(f"idx = {idx}, tidx = {tidx}, isStart = {isStart}, isLim = {isLim}, cur = {cur}, res = {res}")
            dp[idx][tidx][isStart][isLim][cur] = res
            return res
        
        ans = dfs(0, 0, False, False, 0)
        # dfs.cache_clear()
        return ans

    res = calc(b) - calc(a - 1)
    print(res)
    # print('diff', ans - res)
    
for testcase in range(1):
    solve(testcase)