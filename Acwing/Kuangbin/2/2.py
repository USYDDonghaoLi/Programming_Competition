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
dx = [1, 0, 0, -1]
dy = [0, -1, 1, 0]
d = 'dlru'
path = ['' for _ in range(100)]


# @TIME
def solve(testcase):
    s = list(I())
    ed = list(I())
    edx, edy = [0 for _ in range(9)], [0 for _ in range(9)]
    x, y = -1, -1
    for i in range(9):
        if ed[i] != 'X':
            edx[int(ed[i]) - 1], edy[int(ed[i]) - 1] = divmod(i, 3)
        if s[i] == 'X':
            x, y = divmod(i, 3)
    
    ida = 0
    for i in range(9):
        if s[i] != 'X':
            ida += abs(i // 3 - edx[int(s[i]) - 1]) + abs(i % 3 - edy[int(s[i]) - 1])
    
    def dfs(u, ida):
        nonlocal x, y
        if u + ida > dep:
            return 0
        if s == ed:
            print(f"Case {testcase + 1}: {u}")
            print(''.join([d[p] for p in path[:u]]))
            return 1
        
        tmpx, tmpy = x, y
        for i in range(4):
            if u and path[u - 1] + i == 3:
                continue
            nx, ny = tmpx + dx[i], tmpy + dy[i]
            if 0 <= nx < 3 and 0 <= ny < 3:
                a = int(s[nx * 3 + ny]) - 1
                ret = abs(tmpx - edx[a]) + abs(nx - edx[a]) + abs(tmpy - edy[a]) + abs(ny - edy[a])
                x, y = nx, ny
                path[u] = i

                s[nx * 3 + ny], s[tmpx * 3 + tmpy] = s[tmpx * 3 + tmpy], s[nx * 3 + ny]
                if dfs(u + 1, ida + ret):
                    return 1
                s[nx * 3 + ny], s[tmpx * 3 + tmpy] = s[tmpx * 3 + tmpy], s[nx * 3 + ny]
        x, y = tmpx, tmpy
        return 0
    
    for dep in range(10 ** 9):
        if dfs(0, ida):
            break

for testcase in range(II()):
    solve(testcase)