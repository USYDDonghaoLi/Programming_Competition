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
    n, q = MI()
    s = I()
    s = [ord(c) - 97 for c in s]

    A = [[0 for _ in range(n + 1)] for _ in range(26)]
    B = [[0 for _ in range(n + 1)] for _ in range(26)]
    C = [[0 for _ in range(n + 1)] for _ in range(26)]

    for i, c in enumerate(s, 1):
        for j in range(26):
            if c == j:
                A[j][i] = A[j][i - 1] + 1
                B[j][i] = B[j][i - 1] + A[j][i] * i
                C[j][i] = C[j][i - 1] + i
            else:
                A[j][i] = A[j][i - 1]
                B[j][i] = B[j][i - 1]
                C[j][i] = C[j][i - 1]
    
    D = [[0 for _ in range(n + 1)] for _ in range(26)]
    E = [[0 for _ in range(n + 1)] for _ in range(26)]
    F = [[0 for _ in range(n + 1)] for _ in range(26)]

    for i in range(n - 1, -1, -1):
        c = s[i]
        for j in range(26):
            if c == j:
                D[j][i] = D[j][i + 1] + 1
                E[j][i] = E[j][i + 1] + D[j][i] * (i + 1)
                F[j][i] = F[j][i + 1] + (i + 1)
            else:
                D[j][i] = D[j][i + 1]
                E[j][i] = E[j][i + 1]
                F[j][i] = F[j][i + 1]

    # A = [[0 for _ in range(26)] for _ in range(n + 1)]
    # B = [[0 for _ in range(26)] for _ in range(n + 1)]
    # C = [[0 for _ in range(26)] for _ in range(n + 1)]

    # for i, c in enumerate(s, 1):
    #     for j in range(26):
    #         if c == j:
    #             A[i][j] = A[i - 1][j] + 1
    #             B[i][j] = B[i - 1][j] + A[i][j] * i
    #             C[i][j] = C[i - 1][j] + i
    #         else:
    #             A[i][j] = A[i - 1][j]
    #             B[i][j] = B[i - 1][j]
    #             C[i][j] = C[i - 1][j]
    
    # D = [[0 for _ in range(26)] for _ in range(n + 1)]
    # E = [[0 for _ in range(26)] for _ in range(n + 1)]
    # F = [[0 for _ in range(26)] for _ in range(n + 1)]

    # for i in range(n - 1, -1, -1):
    #     c = s[i]
    #     for j in range(26):
    #         if c == j:
    #             D[i][j] = D[i + 1][j] + 1
    #             E[i][j] = E[i + 1][j] + D[i][j] * (i + 1)
    #             F[i][j] = F[i + 1][j] + (i + 1)
    #         else:
    #             D[i][j] = D[i + 1][j]
    #             E[i][j] = E[i + 1][j]
    #             F[i][j] = F[i + 1][j]
    
    # print("\nA", A)
    # print("\nB", B)
    # print("\nC", C)

    # print("\nD", D)
    # print("\nE", E)
    # print("\nF", F)

    for _ in range(q):
        l, r, x = MI()
        l -= 1
        r -= 1
        LEN = r - l + 1
        if LEN < x:
            print(0)
            continue

        if x == 1:
            print(r - l + 1)
        elif x == 2:
            
            res = 0
            for j in range(26):
                cnt = A[j][r + 1] - A[j][l]
                res += cnt * (cnt - 1) // 2
            print(res)
        else:
            assert x == 3
            res = 0
            for j in range(26):
                a = B[j][r + 1] - B[j][l]
                cnta = A[j][l]
                sa = C[j][r + 1] - C[j][l]
                # print('jacs', j, a, cnta, sa, a - cnta * sa)
                a -= cnta * sa


                # rr, ll = n - 1 - l, n - 1 - r
                # b = E[ll][j] - E[rr + 1][j]
                # cntb = D[rr + 1][j]
                # sb = F[ll][j] - F[rr + 1][j]
                # print('jbcs', j, b, cntb, sb, b - cntb * sb)
                # b -= cntb * sb

                # rr, ll = n - 1 - l, n - 1 - r
                b = E[j][l] - E[j][r + 1]
                cntb = D[j][r + 1]
                sb = F[j][l] - F[j][r + 1]
                # print('jbcs', j, b, cntb, sb, b - cntb * sb)
                b -= cntb * sb

                cnt = A[j][r + 1] - A[j][l]
                res += a - b - cnt * (cnt - 1) // 2
            print(res)

    # for _ in range(q):
    #     l, r, x = MI()
    #     l -= 1
    #     r -= 1
    #     LEN = r - l + 1
    #     if LEN < x:
    #         print(0)
    #         continue

    #     if x == 1:
    #         print(r - l + 1)
    #     elif x == 2:
            
    #         res = 0
    #         for j in range(26):
    #             cnt = A[r + 1][j] - A[l][j]
    #             res += cnt * (cnt - 1) // 2
    #         print(res)
    #     else:
    #         assert x == 3
    #         res = 0
    #         for j in range(26):
    #             a = B[r + 1][j] - B[l][j]
    #             cnta = A[l][j]
    #             sa = C[r + 1][j] - C[l][j]
    #             # print('jacs', j, a, cnta, sa, a - cnta * sa)
    #             a -= cnta * sa


    #             # rr, ll = n - 1 - l, n - 1 - r
    #             # b = E[ll][j] - E[rr + 1][j]
    #             # cntb = D[rr + 1][j]
    #             # sb = F[ll][j] - F[rr + 1][j]
    #             # print('jbcs', j, b, cntb, sb, b - cntb * sb)
    #             # b -= cntb * sb

    #             # rr, ll = n - 1 - l, n - 1 - r
    #             b = E[l][j] - E[r + 1][j]
    #             cntb = D[r + 1][j]
    #             sb = F[l][j] - F[r + 1][j]
    #             # print('jbcs', j, b, cntb, sb, b - cntb * sb)
    #             b -= cntb * sb

    #             cnt = A[r + 1][j] - A[l][j]
    #             res += a - b - cnt * (cnt - 1) // 2
    #         print(res)

for testcase in range(1):
    solve(testcase)