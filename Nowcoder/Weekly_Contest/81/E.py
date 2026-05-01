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
    n, k = MI()
    res = [i for i in range(n + 1)]
    for i in range(1, n + 1):
        k -= i * i
    
    # print('k', k)
    
    A = [0]
    for i in range(n, 0, -1):
        A.append(A[-1] + i)
    
    # print('A', A)
    
    if k < 0:
        print(-1)
        return
    
    if k == 0:
        print(*res[1:])
        return
    
    vis = [False for _ in range(k + 1)]
    prev = [-1 for _ in range(k + 1)]

    q = deque()
    q.append(k)

    while q:
        cur = q.popleft()
        for i in range(1, n + 1):
            d = A[i]
            if cur >= d:
                val = cur - d
                if not vis[val]:
                    vis[val] = True
                    prev[val] = cur
                    q.append(val)
    
    if vis[0]:
        cur = 0
        DIFF = [0 for _ in range(n + 2)]
        while cur != k:
            pcur = prev[cur]
            diff = pcur - cur
            for i in range(1, n + 1):
                if diff == A[i]:
                    DIFF[n + 1 - i] += 1
                    DIFF[n + 1] -= 1
                    cur = pcur
                    break
            else:
                assert False
            
        for i in range(2, n + 2):
            DIFF[i] += DIFF[i - 1]
        for i in range(1, n + 1):
            res[i] += DIFF[i]
        
        print(*res[1:])
    else:
        print(-1)

    
    # vis = [[False for _ in range(k + 1)] for _ in range(n + 1)]
    # prev = [[(-1, -1) for _ in range(k + 1)] for _ in range(n + 1)]
    # q = deque()
    # q.append((k, 0))
    # vis[0][k] = True

    # while q:
    #     cur, where = q.popleft()
    #     for i in range(1, n + 1):
    #         d = A[i]
    #         val = cur
    #         if val >= d:
    #             val -= d
    #             if vis[i][val]:
    #                 continue
    #             vis[i][val] = True
    #             q.append((val, i))
    #             prev[i][val] = (cur, where)
    #         else:
    #             break
    
    # DIFF = [0 for _ in range(n + 10)]
    
    # for i in range(1, n + 1):
    #     if vis[i][0]:
    #         where, val = i, 0
    #         while where != 0 and val != k:

    #             pval, pwhere = prev[where][val]

    #             DIFF[n + 1 - where] += 1
    #             DIFF[n + 1] -= 1

    #             where, val = pwhere, pval

    #         for i in range(1, n + 10):
    #             DIFF[i] += DIFF[i - 1]
    #         for i in range(1, n + 1):
    #             res[i] += DIFF[i]
            
    #         print(*res[1:])
    #         return
    
    # print(-1)

                


for testcase in range(1):
    solve(testcase)