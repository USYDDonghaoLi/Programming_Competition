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

d = ((0, 1), (0, -1), (1, 0), (-1, 0))

# @TIME
def solve(testcase):
    n = II()
    grid = [I() for _ in range(2)]
    
    diff = [[inf for _ in range(n)] for _ in range(2)]
    
    def check(i, j):
        
        # print('ij', i, j)
        grid2 = [[] for _ in range(2)]
        for ii in range(2):
            for jj in range(j - 2, j + 3):
                if 0 <= jj < n:
                    grid2[ii].append(grid[ii][jj])
        
        mm = len(grid2[0])
        v = [[False for _ in range(mm)] for _ in range(2)]
        cnt1 = 0
        
        for ii in range(2):
            for jj in range(mm):
                if grid2[ii][jj] == 'x':
                    v[ii][jj] = True
                    continue
                
                if v[ii][jj]:
                    continue
                
                q = deque()
                q.append((ii, jj))
                v[ii][jj] = True
                
                while q:
                    x, y = q.popleft()
                    for dx, dy in d:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 2 and 0 <= ny < mm and not v[nx][ny] and grid2[nx][ny] == '.':
                            v[nx][ny] = True
                            q.append((nx, ny))
                cnt1 += 1
        
        # print(grid2, cnt1, '111')
        
        grid2 = [[] for _ in range(2)]
        for ii in range(2):
            for jj in range(j - 2, j + 3):
                if 0 <= jj < n:
                    grid2[ii].append(grid[ii][jj])
                    # print('change', i, ii, j, jj)
                    if i == ii and j == jj:
                        grid2[ii][-1] = 'x'
        
        mm = len(grid2[0])
        v = [[False for _ in range(mm)] for _ in range(2)]
        cnt2 = 0
        
        for ii in range(2):
            for jj in range(mm):
                if grid2[ii][jj] == 'x':
                    v[ii][jj] = True
                    continue
                
                if v[ii][jj]:
                    continue
                
                q = deque()
                q.append((ii, jj))
                v[ii][jj] = True
                
                while q:
                    x, y = q.popleft()
                    for dx, dy in d:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 2 and 0 <= ny < mm and not v[nx][ny] and grid2[nx][ny] == '.':
                            v[nx][ny] = True
                            q.append((nx, ny))
                cnt2 += 1
        
        # print(grid2, cnt2, '222')
        
        return cnt2 - cnt1
    
    vis = [[False for _ in range(n)] for _ in range(2)]
    tot = 0
    
    for i in range(2):
        for j in range(n):
            if grid[i][j] == 'x':
                vis[i][j] = True
                continue
            
            if vis[i][j]:
                continue
            
            q = deque()
            q.append((i, j))
            vis[i][j] = True
            
            while q:
                x, y = q.popleft()
                for dx, dy in d:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 2 and 0 <= ny < n and not vis[nx][ny] and grid[nx][ny] == '.':
                        vis[nx][ny] = True
                        q.append((nx, ny))
            
            tot += 1
    
    # print(tot, 'tot')
    
    res = 0
    
    for i in range(2):
        for j in range(n):
            if grid[i][j] == 'x':
                continue
            if tot + check(i, j) == 3:
                res += 1

    print(res)
    

for testcase in range(II()):
    solve(testcase)