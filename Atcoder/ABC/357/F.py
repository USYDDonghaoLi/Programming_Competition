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

mod = 998244353

# @TIME
def solve(testcase):
    n, q = MI()
    A = LII()
    B = LII()
    
    sz = ceil(sqrt(n))
    blockA = [[] for _ in range(sz + 10)]
    blockinfoA= [0 for _ in range(sz + 10)]
    flagA = [0 for _ in range(sz + 10)]
    szA = [0 for _ in range(sz + 10)]
    
    for i, v in enumerate(A):
        where, idx = divmod(i, sz)
        blockA[where].append(v)
        blockinfoA[where] += v
        blockinfoA[where] %= mod
        szA[where] += 1
        
    blockB = [[] for _ in range(sz + 10)]
    blockinfoB= [0 for _ in range(sz + 10)]
    flagB = [0 for _ in range(sz + 10)]
    szB = [0 for _ in range(sz + 10)]
    
    for i, v in enumerate(A):
        where, idx = divmod(i, sz)
        blockB[where].append(v)
        blockinfoB[where] += v
        blockinfoB[where] %= mod
        szB[where] += 1

    print(blockA, 'A')
    print(blockB, 'B')
    
    def updateA(l, r, x):
        lwhere, lidx = divmod(l, sz)
        rwhere, ridx = divmod(r, sz)
        
        if lwhere == rwhere:
            for j in range(lidx, ridx + 1):
                blockA[lwhere][j] += x
                blockA[lwhere][j] %= mod
            blockinfoA[lwhere] += x * (ridx - lidx + 1) % mod
            blockinfoA[lwhere] %= mod
        else:
            for j in range(lidx, szA[lwhere]):
                blockA[lwhere][j] += x
                blockA[lwhere][j] %= mod
                blockinfoA[lwhere] += x
                blockinfoA[lwhere] %= mod
            lwhere += 1
            for j in range(ridx + 1):
                blockA[rwhere][j] += x
                blockA[rwhere][j] %= mod
                blockinfoA[rwhere] += x
                blockinfoA[rwhere] %= mod
            rwhere -= 1
            
            for i in range(lwhere, rwhere + 1):
                flagA[i] += x
                flagA[i] %= mod
    
    def updateB(l, r, x):
        lwhere, lidx = divmod(l, sz)
        rwhere, ridx = divmod(r, sz)
        
        if lwhere == rwhere:
            for j in range(lidx, ridx + 1):
                blockB[lwhere][j] += x
                blockB[lwhere][j] %= mod
            blockinfoB[lwhere] += x * (ridx - lidx + 1) % mod
            blockinfoB[lwhere] %= mod
        else:
            for j in range(lidx, szB[lwhere]):
                blockB[lwhere][j] += x
                blockB[lwhere][j] %= mod
                blockinfoB[lwhere] += x
                blockinfoB[lwhere] %= mod
            lwhere += 1
            for j in range(ridx + 1):
                blockB[rwhere][j] += x
                blockB[rwhere][j] %= mod
                blockinfoB[rwhere] += x
                blockinfoB[rwhere] %= mod
            rwhere -= 1
            
            for i in range(lwhere, rwhere + 1):
                flagB[i] += x
                flagB[i] %= mod
    
    def getSumA(l, r):
        lwhere, lidx = divmod(l, sz)
        rwhere, ridx = divmod(r, sz)
        
        res = 0
        
        if lwhere == rwhere:
            for j in range(lidx, ridx + 1):
                res += (blockA[lwhere][j] + flagA[lwhere])
                res %= mod
            return res
        else:
            for j in range(lidx, szA[lwhere]):
                res += (blockA[lwhere][j] + flagA[lwhere])
                res %= mod
            lwhere += 1
            for j in range(ridx + 1):
                res += (blockB[rwhere][j] + flagA[rwhere])
                res %= mod
            rwhere -= 1
            
            for i in range(lwhere, rwhere + 1):
                res += blockinfoA[i] + flagA[i] * szA[i]
                res %= mod
            
            return res
    
    def getSumB(l, r):
        lwhere, lidx = divmod(l, sz)
        rwhere, ridx = divmod(r, sz)
        
        res = 0
        
        if lwhere == rwhere:
            for j in range(lidx, ridx + 1):
                res += (blockB[lwhere][j] + flagB[lwhere])
                res %= mod
            return res
        else:
            for j in range(lidx, szB[lwhere]):
                res += (blockB[lwhere][j] + flagB[lwhere])
                res %= mod
            lwhere += 1
            for j in range(ridx + 1):
                res += (blockB[rwhere][j] + flagB[rwhere])
                res %= mod
            rwhere -= 1
            
            for i in range(lwhere, rwhere + 1):
                res += blockinfoB[i] + flagB[i] * szB[i]
                res %= mod
            
            return res
    
    for _ in range(q):
        ops = LII()
        if ops[0] == 1:
            l, r, x = ops[1:]
            l -= 1
            r -= 1
            updateA(l, r, x)
        elif ops[0] == 2:
            l, r, x = ops[1:]
            l -= 1
            r -= 1
            updateB(l, r, x)
        else:
            l, r = ops[1:]
            l -= 1
            r -= 1
            sa, sb = getSumA(l, r), getSumB(l, r)
            print(sa * sb % mod)

for testcase in range(1):
    solve(testcase)