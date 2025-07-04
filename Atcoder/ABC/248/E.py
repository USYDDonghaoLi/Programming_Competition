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


def solve():
    n, x, y = MI()
    nums = LII()
    l, r = 0, 0

    def ops(l, r):
        print(nums[l : r])
        m = r - l
        res = m * (m + 1) // 2
        if x == y:
            return res
        else:
            stack = []
            for i in range(l, r):
                if nums[i] == x:
                    while stack and stack[-1][1] == 'x':
                        stack.pop()
                    stack.append((i, 'x'))
                    
                elif nums[i] == y:
                    stack.append((i, 'y'))
                else:
                    continue
            print('s', stack)
            return 0
                
    
    to_ret = 0
    while r < n:
        flag1 = False
        flag2 = False
        while r < n and y <= nums[r] and nums[r] <= x:
            if nums[r] == x:
                flag1 = True
            if nums[r] == y:
                flag2 = True
            r += 1
        if l != r and flag1 and flag2:
            to_ret += ops(l, r)
        r += 1
        l = r
solve()