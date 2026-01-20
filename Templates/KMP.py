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

class KMP:
    def __init__(self, s, p):
        self.n, self.m = len(s), len(p)
        self.s = ' ' + s
        self.p = ' ' + p

        #最大公共前后缀长度#
        self.nxt = [0 for _ in range(self.m + 1)]
        #匹配到的最大长度#
        self.f = [0 for _ in range(self.n + 1)]
    
    def NEXT(self):
        j = 0
        for i in range(2, self.m + 1):
            while j > 0 and self.p[j + 1] != self.p[i]:
                j = self.nxt[j]
            if self.p[j + 1] == self.p[i]:
                j += 1
            self.nxt[i] = j
    
    def sol(self):
        self.NEXT()
        j = 0
        for i in range(1, self.n + 1):
            while j == self.m or (j > 0 and self.p[j + 1] != self.s[i]):
                j = self.nxt[j]
            if self.p[j + 1] == self.s[i]:
                j += 1
            self.f[i] = j

def solve():
    s = I()
    p = I()
    n, m = len(s), len(p)
    kmp = KMP(s, p)
    kmp.sol()
    
    for i, v in enumerate(kmp.f):
        if v == m:
            print(i - m + 1)
    
    print(*kmp.nxt[1:])

for _ in range(1):solve()