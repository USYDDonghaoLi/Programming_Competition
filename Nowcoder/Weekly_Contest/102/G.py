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

#f(a, a) = a#
class SpraseTable:
    def __init__(self, v, op, e) -> None:
        self.n = len(v)
        self.op = op
        self.e = e
        self.v = v
        self.l = (self.n).bit_length()
        self.info=[[e for _ in range(self.l)] for _ in range(self.n)]
        for i in range(self.n):
            self.info[i][0] = self.v[i]
        
        for i in range(1, self.l):
            for j in range(self.n):
                if j + (1 << i) - 1 < self.n:
                    self.info[j][i] = self.op(self.info[j][i - 1], self.info[j + (1 << (i - 1))][i - 1])
    
        self.log2 = [-1 for _ in range(self.n + 1)]
        self.log2[1] = 0
        for i in range(2, self.n + 1):
            self.log2[i] = self.log2[i >> 1] + 1
    
    def query(self, l, r):
        s = self.log2[r - l + 1]
        return self.op(self.info[l][s], self.info[r - (1 << s) + 1][s])

# @TIME
def solve(testcase):
    n, q = MI()
    A = LII()

    st = SpraseTable(A, fmax, 0)

    sz = int(sqrt(n))
    queries = [[] for _ in range(sz + 10)]

    res = ['' for _ in range(q)]

    for i in range(q):
        l, r = GMI()
        LEN = r - l + 1
        if LEN & 1:
            res[i] = 'No'
        else:
            queries[l // sz].append((l, r, i))
    
    for i in range(sz + 10):
        if i & 1:
            queries[i].sort(key = lambda x: -x[1])
        else:
            queries[i].sort(key = lambda x: x[1])
    
    cl, cr = 0, -1
    f = [0 for _ in range(200010)]
    cnt = [0 for _ in range(200010)]
    cnt[0] = inf
    cm = 0

    def add(val):
        nonlocal cm
        old_f = f[val]
        cnt[old_f] -= 1
        f[val] += 1
        new_f = f[val]
        cnt[new_f] += 1
        if new_f > cm:
            cm = new_f
    
    def rm(val):
        nonlocal cm
        old_f = f[val]
        cnt[old_f] -= 1
        f[val] -= 1
        new_f = f[val]
        cnt[new_f] += 1
        while not cnt[cm]:
            cm -= 1

    for i in range(sz + 10):
        for l, r, idx in queries[i]:
            while cr < r:
                cr += 1
                add(A[cr])
            while cl > l:
                cl -= 1
                add(A[cl])
            
            while cr > r:
                rm(A[cr])
                cr -= 1
            while cl < l:
                rm(A[cl])
                cl += 1
            
            LEN = r - l + 1 >> 1
            m = st.query(l, r)

            if m > LEN:
                res[idx] = 'No'
            else:
                if cm > 2:
                    res[idx] = 'No'
                else:
                    res[idx] = 'Yes'
    
    print('\n'.join(res))


for testcase in range(1):
    solve(testcase)