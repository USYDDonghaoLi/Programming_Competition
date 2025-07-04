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
    n = II()
    adj = defaultdict(list)

    for _ in range(n - 1):
        a, b, c = LI()
        a, b = int(a), int(b)
        adj[a].append((b, c))
        adj[b].append((a, c))
    
    child = defaultdict(list)
    q = deque([(1, 0)])
    while q:
        cur, fa = q.popleft()
        for o, c in adj[cur]:
            if o == fa:
                continue
            else:
                child[cur].append((o, c))
                q.append((o, cur))
    
    # print('child', child)

    s = I()
    m = len(s)

    up = [[0 for _ in range(m)] for _ in range(n + 1)]

    @bootstrap
    def calcup(node):
        for o, c in child[node]:
            yield calcup(o)
        for o, c in child[node]:
            if s[0] == c:
                up[node][0] = 1
            else:
                up[node][0] = max(up[o][0], up[node][0])
            for i in range(1, m):
                if s[i] == c:
                    up[node][i] = max(up[node][i], 1 + up[o][i - 1])
                else:
                    up[node][i] = max(up[node][i], up[o][i])

        for j in range(1, m):
            up[node][j] = max(up[node][j], up[node][j - 1])
        yield None
    
    down = [[0 for _ in range(m)] for _ in range(n + 1)]
    
    @bootstrap
    def calcdown(node):
        for o, c in child[node]:
            if s[-1] == c:
                down[o][-1] = 1
            else:
                down[o][-1] = max(down[o][-1], down[node][-1])
            for i in range(m - 1):
                if s[i] == c:
                    down[o][i] = max(down[o][i], 1 + down[node][i + 1])
                else:
                    down[o][i] = max(down[o][i], down[node][i + 1])
            yield calcdown(o)
        
        for j in range(m - 2, -1, -1):
            down[node][j] = max(down[node][j], down[node][j + 1])
        yield None
    
    calcup(1)
    calcdown(1)

    print('up', up)
    print('down', down)

    res = 0
    for i in range(1, n + 1):
        for j in range(m):
            res = max(res, up[i][j] + down[i][j])
    
    print(res)

for testcase in range(II()):
    solve(testcase)