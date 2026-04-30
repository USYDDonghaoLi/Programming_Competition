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

class Hash:
    def __init__(self, arr) -> None:
        self.arr = arr
        self.n = len(arr)
        # === 双哈希参数 ===
        self.mul1 = 1331
        self.mod1 = 10**9 + 7
        self.mul2 = 131
        self.mod2 = 10**9 + 9
        
        self.mulpw1 = [1] * (self.n + 1)
        self.mulpw2 = [1] * (self.n + 1)
        for i in range(1, self.n + 1):
            self.mulpw1[i] = self.mulpw1[i - 1] * self.mul1 % self.mod1
            self.mulpw2[i] = self.mulpw2[i - 1] * self.mul2 % self.mod2

        self.HASH1 = [0]
        self.HASH2 = [0]
        for c in self.arr:
            self.HASH1.append((self.HASH1[-1] * self.mul1 + c) % self.mod1)
            self.HASH2.append((self.HASH2[-1] * self.mul2 + c) % self.mod2)

    # 返回 (h1, h2) 元组，[l, r)
    def GetHash(self, l, r):
        h1 = (self.HASH1[r] - self.HASH1[l] * self.mulpw1[r - l]) % self.mod1
        h2 = (self.HASH2[r] - self.HASH2[l] * self.mulpw2[r - l]) % self.mod2
        return (h1 + self.mod1) % self.mod1, (h2 + self.mod2) % self.mod2   # 确保非负


# 在 solve() 里替换原来哈希相关部分
def solve():
    n, m = MI()
    s = I()
    s = [ord(c) for c in s]
    H = Hash(s)          # 现在是双哈希

    mp = defaultdict(int)   # key 变成 tuple (h1,h2)
    B = []

    for _ in range(m):
        t = I()
        t = [ord(c) for c in t]
        hval1 = hval2 = 0
        C = [ (0, 0) ] 
        for c in t:
            hval1 = (hval1 * H.mul1 + c) % H.mod1
            hval2 = (hval2 * H.mul2 + c) % H.mod2
            mp[(hval1, hval2)] += 1
            C.append( (hval1, hval2) )
        B.append(C)

    vis = set()
    for C in B:
        k = len(C)
        for i in range(1, k):
            pc = C[i - 1]
            c = C[i]
            if c in vis:
                continue
            vis.add(c)
            mp[c] = mp[c] + mp[pc]

    res = 0
    for i in range(n):
        l, r = i, n
        while l < r:
            mid = (l + r) >> 1
            h = H.GetHash(i, mid + 1)
            if h in mp:
                l = mid + 1
            else:
                r = mid
        h = H.GetHash(i, l)
        res = fmax(res, mp[h])

    print(res)

for _ in range(II()):
    solve()