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

MOD = 998244353
facts = [1 for _ in range(410)]
factsinv = [1 for _ in range(410)]

for i in range(2, 410):
    facts[i] = facts[i - 1] * i % MOD
factsinv[-1] = pow(facts[-1], MOD - 2, MOD)
for i in range(408, 0, -1):
    factsinv[i] = factsinv[i + 1] * (i + 1) % MOD

def comb(n, m):
    return facts[n] * factsinv[m] % MOD * factsinv[n - m] % MOD

def solve():
    n = II()
    idxs = defaultdict(list)
    grid = [[-1 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        line = LII()
        for j in range(n):
            grid[i][j] = line[j]
            idxs[line[j]].append((i, j))    

    def calc1(num):
        m = len(idxs)
        ret = m

        for i in range(m):
            x1, y1 = idxs[num][i]
            for j in range(i + 1, m):
                x2, y2 = idxs[num][j]
                if y1 <= y2:
                    ret += comb(x2 - x1 + y2 - y1, x2 - x1)
                    ret %= MOD
        
        return ret
    
    def calc2(num):
        ret = 0
        dp = [[0 for _ in range(n)] for _ in range(n)]
        for x, y in idxs[num]:
            dp[x][y] = 1
        for i in range(1, n):
            dp[i][0] += dp[i - 1][0]
            dp[i][0] %= MOD
        for j in range(1, n):
            dp[0][j] += dp[0][j - 1]
            dp[0][j] %= MOD
        for i in range(1, n):
            for j in range(1, n):
                dp[i][j] += dp[i - 1][j] + dp[i][j - 1]
                dp[i][j] %= MOD
        
        for i in range(n):
            for j in range(n):
                if grid[i][j] == num:
                    ret += dp[i][j]
                    ret %= MOD
        
        return ret


    res = 0
    for num in idxs:
        m = len(idxs)
        if m <= n:
            res += calc1(num)
        else:
            res += calc2(num)
        #print(num, res)
        res %= MOD

    print(res)

solve()