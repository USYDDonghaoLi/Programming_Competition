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
from math import gcd
#dfs - stack#
#check top!#

class BSGS:
    #solving problem like a ** x = b (mod m)#
    
    def solution(self, a, b, m, k = 1):
        d = dict()
        cur = 1
        t = int(m ** .5) + 1
        for B in range(1, t + 1):
            cur *= a
            cur %= m
            d[b * cur % m] = B
        
        now = cur * k % m
        for A in range(1, t + 1):
            if now in d:
                return A * t - d[now]
            now *= cur
            now %= m
        
        return float('-inf')
    
    def exBSGS(self, a, b, m, k = 1):
        a %= m; A = a
        b %= m; B = b
        M = m

        cur = 1 % m
        for i in range(10000):
            if cur == B:
                return i
            cur *= A
            cur %= M
            d = gcd(a, m)
            if b % d:
                return float('-inf')
            if d == 1:
                return self.solution(a, b, m, k * a % m) + i + 1
            k *= a // d; k %= m
            b //= d
            m //= d

def solve():
    a, b, m = MI()
    bsgs = BSGS()
    print(bsgs.exBSGS(a, b, m, k = 1))

for _ in range(1):solve()


