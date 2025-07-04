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
#dfs - stack#
#check top!#

def solve():
    n, c = MI()
    bitres1 = [[1 for _ in range(n + 1)] for _ in range(30)]
    bitres0 = [[0 for _ in range(n + 1)] for _ in range(30)]

    for i in range(1, n + 1):
        t, x = MI()
        for bit in range(30):
            b = (x >> bit) & 1
            if t == 1:
                bitres1[bit][i] = bitres1[bit][i - 1] & b
                bitres0[bit][i] = bitres0[bit][i - 1] & b
            elif t == 2:
                bitres1[bit][i] = bitres1[bit][i - 1] | b
                bitres0[bit][i] = bitres0[bit][i - 1] | b
            else:
                bitres1[bit][i] = bitres1[bit][i - 1] ^ b
                bitres0[bit][i] = bitres0[bit][i - 1] ^ b
    
    BIT = [0 for _ in range(30)]
    for bit in range(30):
        if (c >> bit) & 1:
            BIT[bit] = 1
    
    for i in range(1, n + 1):
        for bit in range(30):
            if BIT[bit]:
                BIT[bit] = bitres1[bit][i]
            else:
                BIT[bit] = bitres0[bit][i]
        res = 0
        for bit in range(30):
            if BIT[bit]:
                res ^= 1 << bit
        print(res)
            

for _ in range(1):solve()