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

def manacher(string):
    new_string =['', '$']
    for s in string:
        new_string.append(s)
        new_string.append('$')
    n = len(new_string)

    D =[0 for _ in range(n)]
    l, r = 0, 0

    for i in range(n):
        if i > r:
            while i - D[i] >= 0 and i + D[i] <n and new_string[i - D[i]] == new_string[i + D[i]]:
                D[i] += 1
            l, r = i - D[i] + 1, i + D[i] - 1

        else:
            j = l + r - i
            if j - D[j] >= l:
                D[i] = D[j]
            else:
                D[i] = j - l + 1
                while i - D[i] >= 0 and i + D[i] < n and new_string[i - D[i]] == new_string[i + D[i]]:
                    D[i] += 1
                l, r = i - D[i] + 1, i + D[i] - 1
    
    # print(new_string)
    # print(D)
    
    '''
    if not i & 1:
        LEN = (v + 1 >> 1) * 2 - 1
    else:
        LEN = v >> 1 << 1    
    '''

    return D

# @TIME
def solve(testcase):
    s = I()
    D = manacher(s)

    res = inf
    for i, v in enumerate(D):
        if not i & 1:
            LEN = (v + 1 >> 1) * 2 - 1
        else:
            LEN = v >> 1 << 1
        if LEN > 1:
            if LEN & 1:
                res = fmin(res, 3)
            else:
                res = fmin(res, 2)

    print(-1 if res == inf else res)

for testcase in range(1):
    solve(testcase)