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

'''
手写栈防止recursion limit
注意要用yield 不要用return
函数结尾要写yield None
'''
from types import GeneratorType
def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc

def ask():
    pass

def answer():
    pass

def solve(testcase):
    n, m = LII()
    grid = [[2 for _ in range(m)]]
    for _ in range(n):
        grid.append(LII())
    grid.append([2 for _ in range(m)])
    #print(grid)

    grid2 = [[1 - grid[i][j] for j in range(m)] for i in range(n + 2)]
    #print(grid2)
    
    dp = [[float('inf') for _ in range(8)] for _ in range(n + 2)]
    for j in range(8):
        dp[0][j] = 0

    def check(row, state):
        pstat, nowstat, nxtstat = state >> 2 & 1, state >> 1 & 1, state & 1
        if pstat:
            prev = grid2[row - 1][:]
        else:
            prev = grid[row - 1][:]
        
        if nowstat:
            now = grid2[row][:]
        else:
            now = grid[row][:]
        
        if nxtstat:
            nxt = grid2[row + 1][:]
        else:
            nxt = grid[row + 1][:]
        
        for y in range(m):
            flag = False
            try:
                if now[y] == now[y + 1]:
                    flag = True
            except:
                pass

            try:
                assert y > 0
                if now[y] == now[y - 1]:
                    flag = True
            except:
                pass
                
            if now[y] == prev[y]:
                flag = True
            if now[y] == nxt[y]:
                flag = True

            if not flag:
                return False
        
        return True

    for i in range(1, n + 1):
        for j in range(8):
            #print('solve_check', i, j, check(i, j))
            if check(i, j):
                pstat, nowstat, nxtstat = j >> 2 & 1, j >> 1 & 1, j & 1
                dp[i][j] = min(dp[i][j], dp[i - 1][j >> 1] + nowstat)
                dp[i][j] = min(dp[i][j], dp[i - 1][(j >> 1) | 4] + nowstat)

    #print('dp', dp)

    res = float('inf')
    for j in range(8):
        res = min(res, dp[n][j])
    
    if res == float('inf'):
        print(-1)
    else:
        print(res)

for testcase in range(1):
    solve(testcase)