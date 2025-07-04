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
from math import gcd
sys.setrecursionlimit(2 ** 31 - 1)

class SegmentTree:

    __slots__ = {'n', 'tree', 'nums', 'func'}

    def __init__(self, nums, func, ide_ele) -> None:
        self.n = len(nums) - 1
        self.tree = [ide_ele for _ in range(4 * self.n + 10)]
        self.nums = nums
        self.func = func
        self._build()
    
    def _build(self):
        self.build(1, 1, self.n)
    
    def build(self, pos, left, right):
        if left == right:
            self.tree[pos] = self.nums[left]
        else:
            mid = left + right >> 1
            self.build(pos << 1, left, mid)
            self.build(pos << 1 | 1, mid + 1, right)
            self.tree[pos] = self.func(self.tree[pos << 1], self.tree[pos << 1 | 1])

    def _query(self, l, r):
        return self.query(1, 1, self.n, l, r)
    
    def query(self, pos, left, right, l, r):
        if left == l and right == r:
            return self.tree[pos]
        else:
            mid = left + right >> 1
            if l <= mid:
                if r <= mid:
                    return self.query(pos << 1, left, mid, l, r)
                else:
                    return self.func(self.query(pos << 1, left, mid, l, mid), self.query(pos << 1 | 1, mid + 1, right, mid + 1, r))
            else:
                return self.query(pos << 1 | 1, mid + 1, right, l, r)


def solve():
    n, q = MI()
    A = LII()
    B = LII()

    diffA = [0] + [abs(A[i] - A[i - 1]) for i in range(1, n)]
    diffB = [0] + [abs(B[i] - B[i - 1]) for i in range(1, n)]
    if n > 1:
        Ast = SegmentTree(diffA, gcd, 0)
        Bst = SegmentTree(diffB, gcd, 0)
    
        for _ in range(q):
            h1, h2, w1, w2 = MI()
            temp = A[h1 - 1] + B[w1 - 1]

            if h1 != h2:
                a = Ast._query(h1, h2 - 1)
                if w1 != w2:
                    b = Bst._query(w1, w2 - 1)
                    print(gcd(temp, gcd(a, b)))
                else:
                    print(gcd(temp, a))
            else:
                if w1 != w2:
                    b = Bst._query(w1, w2 - 1)
                    print(gcd(temp, b))
                else:
                    print(temp)
    else:
        for _ in range(q):
            h1, h2, w1, w2 = MI()
            print(A[0] + B[0])
solve()