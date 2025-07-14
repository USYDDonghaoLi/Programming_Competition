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

def compare(A, B):
    flag = True
    for i in range(9, -1, -1):
        if A[i] > B[i]:
            break
        if A[i] < B[i]:
            flag = False
            break
    
    if not flag:
        for i in range(10):
            A[i] = B[i]
    
    return A

# @TIME
def solve(testcase):
    n, k = MI()
    A = LII()
    A.sort(reverse = True)

    B = [[], [], []]
    C = [[], [], []]

    cur = [0 for _ in range(10)]

    t = 0
    for i in range(k - 1, -1, -1):
        cur[A[i]] += 1
        t = (t + A[i]) % 3
        u =  A[i] % 3
        if len(B[u]) < 2:
            B[u].append(A[i])
    
    for i in range(k, n):
        u =  A[i] % 3
        if len(C[u]) < 2:
            C[u].append(A[i])
    
    res = [-1 for _ in range(10)]

    B = B[0] + B[1] + B[2]
    C = C[0] + C[1] + C[2]

    
    for k1 in range(3):
        for k2 in range(fmin(3, k1 + 1)):
            # print('cur', cur)

            for c1 in combinations(B, k1):
                for cc1 in c1:
                    # print('cc1', cc1, cur)
                    cur[cc1] -= 1
                    # print('cc1', cc1, cur)
                    t = (t - cc1) % 3

                for c2 in combinations(C, k2):
                    for cc2 in c2:
                        cur[cc2] += 1
                        t = (t + cc2) % 3
                    
                    if t == 0:
                        # print('c1c2', c1, c2, cur)
                        res = compare(res, cur)

                    for cc2 in c2:
                        cur[cc2] -= 1
                        t = (t - cc2) % 3
                    pass

                for cc1 in c1:
                    # print('cc1', cc1, cur)
                    cur[cc1] += 1
                    # print('cc1', cc1, cur)
                    t = (t + cc1) % 3
    
    # print('res', res)

    if res == [-1 for _ in range(10)]:
        print(-1)
    else:
        check = 0
        D = []
        for i in range(10):
            D.extend([str(i)] * res[i])
            check += i * res[i]
        
        assert check % 3 == 0
        
        if not D:
            print(-1)
        else:
            D = ''.join(D)
            D = D[::-1]
            D = D.lstrip('0')

            if not D:
                print('0')
            else:
                print(D)


for testcase in range(II()):
    solve(testcase)