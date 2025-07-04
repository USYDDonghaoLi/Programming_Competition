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
    n, q = MI()
    nums = LII()
    qs = []
    for j in range(q):
        i, k = MI()
        i -= 1
        qs.append((k, i, j))
    qs.sort()
    idx = 0

    res = [-1 for _ in range(q)]
    mp = defaultdict(int)

    M, index = 0, -1
    for i in range(n):
        if nums[i] > M:
            M = nums[i]
            index = i

    curtime = 1
    l, r = 0, 1
    while curtime < n:

        if nums[l] < nums[r]:
            mp[r] += 1
            l = r
            r += 1
        else:
            mp[l] += 1
            r += 1
        
        while qs[idx][0] == curtime:
            i, j = qs[idx][1], qs[idx][2]
            res[j] = mp[i]
            idx += 1
        
            if idx == q:
                break
        
        curtime += 1


    for i in range(idx, q):
        mp[index] += qs[i][0] + 1 - curtime
        curtime = qs[i][0] + 1
        res[qs[i][2]] = mp[qs[i][1]]
    
    for i in range(q):
        print(res[i])
    
for _ in range(II()):solve()

