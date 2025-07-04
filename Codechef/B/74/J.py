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

mod = 10 ** 9 + 7

from collections import defaultdict

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

from collections import defaultdict

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

class Tarjan:

    def __init__(self, n: int) -> None:
        self.adj = defaultdict(list)
        self.n = n
        self.dfn = [0 for _ in range(self.n + 1)]
        self.low = [0 for _ in range(self.n + 1)]
        self.dfncnt = 0
        self.s = [0 for _ in range(self.n + 1)]
        self.in_stack = [0 for _ in range(self.n + 1)]
        self.tp = 0
        self.scc = [0 for _ in range(self.n + 1)]
        self.sc = 0
        self.sz = [0 for _ in range(self.n + 1)]
        self.SCC = []
    
    def add(self, u: int, v: int):
        self.adj[u].append(v)
    
    @bootstrap
    def process(self, node: int):
        self.dfncnt += 1
        self.tp += 1

        self.low[node] = self.dfn[node] = self.dfncnt
        self.s[self.tp] = node
        self.in_stack[node] = 1

        for o in self.adj[node]:
            if not self.dfn[o]:
                yield self.process(o)
                self.low[node] = min(self.low[node], self.low[o])
            elif self.in_stack[o]:
                self.low[node] = min(self.low[node], self.dfn[o])

        if self.dfn[node] == self.low[node]:
            points = set()
            self.sc += 1
            while self.s[self.tp] != node:
                self.scc[self.s[self.tp]] = self.sc
                points.add(self.s[self.tp])
                self.sz[self.sc] += 1
                self.in_stack[self.s[self.tp]] = 0
                self.tp -= 1
            self.scc[self.s[self.tp]] = self.sc
            points.add(self.s[self.tp])
            self.sz[self.sc] += 1
            self.in_stack[self.s[self.tp]] = 0
            self.tp -= 1
            self.SCC.append(points)
        yield None
    
    def go(self):
        for i in range(1, self.n + 1):
            if not self.dfn[i]:
                self.process(i)

mod = 10 ** 9 + 7

def solve(testcase):
    n, m = MI()
    TARJAN = Tarjan(m)
    
    for _ in range(n):
        u, v = MI()
        TARJAN.add(u, v)
    
    TARJAN.go()
    # print(TARJAN.sz)
    # print(TARJAN.scc)
    # print(TARJAN.SCC)

    res = 1

    for scc in TARJAN.SCC:
        sink = 1
        for node in scc:
            for o in TARJAN.adj[node]:
                if o not in scc:
                    sink = 0
                    break
        
        res *= pow(2, len(scc), mod) - sink
        res %= mod
    
    print(res)

for testcase in range(II()):
    solve(testcase)