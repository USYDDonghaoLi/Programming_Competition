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
    
def solve(testcase):
    n = II()
    A = LII()
    p = [-1 for _ in range(n)]
    q = [-1 for _ in range(n)]

    visp = [False for _ in range(n + 1)]
    visq = [False for _ in range(n + 1)]
    idxs = [i for i in range(n)]
    idxs.sort(key = lambda x: -A[x])

    limit = []

    for i in idxs:
        M = A[i]
        if visp[M]:
            if visq[M]:
                print('NO')
                return
            else:
                q[i] = M
                visq[M] = True
                heappush(limit, (M, i, 'p'))
        else:
            p[i] = M
            visp[M] = True
            heappush(limit, (M, i, 'q'))

    nowp = 1
    nowq = 1

    while limit:
        while nowp <= n and visp[nowp]:
            nowp += 1
        while nowq <= n and visq[nowq]:
            nowq += 1

        lim, idx, where = heappop(limit)
        if where == 'p':
            if nowp <= lim:
                p[idx] = nowp
                visp[nowp] = True
            else:
                print('NO')
                return
        else:
            if nowq <= lim:
                q[idx] = nowq
                visq[nowq] = True
            else:
                print('NO')
                return
    
    print('YES')
    print(*p)
    print(*q)


for testcase in range(II()):
    solve(testcase)