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

# from types import GeneratorType
# def bootstrap(f, stack=[]):
#     def wrappedfunc(*args, **kwargs):
#         if stack:
#             return f(*args, **kwargs)
#         else:
#             to = f(*args, **kwargs)
#             while True:
#                 if type(to) is GeneratorType:
#                     stack.append(to)
#                     to = next(to)
#                 else:
#                     stack.pop()
#                     if not stack:
#                         break
#                     to = stack[-1].send(to)
#             return to
#     return wrappedfunc

# seed(19981220)
# RANDOM = getrandbits(64)
 
# class Wrapper(int):
#     def __init__(self, x):
#         int.__init__(x)

#     def __hash__(self):
#         return super(Wrapper, self).__hash__() ^ RANDOM

# def TIME(f):

#     def wrap(*args, **kwargs):
#         s = perf_counter()
#         ret = f(*args, **kwargs)
#         e = perf_counter()

#         print(e - s, 'sec')
#         return ret
    
#     return wrap

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

# @TIME
def solve(testcase):
    n, k = MI()
    A = []
    B = []
    C = []

    for _ in range(n):
        a, b, c = MI()
        A.append(a)
        B.append(b)
        C.append(c)

    dp = [[[False for _ in range(8)] for _ in range(k + 1)] for _ in range(1 << n)]
    prev = [[[None for _ in range(8)] for _ in range(k + 1)] for _ in range(1 << n)]
    
    dp[(1 << n) - 1][0][0] = True

    submask = defaultdict(list)
    for i in range(1 << n):
        for j in range(i + 1):
            if i | j == i:
                submask[i].append(j)

    @lru_cache(None)
    def check(st):
        AA, BB, CC = [], [], []
        for i in range(n):
            if st >> i & 1:
                AA.append(A[i])
                BB.append(B[i])
                CC.append(C[i])
        
        sa = sum(AA)
        if sa > 10:
            return None, None, False
        
        one = CC.count(1)
        if one and (len(AA) == one or not CC.count(2)):
            return None, None, False
        
        three = CC.count(3)
        if three > 1:
            return None, None, False
        
        if three and sa != 10:
            return None, None, False
        
        if one and three and one + three == len(AA):
            return None, None, False
        
        needstate = 0
        curstate = 0
        for i, c in enumerate(CC):
            if c == 2:
                needstate |= 1 << BB[i] - 1
            curstate |= 1 << BB[i] - 1
        
        return needstate, curstate, True

    for turn in range(k + 1):
        for state in range(1 << n):
            # print('submask', state, submask[state])
            for usestate in submask[state]:
                needstate, nxtstate, flag = check(usestate)
                if not flag:
                    continue
                else:
                    for curstate in range(8):
                        if dp[state][turn][curstate] and curstate | needstate == curstate:
                            if turn + 1 <= k:
                                # print('from', state, 'to', state ^ usestate, 'turn', turn, 'to', turn + 1, 'with state', nxtstate)
                                # print(state ^ usestate, nxtstate)
                                dp[state ^ usestate][turn + 1][nxtstate] = True
                                prev[state ^ usestate][turn + 1][nxtstate] = (state, turn, curstate)

    cs, ct, cc = 0, k, -1
    # print(dp[cs][ct])

    for c in range(8):
        if dp[cs][ct][c]:
            cc = c
            break

    if cc == -1:
        print(-1)
        return

    out = []
    
    while True:
        if prev[cs][ct][cc] is None:
            break
        pcs, pct, pcc = prev[cs][ct][cc]
        used = pcs ^ cs
        AA = []
        BB = []
        CC = []
        for i in range(n):
            if used >> i & 1:
                if C[i] == 1:
                    AA.append(i + 1)
                elif C[i] == 2:
                    BB.append(i + 1)
                else:
                    CC.append(i + 1)
        if AA:
            assert len(BB) > 0
        assert len(CC) <= 1
        res = BB + AA + CC
        out.append(' '.join(map(str, res)))
        cs, ct, cc = pcs, pct, pcc
    
    def check(out):
        prev = 0
        for res in out:
            for r in res:
                r = int(r) - 1
                if C[r - 1] == 2:
                    needstate = 1 << B[r] - 1

    print(len(out))
    assert len(out) == k
    print('\n'.join(reversed(out)))


for testcase in range(1):
    solve(testcase)