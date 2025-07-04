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

class Node:

    __slots__ = {'mxpre', 'mxsuf', 'mx', 'mnpre', 'mnsuf', 'mn', 'sum'}

    def __init__(self) -> None:
        self.mxpre = 0
        self.mxsuf = 0
        self.mx = 0
        self.mnpre = 0
        self.mnsuf = 0
        self.mn = 0
        self.sum = 0
    
    # @staticmethod
    def __add__(self: 'Node', b: 'Node') -> 'Node':
        c = Node()
        c.mxpre = max(self.mxpre, self.sum + b.mxpre)
        c.mnpre = min(self.mnpre, self.sum + b.mnpre)
        c.mxsuf = max(b.mxsuf, b.sum + self.mxsuf)
        c.mnsuf = min(b.mnsuf, b.sum + self.mnsuf)
        c.mx = max(self.mx, b.mx, self.mxsuf + b.mxpre)
        c.mn = min(self.mn, b.mn, self.mnsuf + b.mnpre)
        c.sum = self.sum + b.sum
        return c
    
    def rev(self: 'Node'):
        self.mxpre, self.mxsuf = self.mxsuf, self.mxpre
        self.mnpre, self.mnsuf = self.mnsuf, self.mnpre


def solve(testcase):
    n = II()

    pw = [1 for _ in range(20)]
    for i in range(1, 20):
        pw[i] = pw[i - 1] * 2
    p = [-1 for _ in range(n + 10)]
    x = [1 for _ in range(n + 10)]
    idx = 2
    qry = []

    for _ in range(n):
        op, *lst = LI()
        if op == '+':
            v, xi = map(int, lst)
            p[idx] = v
            x[idx] = xi
            idx += 1
        else:
            u, v, k = map(int, lst)
            qry.append((u, v, k))
    
    n = len(p)
    logn = int(log(n, 2)) + 1
    pp = [[-1 for _ in range(n)] for _ in range(logn + 1)]
    f = [[Node() for _ in range(n)] for _ in range(logn + 1)]

    dep = [0 for _ in range(n + 1)]

    for i in range(1, n):
        if i > 1:
            dep[i] = dep[p[i]] + 1
        pp[0][i] = p[i]
        if x[i] == 1:
            f[0][i].mx = f[0][i].mxpre = f[0][i].mxsuf = f[0][i].sum = 1
        else:
            f[0][i].mn = f[0][i].mnpre = f[0][i].mnsuf = f[0][i].sum = -1
        
        j = 0
        while pw[j + 1] <= dep[i] + 1:
            pp[j + 1][i] = pp[j][pp[j][i]]
            f[j + 1][i] = f[j][i] + f[j][pp[j][i]]
            j += 1

    def query(x, y):
        if dep[x] < dep[y]:
            x, y = y, x
        l = Node()
        r = Node()
        for i in range(logn, -1, -1):
            if (dep[x] - pw[i] >= dep[y]):
                l = l + f[i][x]
                x = pp[i][x]
        if x == y:
            return l + f[0][x]
        for i in range(logn, -1, -1):
            if pp[i][x] != pp[i][y]:
                l = l + f[i][x]
                r = r + f[i][y]
                x = pp[i][x]
                y = pp[i][y]
        r.rev()
        return l + f[1][x] + f[0][y] + r

    for u, v, k in qry:
        info = query(u, v)
        if info.mn <= k and k <= info.mx:
            print('YES')
        else:
            print('NO')

for testcase in range(II()):
    solve(testcase)