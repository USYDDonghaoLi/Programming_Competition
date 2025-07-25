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
    n, m, k = MI()
    grid = [['' for _ in range(m + 1)] for _ in range(n + 1)]
    mp = defaultdict(list)
    belong = defaultdict(str)
    square = defaultdict(list)

    for _ in range(k):
        s, x, y = LI()
        x, y = int(x), int(y)
        if grid[x][y] == '':
            grid[x][y] = s
            mp[s] = [x, y]
            belong[(x, y)] = s
            square[s].append([x, y])
        else:
            if s > grid[x][y]:
                del mp[grid[x][y]]
                del square[grid[x][y]]
                grid[x][y] = s
                mp[s] = [x, y]
                belong[(x, y)] = s
                square[s].append([x, y])
                
            else:
                continue
    
    d = {'W': (-1, 0), 'S': (1, 0), 'A': (0, -1), 'D': (0, 1)}

    q = II()
    for _ in range(q):
        army, pos = LI()
        if army not in mp:
            print('unexisted empire.')
            continue
        dx, dy = d[pos]
        x, y = mp[army]
        nx, ny = x + dx, y + dy
        if not 1 <= nx <= n or not 1 <= ny <= m:
            print('out of bounds!')
            continue
        if belong[(nx, ny)] == army:
            print('peaceful.')
            mp[army] = [nx, ny]
            continue
        if not belong[(nx, ny)]:
            belong[(nx, ny)] = army
            square[army].append([nx, ny])
            mp[army] = [nx, ny]
            print('vanquish!')
            continue
        enemy = belong[(nx, ny)]
        if len(square[enemy]) < len(square[army]) or (len(square[enemy]) == len(square[army]) and army > enemy):
            print(f'{army} wins!')
            for a, b in square[enemy]:
                belong[(a, b)] = army
                square[army].append([a, b])
            del square[enemy]
            del mp[enemy]
            mp[army] = [nx, ny]
        else:
            print(f'{enemy} wins!')
            for a, b in square[army]:
                belong[(a, b)] = enemy
                square[enemy].append([a, b])
            del square[army]
            del mp[army]

for testcase in range(1):
    solve(testcase)