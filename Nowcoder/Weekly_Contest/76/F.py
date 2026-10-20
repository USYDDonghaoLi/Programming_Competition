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

@lru_cache(None)
def g(x):
    if x == 0:
        return 1
    
    c = x
    c0 = 0
    c1 = 0
    
    while ((c & 1) == 0) and (c != 0):
        c0 += 1
        c >>= 1
    
    while (c & 1) == 1:
        c1 += 1
        c >>= 1
    
    if c0 + c1 == 31 or c0 + c1 == 0:
        return -1
    
    p = c0 + c1
    
    x |= (1 << p)
    
    x &= ~((1 << p) - 1)
    
    x |= (1 << (c1 - 1)) - 1
    
    return x

sys.setrecursionlimit(100010)

# @TIME
def solve(testcase):
    n = II()
    A = LII()
    A.sort()
    c = Counter(A)

    mp = defaultdict(int)

    @bootstrap
    def h(x):
        if x in mp:
            yield None
        else:
            nxt = g(x)
            if nxt not in c:
                mp[x] = 1
            else:
                if nxt not in mp:
                    yield h(nxt)
                mp[x] = mp[nxt] + 1
            yield None
    
    for a in A:
        h(a)
    
    res = -1
    M = 0

    for num in mp:
        # print(num, mp[num])
    #     print('h', num, h(num))
        if mp[num] > M:
            M = mp[num]
            res = num
    
    # print(M, res)

    print(M)

    ans = [res]

    for _ in range(M - 1):
        ans.append(g(ans[-1]))
    
    print(*ans)


for testcase in range(1):
    solve(testcase)
