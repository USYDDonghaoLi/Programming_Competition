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

'''
max(***), mp可能为空 -> error
'''

def solve():
    H, W, N, h, w = MI()
    cnt = [0 for _ in range(N + 1)]
    grid = [[0 for _ in range(W)] for _ in range(H)]
    for i in range(H):
        line = LII()
        for j in range(W):
            grid[i][j] = line[j]
            cnt[line[j]] += 1
    
    res = [[-1 for _ in range(W - w + 1)] for _ in range(H - h + 1)]
    now = 0
    for i in range(N + 1):
        if cnt[i]:
            now += 1
    #print(cnt, now)

    for i in range(H - h + 1):
        cntt = cnt[:]
        noww = now
        for ii in range(i, i + h):
            for jj in range(0, 0 + w):
                cntt[grid[ii][jj]] -= 1
                if cntt[grid[ii][jj]] == 0:
                    noww -= 1
        res[i][0] = noww
        #print('cntt', i, 0, cntt)
        for j in range(1, W - w + 1):
            for ii in range(i, i + h):
                cntt[grid[ii][j - 1]] += 1
                if cntt[grid[ii][j - 1]] == 1:
                    noww += 1
                cntt[grid[ii][j + w - 1]] -= 1
                if cntt[grid[ii][j + w - 1]] == 0:
                    noww -= 1
            res[i][j] = noww
            #print('cntt', i, j, cntt)
    
    for i in range(H - h + 1):
        print(*res[i])


for _ in range(1):solve()