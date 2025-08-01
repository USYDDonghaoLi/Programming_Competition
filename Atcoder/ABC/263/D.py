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
    n, l, r = MI()
    nums = LII()

    leftsum = [0 for _ in range(n)]
    rightsum = [0 for _ in range(n)]

    for i in range(n):
        if not i:
            leftsum[i] = l - nums[i]
        else:
            leftsum[i] = leftsum[i - 1] + l - nums[i]
    
    #print(leftsum)
    #print(nums)

    for i in range(n - 1, -1, -1):
        if i == n - 1:
            rightsum[i] = r - nums[i]
        else:
            rightsum[i] = rightsum[i + 1] + r - nums[i]
    
    
    for i in range(1, n):
        leftsum[i] = min(leftsum[i - 1], leftsum[i])
    for i in range(n - 2, -1, -1):
        rightsum[i] = min(rightsum[i], rightsum[i + 1])
    
    #print(leftsum)
    #print(rightsum)
    d = 0
    d = min(d, leftsum[n - 1])
    d = min(d, rightsum[0])

    for i in range(n - 1):
        d = min(d, leftsum[i] + rightsum[i + 1])
    #print(d)

    print(sum(nums) + d)
for _ in range(1):solve()