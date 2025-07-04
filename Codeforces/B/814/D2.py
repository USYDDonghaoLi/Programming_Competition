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

def solve():
    # n = II()
    # nums = [0] + LII()

    # px = [0 for _ in range(n + 1)]
    # for i in range(1, n + 1):
    #     px[i] = px[i - 1] ^ nums[i]
    # dp = [float('inf') for _ in range(n + 1)]
    # dp[0] = 0
    # mp = defaultdict(int)

    # for i in range(1, n + 1):
    #     mp[px[i - 1]] = i - 1
    #     dp[i] = dp[i - 1] + 1
    #     if px[i] in mp:
    #         dp[i] = min(dp[i], dp[mp[px[i]]] + i - mp[px[i]] - 1)
    
    # print(dp[-1])

    n = II()
    nums = LII()
    ps = [0 for _ in range(n + 1)]

    for bit in range(30):
        l, r = 0, 0
        while r < n:
            while r < n and not nums[r] >> bit & 1:
                r += 1
            l = r
            if r == n:
                break
            while r < n and nums[r] >> bit & 1:
                r += 1
            ps[r] -= 1
            ps[l] += 1
            l = r
    
    for i in range(1, n + 1):
        ps[i] += ps[i - 1]
    
    print('ps', ps)

    l, r = 0, 0
    res = 0
    while r < n:
        while r < n and not ps[r]:
            r += 1
        l = r
        if r == n:
            break
        
        while r < n and ps[r] == ps[l]:
            r += 1
        res += r - l + 1 >> 1
        l = r
    
    print(res)

for _ in range(II()):solve()

