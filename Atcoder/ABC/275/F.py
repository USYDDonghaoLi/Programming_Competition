'''
Hala Madrid!
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
from math import log, gcd, sqrt

def solve():
    n, m = MI()
    nums = LII()
    dp = [[[float('inf') for _ in range(2)] for _ in range(m + 1)] for _ in range(n)]
    #下标为i的数，和为j，删(1)或者不删(0)这个数字，最小要删几段
    mp = defaultdict(lambda : float('inf'))

    dp[0][nums[0]][0] = 0
    dp[0][0][1] = 1
    mp[0] = 1
    mp[nums[0]] = 0 if n == 1 else 1

    for i in range(n - 1):
        for j in range(m + 1):
            if j + nums[i + 1] <= m:
                dp[i + 1][j + nums[i + 1]][0] = min(dp[i + 1][j + nums[i + 1]][0], dp[i][j][0], dp[i][j][1])
                mp[j + nums[i + 1]] = min(mp[j + nums[i + 1]], dp[i + 1][j + nums[i + 1]][0] + (i != n - 2))
            dp[i + 1][j][1] = min(dp[i + 1][j][1], dp[i][j][1], dp[i][j][0] + 1)
            mp[j] = min(mp[j], dp[i + 1][j][0] + (i != n - 2))
    
    for i in range(1, m + 1):
        if i in mp:
            print(mp[i])
        else:
            print(-1)

for _ in range(1):solve()