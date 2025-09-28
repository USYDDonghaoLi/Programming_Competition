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
    n, m, q = MI()
    A = [0] + LII()
    N = n + m + 1

    sn = 0
    ss = A[1]

    for i in range(1, n + 2):
        sn += A[i]
    for i in range(n + 2, N + 1):
        ss += A[i]
    
    flag = sn < 0 or ss < 0

    for i in range(1, n + 1):
        if A[i] + A[i + 1] < 0:
            flag = True
            break
    if A[n + 1] + A[1] < 0:
        flag = True
    
    if A[1] + A[n + 2] < 0:
        flag = True

    for i in range(n + 2, N):
        if A[i] + A[i + 1] < 0:
            flag = True
            break
    
    if A[N] + A[1] < 0:
        flag = True
    
    if flag:
        for _ in range(q):
            s, t = MI()
            print(0)
        return
    
    nl = n + 1
    B = [0 for _ in range(nl + 1)]

    for i in range(1, nl + 1):
        B[i] = B[i - 1] + A[i]
    
    C = [0 for _ in range(nl + 1)]
    C[1] = A[1]
    for i in range(1, nl):
        C[i + 1] = C[i] + A[n + 2 - i]
    
    sl = m + 1
    D = [0 for _ in range(sl + 1)]
    D[1] = A[1]
    for i in range(1, sl):
        D[i + 1] = D[i] + A[n + 1 + i]

    E = [0 for _ in range(sl + 1)]
    E[1] = A[1]
    for i in range(1, sl):
        E[i + 1] = E[i] + A[n + m + 2 - i]
    
    def f(idx, flag):
        if idx == 1:
            return 0
        else:
            if flag:
                return idx - 1
            else:
                return idx - (n + 1)

    def g(idx, flag):
        if idx == 1:
            return 0
        else:
            if flag:
                return n + 2 - idx
            else:
                return n + m + 2 - idx
    
    def calc2(u, v, LEN, pref):
        if u == v:
            return 0
        d = (v - u + LEN) % LEN
        if d == 0:
            return 0
        start_idx = (u + 1) % LEN
        end_idx = v
        if start_idx == 0:
            start_idx = LEN
        if end_idx == 0:
            end_idx = LEN
        if start_idx <= end_idx:
            res = pref[end_idx] - pref[start_idx - 1]
        else:
            res = pref[LEN] - pref[start_idx - 1] + pref[end_idx]
        return res

    def calc(u, v, flag):
        if u == v:
            return 0
        
        LEN = nl if flag else sl
        choice1 = B if flag else D
        choice2 = C if flag else E
        
        tu = f(u, flag)
        tv = f(v, flag)
        c1 = calc2(tu, tv, LEN, choice1)
        
        ttu = g(u, flag)
        ttv = g(v, flag)
        c2 = calc2(ttu, ttv, LEN, choice2)
        
        return fmin(c1, c2)

    for _ in range(q):
        s, t = MI()

        if s == t:
            print(fmax(0, A[s]))
            continue

        sn = (s == 1 or (2 <= s <= n + 1))
        ss = (s == 1 or (n + 2 <= s <= N))
        tn = (t == 1 or (2 <= t <= n + 1))
        ts = (t == 1 or (n + 2 <= t <= N))
        
        if sn and tn:
            res = calc(s, t, True)
        elif ss and ts:
            res = calc(s, t, False)
        else:
            s_loop_north = sn and not ss
            t_loop_north = tn and not ts
            res = calc(s, 1, s_loop_north) + calc(1, t, t_loop_north)
        
        print(fmax(0, res + A[t]))

for testcase in range(1):
    solve(testcase)