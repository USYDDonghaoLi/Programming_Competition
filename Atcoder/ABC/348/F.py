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

# '''
# 手写栈防止recursion limit
# 注意要用yield 不要用return
# 函数结尾要写yield None
# '''
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

# RANDOM = getrandbits(32)
 
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

def popcount(n: int) -> int:
    n -= ((n >> 1) & 0x5555555555555555)
    n = (n & 0x3333333333333333) + ((n >> 2) & 0x3333333333333333)
    n = (n + (n >> 4)) & 0x0f0f0f0f0f0f0f0f
    n += ((n >> 8) & 0x00ff00ff00ff00ff)
    n += ((n >> 16) & 0x0000ffff0000ffff)
    n += ((n >> 32) & 0x00000000ffffffff)
    return n & 0x7f

class Bitset:
    def __init__(self, n: int) -> None:
        self.n = n
        self.m = (n + 62) // 63
        self.A = [0] * self.m
 
    def __len__(self) -> int:
        return self.n
 
    @property
    def size(self) -> int:
        return self.n
 
    def __str__(self) -> str:
        S = []
        for a in self.A:
            S.append(bin(a)[2:].zfill(63)[::-1])
        S = "".join(S)
        return S[:self.n][::-1]
 
    def __getitem__(self, ind: int) -> int:
        i = ind // 63
        j = ind - i * 63
        return self.A[i] >> j & 1
 
    def __setitem__(self, ind: int, k: int) -> None:
        i = ind // 63
        j = ind - i * 63
        if (self.A[i] >> j & 1) != k:
            self.A[i] ^= 1 << j     
        else:
            pass
 
    def rev(self, ind: int) -> None:
        i = ind // 63
        j = ind - i * 63
        self.A[i] ^= 1 << j
 
    def count(self) -> int:
        ret = 0
        for a in self.A:
            ret += popcount(a)
        return ret
 
    def __sum__(self) -> int:
        return self.count()
 
    def resize(self, n: int) -> None:
        m = (n + 62) // 63
        if m > self.m:
            self.A += [0] * (m - self.m)
        else:
            self.A = self.A[:m]
            j = n % 63
            if j != 0:
                self.A[-1] &= (1 << j) - 1
            else:
                pass
        self.n = n
        self.m = m
 
    def __and__(self, other: 'Bitset') -> 'Bitset':
        if self.n < other.n:
            n = self.n
        else:
            n = other.n
 
        ret = Bitset(n)
        for i, (a, b) in enumerate(zip(self.A, other.A)):
            ret.A[i] = a & b
 
        return ret
 
    def __iand__(self, other: 'Bitset') -> 'Bitset':
        if self.m < other.m:
            m = self.m
        else:
            m = other.m
        for i in range(m):
            self.A[i] &= other.A[i]
        for i in range(m, self.m):
            self.A[i] = 0
        return self
 
    def __or__(self, other: 'Bitset') -> 'Bitset':
        if self.n > other.n:
            n = self.n
        else:
            n = other.n
 
        ret = Bitset(n)
        for i in range(ret.m):
            if i < self.m and i < other.m:
                ret.A[i] = self.A[i] | other.A[i]
            elif i < self.m:
                ret.A[i] = self.A[i]
            else:
                ret.A[i] = other.A[i]
 
        return ret
 
    def __ior__(self, other: 'Bitset') -> 'Bitset':
        if self.m < other.m:
            m = self.m
        else:
            m = other.m
        for i in range(m):
            self.A[i] |= other.A[i]
        if self.n < other.n:
            x = self.n % 63
            if x != 0:
                mask = (1 << x) - 1
                self.A[-1] &= mask
        else:
            pass
        return self
 
    def __xor__(self, other: 'Bitset') -> 'Bitset':
        if self.n > other.n:
            n = self.n
        else:
            n = other.n
 
        ret = Bitset(n)
        for i in range(ret.m):
            if i < self.m and i < other.m:
                ret.A[i] = self.A[i] ^ other.A[i]
            elif i < self.m:
                ret.A[i] = self.A[i]
            else:
                ret.A[i] = other.A[i]
 
        return ret
 
    def __ixor__(self, other: 'Bitset') -> 'Bitset':
        if self.m < other.m:
            m = self.m
        else:
            m = other.m
        for i in range(m):
            self.A[i] ^= other.A[i]
        if self.n < other.n:
            x = self.n % 63
            if x != 0:
                mask = (1 << x) - 1
                self.A[-1] &= mask
        else:
            pass
        return self
 
    def and_count(self, other: 'Bitset') -> int:
        ret = 0
        for a, b in zip(self.A, other.A):
            ret += popcount(a & b)
        return ret
 
    def or_count(self, other: 'Bitset') -> int:
        ret = 0
        if self.m < other.m:
            m = self.m
        else:
            m = other.m
        for a, b in zip(self.A[:m], other.A[:m]):
            ret += popcount(a | b)
 
        for a in self.A[m:]:
            ret += popcount(a)
 
        for a in other.A[m:]:
            ret += popcount(a)
 
        return ret
 
    def xor_count(self, other: 'Bitset') -> int:
        ret = 0
        if self.m < other.m:
            m = self.m
        else:
            m = other.m
        for a, b in zip(self.A[:m], other.A[:m]):
            ret += popcount(a ^ b)
 
        for a in self.A[m:]:
            ret += popcount(a)
 
        for a in other.A[m:]:
            ret += popcount(a)
 
        return ret
 
    def __rshift__(self, k: int) -> 'Bitset':
        ret = Bitset(self.n)
        x = k // 63
        for i in range(x, self.m):
            ret.A[i - x] = self.A[i]
        k -= x * 63
        if k != 0:
            mask = (1 << k) - 1
            rk = 63 - k
            for i, a in enumerate(ret.A):
                if i != 0:
                    ret.A[i - 1] |= (a & mask) << (rk)
                ret.A[i] = a >> k
        else:
            pass
        return ret
 
    def __irshift__(self, k: int) -> 'Bitset':
        x = k // 63
        for i in range(x, self.m):
            self.A[i - x] = self.A[i]
        for i in range(self.m - x, self.m):
            self.A[i] = 0
        k -= x * 63
        if k != 0:
            mask = (1 << k) - 1
            rk = 63 - k
            for i, a in enumerate(self.A):
                if i != 0:
                    self.A[i - 1] |= (a & mask) << (rk)
                self.A[i] = a >> k
        else:
            pass
        return self
 
    def __lshift__(self, k: int) -> 'Bitset':
        ret = Bitset(self.n)
        x = k // 63
        for i in range(x, self.m):
            ret.A[i] = self.A[i - x]
        k -= x * 63
        if k != 0:
            rk = 63 - k
            mask = (1 << rk) - 1
            for i in range(self.m - 1, -1, -1):
                ret.A[i] &= mask
                ret.A[i] <<= k
                if i != 0:
                    ret.A[i] |= ret.A[i - 1] >> rk
        else:
            pass
        return ret
 
    def __ilshift__(self, k: int) -> 'Bitset':
        x = k // 63
        for i in range(self.m - 1, x - 1, -1):
            self.A[i] = self.A[i - x]
        for i in range(x - 1, -1, -1):
            self.A[i] = 0
        k -= x * 63
        if k != 0:
            rk = 63 - k
            mask = (1 << rk) - 1
            for i in range(self.m - 1, -1, -1):
                self.A[i] &= mask
                self.A[i] <<= k
                if i != 0:
                    self.A[i] |= self.A[i - 1] >> rk
        else:
            pass
        return self

# @TIME
def solve(testcase):
    n, m = MI()
    A = [LII() for _ in range(n)]
    
    bt = [Bitset(2010) for _ in range(n)]
    bs = [Bitset(2010) for _ in range(1000)]
    
    for i in range(m):
        for j in range(n):
            bs[A[j][i]] = j
        for j in range(n):
            bt[j] ^= bs[A[j][i]]
        for j in range(n):
            bs[A[j][i]] = j
    
    res = 0
    for i in range(n):
        res += count(bt[i])
    
    if m & 1:
        res -= n
    
    print(res // 2)

for testcase in range(1):
    solve(testcase)