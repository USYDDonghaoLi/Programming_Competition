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
    A = [0 for _ in range(n + 22)]
    B = [0 for _ in range(n + 22)]
    # C = [0 for _ in range(n + 22)]
    # D = [0 for _ in range(n + 22)]

    # for _ in range(n):
    #     a, b = MI()
    #     a += 11
    #     b += 11

    #     '''
    #     0 ~ a - 2, diff = -1
    #     '''
    #     A[a - 2] -= 1
    #     A[0] += 1
    #     C[0] += a - 1

    #     '''
    #     a + 2 ~ b - 2,
    #     left - mid diff = 1
    #     mid - right diff = -1
    #     '''
    #     if a + 2 <= b - 2:
    #         LEN = b - 2 - (a + 2) + 1
    #         if LEN & 1:
    #             mid = a + b >> 1
                
    #             B[a + 2] += 1
    #             B[mid + 1] -= 1

    #             A[b - 2] -= 1
    #             A[mid - 1] += 1
    #         else:
    #             mid = a + b >> 1

    #             B[a + 2] += 1
    #             B[mid + 1] -= 1

    #             A[b - 2] -= 1
    #             A[mid] += 1
    #     '''
    #     b + 2 ~ inf diff = 1
    #     '''

    #     B[b + 2] += 1
    #     B[n + 20] -= 1
    #     D[n + 21] += n + 20 - (b + 1)
    
    # for i in range(n + 20, -1, -1):
    #     A[i] += A[i + 1]
    # for i in range(1, n + 21):
    #     B[i] += B[i - 1]
    
    # print("A", A)
    # print("B", B)

    # for i in range(1, n + 21):
    #     C[i] = C[i - 1] + A[i] + B[i]
    # for i in range(n + 20, -1, -1):
    #     D[i] = D[i + 1] - B[i]
    
    # print("C", C)
    # print("D", D)

    for _ in range(n):
        a, b = MI()
        a += 11
        b += 11
        '''
        0 ~ a - 2, diff = -1
        '''
        A[1] -= 1
        A[a - 1] += 1
        B[0] += a - 2
        '''
        a + 2 ~ b - 2,
        left - mid diff = 1
        mid - right diff = -1
        ''' 
        if a + 2 <= b - 2:
            LEN = b - 2 - (a + 2) + 1
            if LEN & 1:
                mid = a + b >> 1
                
                A[a + 2] += 1
                A[mid + 1] -= 1
                print("A", A)

                A[mid + 1] -= 1
                A[b - 1] += 1
                print("A", A)

                print(a + 2, mid + 1, mid + 1, b - 1)
            else:
                mid = a + b >> 1

                A[a + 2] += 1
                A[mid + 1] -= 1

                A[mid + 2] -= 1
                A[b - 1] += 1
        
        '''
        b + 2 ~ inf diff = 1
        '''
        A[b + 2] += 1
        A[n + 20] -= 1

        print("A", A)
    
    for i in range(1, n + 21):
        A[i] += A[i - 1]

    
    print("AA", A)
    print(B[0])
    
    for i in range(1, n + 21):
        B[i] = B[i - 1] + A[i]
    
    print("B", B)
    
    res = []
    
    for _ in range(q):
        x = II()
        res.append(B[x + 11])
    
    print(*res)

for testcase in range(II()):
    solve(testcase)