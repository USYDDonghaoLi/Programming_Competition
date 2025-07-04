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
    n, m = MI()
    v = [False for _ in range(100001)]
    va = [False for _ in range(100001)]
    vb = [False for _ in range(100001)]
    for _ in range(n):
        a, b = MI()
        print('ab', a, b)
        v[a] = v[b] = True
        va[a] = True
        vb[b] = True
    print(va[3], vb[3])

    res = [0 for _ in range(100001)]
    l, r = 0, 0
    while r < 100001:
        while r < 100001 and not v[r]:
            r += 1
            l = r
        while r < 100001 and v[r]:
            r += 1
        for i in range(1, r - l + 1):
            res[i] += r - l + 1 - i
        print('lr', l, r)

        if l == r:
            continue
        ll, rr = l, l
        flag = 0
        while rr < r:
            print(va[3], vb[3])
            while rr < r and va[rr] and vb[rr]:
                rr += 1
                ll = rr
            print('llrr1', ll, rr)
            if flag:
                while rr < r and va[rr] and not vb[rr]:
                    rr += 1
                if rr != ll:
                    for i in range(1, rr - ll + 1):
                        res[i] -= rr - ll + 1 - i
                flag ^= 1
                print('llrr2', ll, rr)
                ll = rr

            else:
                while rr < r and vb[rr] and not va[rr]:
                    rr += 1
                if rr != ll:
                    for i in range(1, rr - ll + 1):
                        res[i] -= rr - ll + 1 - i
                flag ^= 1
                ll = rr
                print('llrr3', ll, rr)
            print('llrr', ll, rr)
        l = r
    print(*res[1: m + 1])

for _ in range(1):solve()