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

dp = [[0 for _ in range(3101)] for _ in range(3101)]
s = [[0 for _ in range(3101)] for _ in range(3101)]

def solve():
    n, p = MI()

    dp[0][0] = pow(25, p - 2, p) * 26 % p

    ten = [1, 10, 100, 1000, 10000, 100000]
    for i in range(1, n + 1):
        s[0][i] = dp[0][0]
    
    #s长度i t长度j#
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(1, 5):
                if i < k - 1:
                    continue
                else:
                    x = max(j - ten[k - 1] + 1, 0)
                    y = max(j - ten[k] + 1, 0)
                    dp[i][j] += (s[i - k - 1][x] - s[i - k - 1][y] + p) * 25
                    dp[i][j] %= p
            s[i][j + 1] = s[i][j] + dp[i][j]
            s[i][j + 1] %= p
    
    res = 0
    for i in range(1, n):
        res += dp[i][n]
    print(res % p)

solve()