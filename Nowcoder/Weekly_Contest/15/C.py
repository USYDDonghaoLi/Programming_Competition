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

# @TIME
def solve(testcase):
    s = I()
    n = len(s)
    if n < 3:
        res = []
        S = ['0', '1', '2']
        for i in range(n):
            if res and s[i] == res[-1]:
                print(-1)
                return
            if s[i] in S:
                res.append(s[i])
                S.remove(s[i])
            else:
                res.append(S[0])
                S.pop(0)
            # print('res', res, S, 'S')
        print(''.join(res))
        return

    @lru_cache(None)
    def encode(a, b, c):
        return a * 9 + b * 3 + c

    @lru_cache(None)
    def decode(state):
        c = state % 3
        state //= 3
        b = state % 3
        state //= 3
        a = state
        return a, b, c

    '''
    每个state代表这三位在的三进制数字
    '''
    dp = [[0 for _ in range(27)] for _ in range(n)]
    prev = defaultdict(lambda : defaultdict(int))

    '''
    处理前两位
    '''
    if s[0] == '?':
        dp[0][0] = dp[0][1] = dp[0][2] = 1
    else:
        dp[0][int(s[0])] = 1
    
    if s[1] == '?':
        for j in range(3):
            if dp[0][j]:
                for t in range(3):
                    if j == t:
                        continue
                    new = j * 3 + t
                    dp[1][new] = 1
    else:
        for j in range(3):
            if dp[0][j]:
                if int(s[1]) == j:
                    continue
                dp[1][j * 3 + int(s[1])] = 1

    for i in range(2, n):
        if s[i] == '?':
            for t in range(3):
                for j in range(27):
                    if dp[i - 1][j]:
                        a, b, c = decode(j)
                        if c == t:
                            continue
                        newstate = encode(b, c, t)
                        if not newstate & 1:
                            dp[i][newstate] = 1
                            prev[i][newstate] = j
        else:
            t = int(s[i])
            for j in range(27):
                if dp[i - 1][j]:
                    a, b, c = decode(j)
                    if c == t:
                        continue
                    newstate = encode(b, c, t)
                    if not newstate & 1:
                        dp[i][newstate] = 1
                        prev[i][newstate] = j
    
    # print('dp', dp)
    # print('prev', prev)

    start = -1
    for j in range(27):
        if dp[-1][j]:
            start = j
            break
    else:
        print(-1)
        return
    
    
    a, b, c = decode(start)
    res = [c, b, a]
    curidx = n - 1
    curstate = start

    while curidx > 2:
        prevstate = prev[curidx][curstate]
        a, b, c = decode(prevstate)
        res.append(a)
        curstate = prevstate
        curidx -= 1

    res.reverse()
    print(''.join(list(map(str, res))))

    for i in range(1, n):
        assert res[i] != res[i - 1]    

    for i in range(2, n):
        assert encode(res[i - 2], res[i - 1], res[i]) & 1 == 0

for testcase in range(1):
    solve(testcase)