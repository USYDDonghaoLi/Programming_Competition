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

'''
0b10100001110110010101
0b11101100001101010001
0b11010101111111000010
0b11001101000110110101
0b11111100111001000001
0b10011111000100011101
0b10000100100111000111
0b10111110101110100011
'''

# @TIME
def solve(testcase):
    # nums = LII()
    # for num in nums:
    #     print(bin(num))
    
    n, k = MI()
    res = [1 << k - 1 for i in range(n)]
    need = [0 for _ in range(n)]
    
    def calc(l, r, bit):
        if bit == -1:
            return
        if l == r:
            return
        elif l + 1 == r:
            need[r] |= 1 << bit
        else:
            mid = l + r >> 1
            for i in range(mid + 1, r + 1):
                need[i] |= 1 << bit
            calc(l, mid, bit - 1)
            calc(mid + 1, r, bit - 1)
        
        # print(l, r, bit, need)

    calc(0, n - 1, k - 2)

    for i in range(n):
        res[i] |= need[i]
    
    print(*res)

    # S = set()
    # nums = [662933,967505,876482,840117,1035841,651549,543175,781219]
    # for num in nums:
    #     while num:
    #         S.add(num)
    #         num >>= 1
    
    # print(len(S))

    # S = set()
    # for r in res:
    #     while r:
    #         S.add(r)
    #         r >>= 1
    # print(len(S))
    # n, k = MI()
    # if n >= (1 << k) - 1:
    #     res = [1 for _ in range(n)]
    #     for i in range((1 << k) - 1):
    #         res[i] = i + 1
    #     print(*res)
    # else:
    #     nums = []

for testcase in range(II()):
    solve(testcase)