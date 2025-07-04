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
    s = I()
    n = len(s)

    #0alice 1tie 2bob
    @lru_cache(None)
    def dp(l, r):
        if l + 1 == r:
            if s[l] == s[r]:
                return 1
            else:
                return 0
        else:
            state = 2
            if s[l] > s[l + 1] or s[l] > s[r]:
                state = min(state, 2)
            elif s[l] == s[l + 1] and s[l] == s[r]:
                t1 = dp(l + 1, r - 1)
                t2 = dp(l + 2, r)
                state = min(state, max(t1, t2))
            elif s[l] == s[l + 1]:
                t = dp(l + 2, r)
                state = min(state, t)
            elif s[l] == s[r]:
                t = dp(l + 1, r - 1)
                state = min(state, t)
            else:
                state = min(state, 0)
        
            if s[r] > s[l] or s[r] > s[r - 1]:
                state = min(state, 2)
            elif s[r] == s[r - 1] and s[r] == s[l]:
                t1 = dp(l, r - 2)
                t2 = dp(l + 1, r - 1)
                state = min(state, max(t1, t2))
            elif s[r] == s[r - 1]:
                t = dp(l, r - 2)
                state = min(state, t)
            elif s[r] == s[l]:
                t = dp(l + 1, r - 1)
                state = min(state, t)
            else:
                state = min(state, 0)
            
            return state


    s = dp(0, n - 1)
    if s == 0:
        print('Alice')
    elif s == 1:
        print('Draw')
    else:
        print('Bob')

for _ in range(II()):solve()