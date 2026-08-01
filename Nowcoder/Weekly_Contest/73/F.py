'''
Hala Madrid!
https://github.com/USYDDonghaoLi/Programming_Competition
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

def construct(x, y, k):
    if k < 0:
        return None
    
    if y == 0:
        return '0' * x if k == 0 else None
    
    if x == 0:
        return '1' * y if k == 0 else None
    
    if k > x * y:
        return None
    
    q = k // y
    r = k % y
    s = []
    zeros_placed = 0

    for i in range(y):
        target = q + (1 if i >= y - r else 0)

        while zeros_placed < target:
            s.append('0')
            zeros_placed += 1

        s.append('1')

    while zeros_placed < x:
        s.append('0')
        zeros_placed += 1
        
    return ''.join(s)

def solve(testcase):
    n, m = MI()
    A = []
    for _ in range(m):
        l, r, x, y, k = MI()
        A.append((l - 1, r - 1, x, y, k))

    if m == 0:
        print('0' * n)
        return

    A.sort(key=lambda t: (t[0], -t[1]))

    res = ['0' for _ in range(n)]

    cl, cr, cx, cy, ck = A[-1]
    s = construct(cx, cy, ck)
    if s is None:
        print(-1)
        return
    for i in range(cl, cr + 1):
        res[i] = s[i - cl]

    for idx in range(m - 2, -1, -1):
        l, r, x, y, k = A[idx]
        LEFT = cl - l
        RIGHT = r - cr
        a = x - cx          
        b = y - cy          
        if a < 0 or b < 0 or a + b != LEFT + RIGHT:
            print(-1)
            return
        ADDK = k - ck
        if ADDK < 0:
            print(-1)
            return

        found = False
        min_zl = max(0, a - RIGHT)
        max_zl = min(a, LEFT)
        for zl in range(min_zl, max_zl + 1):
            zr = a - zl
            yl = LEFT - zl
            yr = RIGHT - zr

            base = zl * cy + zl * yr + cx * yr
            maxadd = zl * yl + zr * yr

            if base <= ADDK <= base + maxadd:

                excess = ADDK - base
                kl = min(excess, zl * yl)
                kr = excess - kl
                left_s = construct(zl, yl, kl)
                right_s = construct(zr, yr, kr)

                if left_s is None or right_s is None:
                    continue

                for j in range(LEFT):
                    res[l + j] = left_s[j]
                for j in range(RIGHT):
                    res[cr + 1 + j] = right_s[j]

                found = True

                break

        if not found:
            print(-1)
            return

        cl, cr, cx, cy, ck = l, r, x, y, k

    print(''.join(res))

for testcase in range(1):
    solve(testcase)