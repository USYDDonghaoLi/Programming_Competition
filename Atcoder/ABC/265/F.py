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
#dfs - stack#
#check top!#

mod = 998244353

def solve():
    N, D = MI()
    p = LII()
    q = LII()

    dp = [[0 for _ in range(D + 1)] for _ in range(D + 1)]
    dp[0][0] = 1

    for n in range(N):
        pn, qn = p[n], q[n]
        s = abs(pn - qn)
        nxt = [[0 for _ in range(D + 1)] for _ in range(D + 1)]

        #calculating diagonal persum1 (i, j) -> (i + 1, j - 1)#
        dp2 = [[0 for _ in range(D + 1)] for _ in range(D + 1)]
        for i in range(D + 1):
            for j in range(D + 1):
                dp2[i][j] = dp[i][j]
                if i != 0 and j != D:
                    dp2[i][j] += dp2[i - 1][j + 1]
                    dp2[i][j] %= mod

        #from (0, s) to (s, 0)# 
        for i in range(D + 1):
            for j in range(D + 1):
                si = i
                sj = j - s
                if sj < 0:
                    si += sj
                    sj = 0
                if 0 <= si <= D and 0 <= sj <= D:
                    nxt[i][j] += dp2[si][sj]
                    nxt[i][j] %= mod
                
                ti = i - (s + 1)
                tj = j + 1
                if 0 <= ti <= D and 0 <= tj <= D:
                    nxt[i][j] -= dp2[ti][tj]
                    nxt[i][j] %= mod
        
        #calculating diagonal presum2 (i, j) -> (i + 1, j + 1)#
        dp3 = [[0 for _ in range(D + 1)] for _ in range(D + 1)]
        for i in range(D + 1):
            for j in range(D + 1):
                dp3[i][j] = dp[i][j]
                if i and j:
                    dp3[i][j] += dp3[i - 1][j - 1]
                    dp3[i][j] %= mod
                if i + 1 <= D and j + s + 1 <= D:
                    nxt[i + 1][j + s + 1] += dp3[i][j]
                    dp3[i + 1][j + s + 1] %= mod
                if i + s + 1 <= D and j + 1 <= D:
                    nxt[i + s + 1][j + 1] += dp3[i][j]
                    nxt[i + s + 1][j + 1] %= mod
        
        dp = nxt

    print(sum(sum(v) for v in dp) % mod)
for _ in range(1):solve()

