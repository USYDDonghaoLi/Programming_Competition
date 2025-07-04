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
    a, b, c = MI()
    dist = [[float('inf') for _ in range(101)] for _ in range(101)]
    prev = defaultdict(tuple)
    dist[0][0] = 0
    q = deque()
    q.append((0, 0))

    while q:
        x, y = q.popleft()
        if dist[x][0] > dist[x][y] + 1:
            dist[x][0] = dist[x][y] + 1
            prev[(x, 0)] = (x, y)
            q.append((x, 0))
        if dist[0][y] > dist[x][y] + 1:
            dist[0][y] = dist[x][y] + 1
            prev[(0, y)] = (x, y)
            q.append((0, y))
        if dist[x][b] > dist[x][y] + 1:
            dist[x][b] = dist[x][y] + 1
            prev[(x, b)] = (x, y)
            q.append((x, b))
        if dist[a][y] > dist[x][y] + 1:
            dist[a][y] = dist[x][y] + 1
            prev[(a, y)] = (x, y)
            q.append((a, y))
        t = x + y
        if t <= a:
            if dist[t][0] > dist[x][y] + 1:
                dist[t][0] = dist[x][y] + 1
                prev[(t, 0)] = (x, y)
                q.append((t, 0))
        else:
            if dist[a][t - a] > dist[x][y] + 1:
                dist[a][t - a] = dist[x][y] + 1
                prev[(a, t - a)] = (x, y)
                q.append((a, t - a))

        if t <= b:
            if dist[0][t] > dist[x][y] + 1:
                dist[0][t] = dist[x][y] + 1
                prev[(0, t)] = (x, y)
                q.append((0, t))
        else:
            if dist[t - b][b] > dist[x][y] + 1:
                dist[t - b][b] = dist[x][y] + 1
                prev[(t - b, b)] = (x, y)
                q.append((t - b, b))
    
    finalx, finaly = -1, -1
    res = float('inf')
    for i in range(101):
        if dist[i][c] < res:
            res = dist[i][c]
            finalx, finaly = i, c
    for j in range(101):
        if dist[c][j] < res:
            res = dist[c][j]
            finalx, finaly = c, j
    
    print(res)
    ops = []
    x, y = finalx, finaly
    while x != 0 or y != 0:
        # print('xy', x, y, prev[(x, y)])
        px, py = prev[(x, y)]

        if px + py == x + y:
            if px >= x:
                ops.append('POUR(1,2)')
            else:
                ops.append('POUR(2,1)')
        else:
            if px < a and x == a:
                ops.append('FILL(1)')
            elif py < b and y == b:
                ops.append('FILL(2)')
            elif px != 0 and x == 0:
                ops.append('DROP(1)')
            elif py != 0 and y == 0:
                ops.append('DROP(2)')
    
        x, y = px, py

    for o in ops[::-1]:
        print(o)



for testcase in range(1):
    solve(testcase)