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
        while pos < self.n:
            self.tree[pos] += x
            pos += self.lowbit(pos)

    def query(self, pos):
        to_ret = 0
        while pos:
            to_ret += self.tree[pos]
            pos -= self.lowbit(pos)
        return to_ret

    def query_sum(self, l, r):
        return self.query(r) - self.query(l - 1)

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

# @TIME
def solve(testcase):
    n = II()
    nums = LII()
    mx = n * 60
    base = n * 20
    
    count2 = [0 for _ in range(n + 1)]
    count5 = [0 for _ in range(n + 1)]
    F2, FC2, F5, FC5 = FenwickTree(mx + 10), FenwickTree(mx + 10), FenwickTree(mx + 10), FenwickTree(mx + 10)
    FC2.update(base, 1)
    FC5.update(base, 1)
    
    res = 0
    for i, v in enumerate(nums, 1):
        t = 0
        while v % 2 == 0:
            t += 1
            v //= 2
        count2[i] = count2[i - 1] + t
        t = 0
        while v % 5 == 0:
            t += 1
            v //= 5
        count5[i] = count5[i - 1] + t
    
        diff = count2[i] - count5[i]
        sum5 = F5.query(diff + base)
        cnt5 = FC5.query(diff + base)
        sum2 = F2.query_sum(diff + base + 1, mx)
        cnt2 = FC2.query_sum(diff + base + 1, mx)
        
        res += count5[i] * cnt5 - sum5
        res += count2[i] * cnt2 - sum2
        
        F2.update(diff + base, count2[i])
        FC2.update(diff + base, 1)
        F5.update(diff + base, count5[i])
        FC5.update(diff + base, 1)
    
    print(res)

for testcase in range(1):
    solve(testcase)