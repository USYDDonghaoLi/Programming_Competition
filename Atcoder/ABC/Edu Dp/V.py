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
    n, m = MI()
    adj = defaultdict(list)
    for _ in range(n - 1):
        x, y = MI()
        adj[x].append(y)
        adj[y].append(x)
    
    '''
    m不是质数，不能取逆，所以要计算前缀积后缀积。
    '''
    f = [-1 for _ in range(n + 1)]
    g = [-1 for _ in range(n + 1)]
    premul = defaultdict(list)
    sufmul = defaultdict(list)

    @bootstrap
    def calc1(node, parent):
        ret = 1
        for o in adj[node]:
            if o == parent:
                continue
            else:
                yield calc1(o, node)
                ret *= f[o] + 1
                ret %= m
        f[node] = ret

        k = len(adj[node])
        pre = [1 for _ in range(k + 1)]
        suf = [1 for _ in range(k + 1)]
        for i in range(1, k):
            pre[i] = pre[i - 1]
            if adj[node][i - 1] != parent:
                pre[i] *= f[adj[node][i - 1]] + 1
                pre[i] %= m
        for i in range(k - 2, -1, -1):
            suf[i] = suf[i + 1]
            if adj[node][i + 1] != parent:
                suf[i] *= f[adj[node][i + 1]] + 1
                suf[i] %= m
        premul[node] = pre
        sufmul[node] = suf
        yield None
    
    calc1(1, 0)

    #print('f', f)
    g[1] = 1

    @bootstrap
    def calc2(node, parent):
        k = len(adj[node])
        for i in range(k):
            if adj[node][i] == parent:
                continue
            else:
                g[adj[node][i]] = premul[node][i] * sufmul[node][i] % m * g[node] % m + 1
                yield calc2(adj[node][i], node)
        yield None
    
    calc2(1, 0)
    #print('g', g)

    for i in range(1, n + 1):
        print(f[i] * g[i] % m)

for testcase in range(1):
    solve(testcase)