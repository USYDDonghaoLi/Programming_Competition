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

mod = 998244353

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0 for _ in range(n)]
    
    def fill(self, a):
        for i in range(self.n):
            self.update(i, a[i])

    def lowbit(self, x):
        return x & (-x)

    def update(self, pos, x):
        pos += 1
        while pos <= self.n:
            self.tree[pos - 1] += x
            self.tree[pos - 1] %= mod
            pos += self.lowbit(pos)

    def query(self, pos):
        to_ret = 0
        while pos:
            to_ret += self.tree[pos - 1]
            to_ret %= mod
            pos -= self.lowbit(pos)
        return to_ret

    def query_sum(self, l, r):
        return (self.query(r) - self.query(l)) % mod

    def lower_bound(self, val):
        ret, su = 0, 0
        for i in reversed(range(self.n.bit_length())):
            ix = ret + (1 << i)
            if ix < self.n and su + self.tree[ix] < val:
                su += self.tree[ix]
                ret += 1 << i
        return ret
    
    def upper_bound(self, val):
        ret, su = 0, 0
        for i in reversed(range(self.n.bit_length())):
            ix = ret + (1 << i)
            if ix < self.n and su + self.tree[ix] <= val:
                su += self.tree[ix]
                ret += 1 << i
        return ret

pw2 = [1 for _ in range(200010)]
for i in range(1, 200010):
    pw2[i] = pw2[i - 1] * 2 % mod

# @TIME
def solve(testcase):
    s = I()
    n = len(s)

    s = [int(c) for c in s]

    pre = [FenwickTree(n + 10) for _ in range(2)]
    suf = [FenwickTree(n + 10) for _ in range(2)]

    for i, a in enumerate(s):
        pre[a].update(i, pw2[i])
        suf[a].update(i, pw2[n - 1 - i])
    
    A = [[0 for _ in range(2)] for _ in range(n + 10)]
    for i in range(n - 1, -1, -1):
        A[i][0] = A[i + 1][0]
        A[i][1] = A[i + 1][1]
        A[i][s[i]] = (A[i][s[i]] + pw2[n - 1 - i]) % mod

    res = pw2[n] - 1
    for i in range(n):
        res = (res + A[i + 1][1 - s[i]] * pw2[i]) % mod
    
    ans = []

    q = II()
    queries = LII()
    for i in range(q):
        x = queries[i] - 1

        if x + 1 < n:
            res -= pw2[x] * suf[1 - s[x]].query_sum(x + 1, n)
            res += pw2[x] * suf[s[x]].query_sum(x + 1, n)

        if x:
            res -= pw2[n - 1 - x] * pre[1 - s[x]].query_sum(0, x)
            res += pw2[n - 1 - x] * pre[s[x]].query_sum(0, x)
        
        res %= mod
        
        pre[s[x]].update(x, -pw2[x])
        suf[s[x]].update(x, -pw2[n - 1 - x])
        s[x] = 1 - s[x]
        pre[s[x]].update(x, pw2[x])
        suf[s[x]].update(x, pw2[n - 1 - x])

        ans.append(res)
    
    print(*ans)


for testcase in range(II()):
    solve(testcase)