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
#dfs - stack#
#check top!#

def solve():
    n = II()
    nums = LII()

    res = []
    idxs = []
    for i in range(n):
        if nums[i] & 1:
            idxs.append(i)
    t = 0
    for i in range(0, n + (n & 1), 2):
        idx = idxs[t]
        t += 1

        if idx >= i:
            if (idx ^ i) & 1:
                for j in range(idx - 2, i - 1, -2):
                    res.append(('B', j + 1))
                    nums[j], nums[j + 2] = nums[j + 2], nums[j]
                res.append(('A', i + 1))
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
            else:
                for j in range(idx - 2, i - 2, -2):
                    res.append(('B', j + 1))
                    nums[j], nums[j + 2] = nums[j], nums[j + 2]
        else:
            if (idx ^ i) & 1:
                for j in range(idx, i - 1, 2):
                    res.append(('B', j + 1))
                    nums[j], nums[j + 2] = nums[j + 2], nums[j]
                res.append(('A', i))
                nums[i - 1], nums[i] = nums[i], nums[i - 1]
            else:
                for j in range(idx, i, 2):
                    res.append(('B', j + 1))
                    nums[j], nums[j + 2] = nums[j], nums[j + 2]
    print(nums)
    
    for i in range(1, n + (n & 1), 2):
        idx = -1
        need = i - 1
        for j in range(n):
            if nums[j] == i:
                idx = j
                break
        if need >= j:
            for k in range(j, need, 2):
                res.append(('B', k + 1))
                nums[k], nums[k + 2] = nums[k + 2], nums[k]
        else:
            for k in range(j - 2, need, -2):
                res.append(('B', k + 1))
                nums[k], nums[k + 2] = nums[k + 2], nums[k]
    
    for i in range(2, n + (n & 1), 2):
        idx = -1
        need = i - 1
        for j in range(n):
            if nums[j] == i:
                idx = j
                break
        if need >= j:
            for k in range(j, need, 2):
                res.append(('B', k + 1))
                nums[k], nums[k + 2] = nums[k + 2], nums[k]
        else:
            for k in range(j - 2, need, -2):
                res.append(('B', k + 1))
                nums[k], nums[k + 2] = nums[k + 2], nums[k]
        
    print(nums)
    print(len(res))
    for a, b in res:
        print(a, b)


for _ in range(1):solve()

