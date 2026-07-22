'''
Hala Madrid!
https://www.zhihu.com/people/li-dong-hao-78-74
'''

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
def LGMI():
    return list(map(lambda x: int(x) - 1, input().split()))

#------------------------------FastIO---------------------------------

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
from time import *
from random import *
from math import log, gcd, sqrt, ceil

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

def solve(testcase):
    n = II()
    A = LII()

    if n == 1:
        print(1)
        return

    if A[0] < A[1]:
        flag = True
    else:
        flag = False
    
    B = []
    
    l, r = 0, 1
    while r < n:
        if flag:
            while r < n and A[r] > A[r - 1]:
                r += 1
        else:
            while r < n and A[r] < A[r - 1]:
                r += 1
        
        B.append((l, r - 1, flag))
            
        l = r - 1
        flag = not flag
    
    m = len(B)

    res = 0
    for i in range(m):
        l, r, f = B[i]
        LEN = r - l + 1
        res += LEN * (LEN + 1) // 2
    res -= m - 1


    for i in range(1, m):
        l1, r1, f1 = B[i - 1]
        l2, r2, f2 = B[i]
        LEN1 = r1 - l1 + 1
        LEN2 = r2 - l2 + 1

        if f1 and not f2:
            left_val = A[r1 - 1]
            cnt = 0
            for e in range(r1 + 1, r2 + 1):
                if A[e] > left_val:
                    cnt += 1
                else:
                    break
            res += (LEN1 - 1) * cnt

        if not f1 and f2:
            right_val = A[l2 + 1]
            cnt = 0
            for s in range(r1 - 1, l1 - 1, -1):
                if A[s] < right_val:
                    cnt += 1
                else:
                    break
            res += cnt * (LEN2 - 1)

    for i in range(2, m):
        l1, r1, f1 = B[i - 2]
        l2, r2, f2 = B[i - 1]
        l3, r3, f3 = B[i]
        LEN1 = r1 - l1 + 1
        LEN3 = r3 - l3 + 1

        if f1 and not f2 and f3:
            if A[r2] > A[r1 - 1] and A[l2] < A[l3 + 1]:
                res += (LEN1 - 1) * (LEN3 - 1)
    
    print(res)

for testcase in range(1):
    solve(testcase)