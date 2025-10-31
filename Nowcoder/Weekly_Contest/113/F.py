'''
Hala Madrid!
https://github.com/USYDDonghaoLi/Programming_Competition
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

'''
495 = 11 * 3 * 3 * 5
'''

class SegTree:

    __slots__ = {'n', 'op', 'e', 'log', 'size', 'd'}

    def __init__(self, V, OP, E):
        '''
        V: 原始数组
        OP: 维护的运算(min, max, sum...)
        E: 线段树初值
        '''
        self.n = len(V)
        self.op = OP
        self.e = E
        self.log = (self.n - 1).bit_length()
        self.size = 1 << self.log
        self.d=[E for _ in range(2*self.size)]
        for i in range(self.n):
            self.d[self.size + i] = V[i]
        for i in range(self.size - 1, 0, -1):
            self.update(i)

    def set(self, p, x):
        assert 0 <= p and p < self.n
        p += self.size
        self.d[p] = x
        for i in range(1, self.log + 1):
            self.update(p >> i)

    def get(self, p):
        assert 0 <= p and p <self.n
        return self.d[p + self.size]

    def prod(self, l ,r):
        #[l, r)
        assert 0 <= l and l <= r and r <= self.n
        sml = self.e
        smr = self.e
        l += self.size
        r += self.size

        while(l < r):
            if (l & 1):
                sml = self.op(sml, self.d[l])
                l += 1
            if (r & 1):
                smr = self.op(self.d[r - 1], smr)
                r -= 1
            l >>= 1
            r >>= 1
        return self.op(sml, smr)

    def all_prod(self):
        return self.d[1]

    def max_right(self, l, f):
        assert 0 <= l and l <= self.n
        assert f(self.e)
        if l == self.n:
            return self.n
        l += self.size
        sm = self.e
        while(1):
            while(l % 2 == 0):
                l >>= 1
            if not(f(self.op(sm, self.d[l]))):
                while(l < self.size):
                    l = 2 * l
                    if f(self.op(sm, self.d[l])):
                        sm = self.op(sm, self.d[l])
                        l += 1
                return l - self.size
            sm = self.op(sm,self.d[l])
            l += 1
            if (l & -l) == l:
                break
        return self.n
    def min_left(self, r, f):
        assert 0 <= r and r < self.n
        assert f(self.e)
        if r == 0:
            return 0
        r += self.size
        sm = self.e
        while(1):
            r -= 1
            while(r > 1 and (r % 2)):
                r >>= 1
            if not(f(self.op(self.d[r], sm))):
                while(r < self.size):
                    r = (2 * r + 1)
                    if f(self.op(self.d[r], sm)):
                        sm=self.op(self.d[r], sm)
                        r -= 1
                return r + 1 - self.size
            sm = self.op(self.d[r] ,sm)
            if (r & -r) == r:
                break
        return 0

    def update(self, k):
        self.d[k] = self.op(self.d[2 * k], self.d[2 * k + 1])
        
    def __str__(self):
        return str([self.get(i) for i in range(self.n)])

d = {
    0: 1,
    1: 3,
    9: 5,
    10: 11,
    11: 5 * 11,
    2: 3 * 5,
    3: 3 * 11,
    4: 3 * 5 * 11,
    5: 3 * 3,
    6: 3 * 3 * 5,
    7: 3 * 3 * 11,
    8: 3 * 3 * 5 * 11,
}


d2 = {v: i for i, v in d.items()}

good = [[] for _ in range(12)]

for i in range(12):
    for j in range(i, 12):
        if d[i] * d[j] % 495 == 0:
            good[i].append(j)

# print('good', good)

# @TIME
def solve(testcase):
    n, q = MI()

    A = LII()

    V = []
    E = [0 for _ in range(12)]

    for a in A:
        flag = -1
        for v in d2:
            if a % v == 0:
                flag = d2[v]
        
        v = [0 for _ in range(12)]
        v[flag] = 1
        V.append(v)
    
    sg = SegTree(
        V,
        lambda x, y: [
            a + b for a, b in zip(x, y)
        ],
        E
    )

    # print('sg', sg)

    for _ in range(q):
        ops = LII()
        op = ops[0]

        if op == 1:
            x, y = ops[1] - 1, ops[2]
            flag = -1
            for v in d2:
                if y % v == 0:
                    flag = d2[v]
            
            v = [0 for _ in range(12)]
            v[flag] = 1
            sg.set(x, v)
        else:
            l, r = ops[1] - 1, ops[2] - 1
            res = 0
            ans = sg.prod(l, r + 1)
            # print('ans', list(ans))

            for i in range(12):
                for j in good[i]:
                    if i == j:
                        res += ans[i] * (ans[i] - 1) // 2
                    else:
                        res += ans[i] * ans[j]
            print(res)

for testcase in range(1):
    solve(testcase)