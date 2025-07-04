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

    l, r = 0, 0
    res = 0
    while r < n:
        while r < n and nums[r] == nums[l]:
            r += 1
        res += l * (n - l)
        res += (n + n - r + 1 - l) * (r - l) // 2
        l = r
    #print('temp', res)

    for _ in range(q):
        idx, val = MI()
        idx -= 1
        if idx > 0:
            lval = nums[idx - 1]
        else:
            lval = -1
        
        if idx < n - 1:
            rval = nums[idx + 1]
        else:
            rval = -1
        
        curval = nums[idx]
        if curval == lval and curval == rval:
            if val == lval:
                pass
            else:
                res += idx * (n - idx)
                res += (idx + 1) * (n - idx - 1)
        elif curval == lval:
            if val == lval:
                pass
            elif val == rval:
                res += idx * (n - idx)
                res -= (idx + 1) * (n - idx - 1)
            else:
                res += idx * (n - idx)
        elif curval == rval:
            if val == rval:
                pass
            elif val == lval:
                res -= idx * (n - idx)
                res += (idx + 1) * (n - idx - 1)
            else:
                res += (idx + 1) * (n - idx - 1)
        else:
            if lval == rval:
                if val == lval:
                    res -= idx * (n - idx)
                    res -= (idx + 1) * (n - idx - 1)
                else:
                    pass
            else:
                if val == lval:
                    res -= idx * (n - idx)
                elif val == rval:
                    res -= (idx + 1) * (n - idx - 1)
                else:
                    pass
            
        nums[idx] = val
        #print('nums', nums)
        print(res)

for _ in range(1):solve()

