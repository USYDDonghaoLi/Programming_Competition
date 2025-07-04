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
#dfs - stack#

class SegTree:
    def __init__(self, n) -> None:
        self.tree = [0 for _ in range(8 * n + 1)]
        self.lazy = [(0, 0) for _ in range(8 * n + 1)]
        self.n = n
        self.MOD = 998244353
        self.inv2 = pow(2, self.MOD - 2, self.MOD)
    
    def _bulid(self, arr):
        self.nums = arr
        self.build(1, 1, self.n)
    
    def build(self, pos, l, r):
        if l == r:
            self.tree[pos] = self.nums[l]
        else:
            mid = (l + r) >> 1
            self.build(pos + pos, l, mid)
            self.build(pos + pos + 1, mid + 1, r)
            self.tree[pos] = self.tree[pos + pos] + self.tree[pos + pos + 1]
    
    
    def _update(self, left, right, val):
        self.update(1, 1, self.n, left, right, val)
    
    def update(self, pos, l, r, left, right, val):
        if l == left and r == right:
            self.pushdown(pos, l, r)
            self.lazy[pos] = (val, l - left + 1)
        
        else:
            self.tree[pos] += val * (right - left + 1) % self.MOD * (right - left + 2) % self.MOD * self.inv2 % self.MOD
            mid = (l + r) >> 1

            if left <= mid:
                if right <= mid:
                    self.update(pos + pos, l, mid, left, right, val)
                else:
                    self.update(pos + pos, l, mid, left, mid, val)
                    self.update(pos + pos + 1, mid + 1, r, mid + 1, right, val)
            else:
                self.update(pos + pos + 1, mid + 1, r, left, right, val)
    
    def _query(self, left, right):
        print(self.query(1, 1, self.n, left, right))
    
    def query(self, pos, l, r, left, right):
        if l == left and r == right:
            val, mul = self.lazy[pos]
            return self.tree[pos] + val * (mul + mul + right - left + 1) % self.MOD * (right - left + 1) % self.MOD * self.inv2 * self.MOD
        
        else:
            if self.lazy[pos] != (0, 0):
                self.pushdown(pos, l, r)
            mid = (l + r) >> 1

            if left <= mid:
                if right <= mid:
                    return self.query(pos + pos, l, mid, left, right)
                else:
                    return self.query(pos + pos, l, mid, left, mid) + self.query(pos + pos + 1, mid + 1, r, mid + 1, right)
            else:
                return self.query(pos + pos + 1, mid + 1, r, left, right)
    
    def pushdown(self, pos, l, r):
        val, mul = self.lazy[pos]
        mid = l + r >> 1
        self.tree[pos] += val * (mul + mul + r - l + 1) % self.MOD * (r - l + 1) % self.MOD * self.inv2 * self.MOD
        if self.tree[pos << 1]:
            self.pushdown(pos << 1, l, mid)
        if self.tree[pos << 1 | 1]:
            self.pushdown(pos << 1 | 1, mid + 1, r)
        self.lazy[pos] = (0, 0)
        self.lazy[pos << 1] = (val, mul)
        self.lazy[pos << 1 | 1] = (val, mul + mid - l + 2)

def solve():
    MOD = 998244353
    n, q = MI()
    nums = [0] + LII()
    st = SegTree(n + 10)
    for i in range(1, n + 1):
        st._update(i, i, nums[i])
        print('tree', st.tree)
    
    for _ in range(q):
        haha = LII()
    
solve()