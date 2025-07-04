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
#check top!#

class FenwickTree_max:
    def __init__(self,n):
        self.tree =[0 for _ in range(n)]
        self.nums = [0 for _ in range(n)]
        self.n = n
    
    def lowbit(self, x):
        return x & (-x)
    
    def update(self, idx, val):
        self.nums[idx] = val
        while idx < self.n:
            self.tree[idx] = val
            lx = self.lowbit(idx)
            i = 1
            while i < lx:
                self.tree[idx] = max(self.tree[idx], self.tree[idx - i])
                i <<= 1
            idx += self.lowbit(idx)

    def query(self, l, r):
        ans = float('-inf')
        while r >= l:
            ans = max(self.nums[r], ans)
            r -= 1
            while r - self.lowbit(r) >= l:
                ans = max(self.nums[r], ans)
                ans = max(self.tree[r], ans)
                r -= self.lowbit(r)
        return ans

def solve():
    n, m = MI()
    nums = [0] + LII()
    tree = FenwickTree_max(m + 10)
    for i in range(1, m + 1):
        tree.update(i, nums[i])

    def check(lx, ly, rx, ry):
        if ry < ly:
            lx, ly, rx, ry = rx, ry, lx, ly

        q, r = divmod(n, k)
        ql, rl = divmod(lx, k)
        qr, rr = divmod(rx, k)

        if r >= rl:
            lx = q * k + rl
        else:
            lx = (q - 1) * k + rl
        
        if r >= rr:
            rx = q * k + rr
        else:
            rx = (q - 1) * k + rr

        M = tree.query(ly, ry)
        return lx > M and rx > M


    q = II()
    for _ in range(q):
        xs, ys, xf, yf, k = MI()

        if abs(xf - xs) % k or abs(yf - ys) % k:
            print('NO')
        else:
            if check(xs, ys, xf, yf):
                print('YES')
            else:
                print('NO')
for _ in range(1):solve()