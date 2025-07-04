from re import M
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

mod = 998244353

def solve():
    n, m = MI()
    q = II()
    for _ in range(q):
        a, b, c, d = MI()
        odr, evr, odc, evc = [], [], [],[]
        if a & 1:
            if b & 1:
                odr = [a, b]
                evr = [a + 1, b - 1]
            else:
                odr = [a, b - 1]
                evr = [a + 1, b]
        else:
            if b & 1:
                odr = [a + 1, b]
                evr = [a, b - 1]
            else:
                odr = [a + 1, b - 1]
                evr = [a, b]
        
        if c & 1:
            if d & 1:
                odc = [c, d]
                evc = [c + 1, d - 1]
            else:
                odc = [c, d - 1]
                evc = [c + 1, d]
        else:
            if d & 1:
                odc = [c + 1, d]
                evc = [c, d - 1]
            else:
                odc = [c + 1, d - 1]
                evc = [c, d]
        
        #print(odr, odc, evr, evc)
        
        res = 0
        if odr[0] > odr[1] or odc[0] > odc[1]:
            pass
        else:
            k1 = (odc[0] + odc[1]) * ((odc[1] - odc[0]) // 2 + 1) // 2
            k1 %= mod
            #print('k1', k1)
            res += ((odr[1] - odr[0]) // 2 + 1) * k1 % mod
            res %= mod
            #print('res', res)
            k2 = (odr[0] + odr[1] - 2) * ((odr[1] - odr[0]) // 2 + 1) // 2
            #print('k2', k2)
            k2 %= mod
            k2 *= m
            k2 %= mod
            res += k2 * ((odc[1] - odc[0]) // 2 + 1) % mod
            res %= mod
            #print('res', res)
        
        if evr[0] > evr[1] or evc[0] > evc[1]:
            pass
        else:
            k1 = (evc[0] + evc[1]) * ((evc[1] - evc[0]) // 2 + 1) // 2
            k1 %= mod
            #print('k1', k1)
            res += ((evr[1] - evr[0]) // 2 + 1) * k1 % mod
            #print('res', res)
            k2 = (evr[0] + evr[1] - 2) * ((evr[1] - evr[0]) // 2 + 1) // 2
            #print('k2', k2)
            k2 %= mod
            k2 *= m
            k2 %= mod
            res += k2 * ((evc[1] - evc[0]) // 2 + 1) % mod
            res %= mod
            #print('res', res)

        print(res)
for _ in range(1):solve()

