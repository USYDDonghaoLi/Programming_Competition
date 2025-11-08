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

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)  # Index 0 is unused; tree[1] to tree[n] for positions 1 to n
    
    def fill(self, a):
        # Assumes a is 1-based list: a[0] unused or ignored, a[1] to a[n]
        for i in range(1, self.n + 1):
            self.update(i, a[i])

    def lowbit(self, x):
        return x & (-x)

    def update(self, pos, x):
        # pos is 1-based (1 to n)
        while pos <= self.n:
            self.tree[pos] += x
            pos += self.lowbit(pos)

    def query(self, pos):
        # Prefix sum from 1 to pos (inclusive)
        to_ret = 0
        while pos > 0:
            to_ret += self.tree[pos]
            pos -= self.lowbit(pos)
        return to_ret

    def query_sum(self, l, r):
        if l > r:
            return 0
        # Range sum from l to r (inclusive, 1-based)
        return self.query(r) - self.query(l - 1)

    def lower_bound(self, val):
        # Find the smallest index (1-based) where prefix sum >= val
        ret, su = 0, 0
        for i in reversed(range((self.n + 1).bit_length())):
            ix = ret + (1 << i)
            if ix <= self.n and su + self.tree[ix] < val:
                su += self.tree[ix]
                ret += 1 << i
        return ret + 1  # Adjust to 1-based if ret is 0-based internally
    
    def upper_bound(self, val):
        # Find the smallest index (1-based) where prefix sum > val
        ret, su = 0, 0
        for i in reversed(range((self.n + 1).bit_length())):
            ix = ret + (1 << i)
            if ix <= self.n and su + self.tree[ix] <= val:
                su += self.tree[ix]
                ret += 1 << i
        return ret + 1  # Adjust to 1-based

# @TIME
def solve(testcase):
    n = II()
    A = LII()

    B = list(sorted(set(A)))
    ID = defaultdict(int)
    for i, v in enumerate(B):
        ID[v] = i
    
    P = [0 for _ in range(n + 1)]
    Z = [0 for _ in range(n + 1)]

    for i in range(n):
        P[i + 1] = P[i] + A[i]
        Z[i + 1] = Z[i] + (A[i] == 0)

    q = II()
    sz = 300
    m = (n + sz - 1) // sz
    queries = [[] for _ in range(m)]

    for i in range(q):
        l, r = GMI()
        queries[l // sz].append((l, r + 1, i))
    
    for i in range(m):
        if i & 1:
            queries[i].sort(key = lambda x: -x[1])
        else:
            queries[i].sort(key = lambda x: x[1])
    
    cl, cr = 0, 0

    k = len(B)

    ft = FenwickTree(k)

    def f(l, r):
        mx = P[r] - P[l]
        if Z[r] - Z[l]:
            mx = fmax(mx, (P[r] - P[l]) ^ 1)
        cur = 0
        
        while True:
            v = ft.query(bisect_left(B, cur + 2))
            if v == cur:
                break
            else:
                cur = v
        
        if cur == P[r] - P[l]:
            if Z[r] - Z[l] != r - l and Z[r] - Z[l]:
                mx = fmax(mx, (cur + 1) ^ 1)
        
        return mx
    
    res = [-1 for _ in range(q)]

    for i in range(m):
        for l, r, idx in queries[i]:
            while cr < r:
                ft.update(ID[A[cr]] + 1, A[cr])
                cr += 1
            while cl > l:
                cl -= 1
                ft.update(ID[A[cl]] + 1, A[cl])
            while cr > r:
                cr -= 1
                ft.update(ID[A[cr]] + 1, -A[cr])
            while cl < l:
                ft.update(ID[A[cl]] + 1, -A[cl])
                cl += 1
            
            res[idx] = f(l, r)
    
    print("\n".join(map(str, res)))


for testcase in range(1):
    solve(testcase)