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
from math import ceil
#dfs - stack#
#check top!#

def solve():
    n = II()
    nums = LII()

    dp = [11000 for _ in range(8192)]
    dp[nums[0]] = 0.5 if nums[0] else 0
    S = set()
    S.add(nums[0])

    #到第i位，给第j位^j，使得前i个数都变成0的最小代价#
    for i in range(1, n):
        SS = set()#记录使用过的j#
        temp = [11000 for _ in range(8192)]
        m = 11000
        for j in S:
            m = min(dp[j], m)
        if nums[i]:
            temp[nums[i]] = min(temp[nums[i]], ceil(m) + 0.5)
            SS.add(nums[i])
        else:
            temp[0] = m
            SS.add(0)
        
        for j in S:
            if nums[i] ^ j == 0:
                temp[j] = min(temp[j], dp[j] + 0.5)
                SS.add(j)
            else:
                temp[nums[i] ^ j] = min(temp[nums[i] ^ j], ceil(dp[j]) + 0.5)
                SS.add(nums[i] ^ j)

        dp = temp[:]
        S = SS
        

    res = 11000
    for j in S:
        res = min(res, ceil(dp[j]))

    print(res)

for _ in range(II()):solve()

