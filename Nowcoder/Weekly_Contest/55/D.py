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
    grid = [LII() for _ in range(n)]
    vis = [[False for _ in range(n)] for _ in range(n)]
    vis[0][0] = True

    left = [[-1 for _ in range(n)] for _ in range(n)]
    right = [[n for _ in range(n)] for _ in range(n)]
    up = [[-1 for _ in range(n)] for _ in range(n)]
    down = [[n for _ in range(n)] for _ in range(n)]

    for i in range(n):
        cur = -1
        for j in range(n):
            left[i][j] = cur
            if grid[i][j]:
                cur = j
    
    for i in range(n):
        cur = n
        for j in range(n - 1, -1, -1):
            right[i][j] = cur
            if grid[i][j]:
                cur = j
    
    for j in range(n):
        cur = -1
        for i in range(n):
            up[i][j] = cur
            if grid[i][j]:
                cur = i
    
    for j in range(n):
        cur = n
        for i in range(n - 1, -1, -1):
            down[i][j] = cur
            if grid[i][j]:
                cur = i

    step = 0
    q = deque()
    q.append((0, 0))

    while q:
        k = len(q)
        # print('q', q)
        for _ in range(k):
            x, y = q.popleft()
            if x == n - 1 and y == n - 1:
                print(step)
                return
            
            '''
            left
            '''
            nx, ny = x, y - 1
            if 0 <= nx < n and 0 <= ny < n:
                if grid[nx][ny]:
                    '''
                    left wall
                    '''
                    ny = right[x][y]
                    ny -= 1
                
                # if not vis[nx][ny]:
                #     vis[nx][ny] = True
                #     q.append((nx, ny))
            else:
                ny = right[x][y]
                ny -= 1
            
            
            if not vis[nx][ny]:
                vis[nx][ny] = True
                q.append((nx, ny))
            
            '''
            right
            '''
            nx, ny = x, y + 1
            if 0 <= nx < n and 0 <= ny < n:
                if grid[nx][ny]:
                    '''
                    right wall
                    '''
                    ny = left[x][y]
                    ny += 1
                
                # if not vis[nx][ny]:
                #     vis[nx][ny] = True
                #     q.append((nx, ny))
            else:
                ny = left[x][y]
                ny += 1

            if not vis[nx][ny]:
                vis[nx][ny] = True
                q.append((nx, ny))

            '''
            up
            '''
            nx, ny = x - 1, y
            if 0 <= nx < n and 0 <= ny < n:
                if grid[nx][ny]:
                    '''
                    up wall
                    '''
                    nx = down[x][y]
                    nx -= 1
                
                # if not vis[nx][ny]:
                #     vis[nx][ny] = True
                #     q.append((nx, ny))
            else:
                nx = down[x][y]
                nx -= 1
            
            if not vis[nx][ny]:
                vis[nx][ny] = True
                q.append((nx, ny))

            '''
            down
            '''
            nx, ny = x + 1, y
            if 0 <= nx < n and 0 <= ny < n:
                if grid[nx][ny]:
                    '''
                    down wall
                    '''
                    nx = up[x][y]
                    nx += 1
                
                # if not vis[nx][ny]:
                #     vis[nx][ny] = True
                #     q.append((nx, ny))
            else:
                nx = up[x][y]
                nx += 1
            
            if not vis[nx][ny]:
                vis[nx][ny] = True
                q.append((nx, ny))

        step += 1
    
    print(-1)

for testcase in range(1):
    solve(testcase)