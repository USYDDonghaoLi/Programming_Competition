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
sys.setrecursionlimit(2 ** 31 - 1)

class BIT:

    def __init__(self, n) -> None:
        self.n = n
        self.bit = [0 for _ in range(self.n + 1)]
    
    def build(self, arr):
        for idx, val in enumerate(arr):
            self.update(idx, val)
    
    def update(self, idx, val):
        idx += 1
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx
    
    def _query(self, left, right):
        return self.query(right) - self.query(left)
    
    def query(self, idx):
        res = 0
        while idx:
            res += self.bit[idx]
            idx -= idx & -idx
        return res


def solve():
    n, m, q = MI()
    prev = [(-1, 0) for i in range(n)]

    T = [-1 for _ in range(q)]
    A = [-1 for _ in range(q)]
    B = [-1 for _ in range(q)]
    C = [-1 for _ in range(q)]

    subt = [[] for _ in range(q)]
    ans = []

    for i in range(q):
        line = LII()
        try:
            t, a, b, c = line
        except:
            t, a, b = line
        
        T[i] = t
        if t == 1:
            a -= 1
            b -= 1
            A[i], B[i], C[i] = a, b, c
        elif t == 2:
            a -= 1
            A[i], B[i] = a, b
            prev[a] = (i, b)
        else:
            c = len(ans)
            a -= 1
            b -= 1
            A[i], B[i], C[i] = a, b, c
            j, x = prev[a]
            ans.append(x)
            if j >= 0:
                subt[j].append(i)
    
    bit = BIT(m + 1)
    for i, (t, a, b, c) in enumerate(zip(T, A, B, C)):
        if t == 1:
            bit.update(a, c)
            bit.update(b + 1, -c)
        elif t == 2:
            for j in subt[i]:
                ans[C[j]] -= bit._query(0, B[j] + 1)
        else:
            ans[c] += bit._query(0, b + 1)
    
    for a in ans:
        print(a)
solve()
