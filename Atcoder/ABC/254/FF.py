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
from math import ceil, log, gcd
sys.setrecursionlimit(2 ** 31 - 1)

class SparseTable:

    __slots__ = {'arr', 'n', 'm', 'func', 'st'}

    def __init__(self, arr, func, ide_ele) -> None:
        try:
            self.arr = arr
            self.n = len(arr)
            self.m = ceil(log(self.n, 2))
            self.func = func
            self.st = [[ide_ele for _ in range(self.n)] for _ in range(self.m + 1)]

            for i in range(self.m + 1):
                if not i:
                    for j in range(self.n):
                        self.st[i][j] = self.arr[j]
                else:
                    for j in range(self.n):
                        try:
                            self.st[i][j] = self.func(self.st[i - 1][j], self.st[i - 1][j + (1 << i - 1)])
                        except:
                            self.st[i][j] = self.st[i - 1][j]
            #print('st', self.st)
        except:
            self.st = [0]

    def query(self, left, right):
        if left == right:
            return self.st[0][left]
        lg = int(log(right - left, 2))
        return self.func(self.st[lg][left], self.st[lg][right - (1 << lg) + 1])    


def solve():
    n, q = MI()
    A = LII()
    B = LII()

    diffA = [abs(A[i] - A[i - 1]) for i in range(1, n)]
    diffB = [abs(B[i] - B[i - 1]) for i in range(1, n)]

    sta = SparseTable(diffA, gcd, 0)
    stb = SparseTable(diffB, gcd, 0)

    for _ in range(q):
        h1, h2, w1, w2 = GMI()
        temp = A[h1] + B[w1]
        #print('temp', temp)
        if h1 != h2:
            if w1 != w2:
                a = sta.query(h1, h2 - 1)
                b = stb.query(w1, w2 - 1)
                #print('ab', a, b)
                print(gcd(temp, gcd(a, b)))
            else:
                a = sta.query(h1, h2 - 1)
                print(gcd(temp, a))
        else:
            if w1 != w2:
                b = stb.query(w1, w2 - 1)
                print(gcd(temp, b))
            else:
                print(temp)
solve()