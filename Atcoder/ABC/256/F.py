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

class BIT:

    #__slots__ = {'n', 'tree', 'MOD'}

    def __init__(self, n) -> None:
        self.n = n
        self.tree = [0 for _ in range(self.n)]
        self.MOD = 998244353
    
    def update(self, idx, val):
        while idx < self.n:
            self.tree[idx] += val
            self.tree[idx] += self.MOD
            self.tree[idx] %= self.MOD
            idx += idx & (-idx)
    
    def q(self, idx):
        res = 0
        while idx:
            res += self.tree[idx]
            res %= self.MOD
            idx -= idx & (-idx)
        return res
    
    def query(self, l, r):
        return (self.q(r) - self.q(l - 1) + self.MOD) % self.MOD 

def solve():
    n, q = MI()
    nums = LII()
    MOD = 998244353
    inv2 = pow(2, MOD - 2, MOD)

    bit1 = BIT(n + 10)
    bit2 = BIT(n + 10)
    bit3 = BIT(n + 10)

    for i, v in enumerate(nums):
        bit1.update(i + 1, (i + 1) ** 2 * v)
        bit2.update(i + 1, (i + 1) * v)
        bit3.update(i + 1, v)
    
    for _ in range(q):
        query = LII()
        if query[0] == 1:
            x, v = query[1], query[2]
            dv = v - nums[x - 1]
            bit1.update(x, x ** 2 * dv)
            bit2.update(x, x * dv)
            bit3.update(x, dv)
            nums[x - 1] = v
        else:
            x = query[1]
            ans1 = bit1.q(x)
            ans2 = bit2.q(x)
            ans3 = bit3.q(x)

            ans2 *= (2 * x + 3)
            ans2 %= MOD
            ans3 *= (x + 1) * (x + 2)
            ans3 %= MOD

            print(((ans1 - ans2 + ans3) % MOD + MOD) % MOD * inv2 % MOD)

solve()