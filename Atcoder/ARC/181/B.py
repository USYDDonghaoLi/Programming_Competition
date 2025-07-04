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

class UnionFind:
    def __init__(self, n: int):
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.setCount = n
    
    def Find(self, a: int) -> int:
        a = self.parent[a]
        acopy = a
        while a != self.parent[a]:
            a = self.parent[a]
        while acopy != a:
            self.parent[acopy], acopy = a, self.parent[acopy]
        return a
    
    def Union(self, x: int, y: int) -> bool:
        root_x = self.Find(x)
        root_y = self.Find(y)
        if root_x == root_y:
            return False
        if self.size[root_x] > self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_x] = root_y
        self.size[root_y] += self.size[root_x]
        self.setCount -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.Find(x) == self.Find(y)

    def members(self, x):
        root = self.Find(x)
        return [i for i in range(self.n) if self.Find(i) == root]
    
    def roots(self):
        return [i for i, x in enumerate(self.parent) if i == x]
    
    def group_count(self):
        return len(self.roots())
    
    def all_group_members(self):
        mp = defaultdict(list)
        for member in range(self.n):
            mp[self.Find(member)].append(member)
        return mp

class Hash:
    def __init__(self, arr) -> None:
        if arr[0].isalpha():
            self.arr = [ord(c) for c in arr]
        else:
            self.arr = arr
        self.mul = 19981220
        self.mod = 10 ** 9 + 7
        self.n = len(arr)
        self.mulpw = [1 for _ in range(self.n + 1)]
        for i in range(1, self.n + 1):
            self.mulpw[i] = self.mulpw[i - 1] * self.mul % self.mod

        self.HASH = [0]
        for c in self.arr:
            self.HASH.append((self.HASH[-1] * self.mul + c) % self.mod)

    #[l, r)
    def GetHash(self, l, r):
        return (self.HASH[r] - self.HASH[l] * self.mulpw[r - l]) % self.mod

    #[l, r]
    def CheckEqual(self, start, end, sz):
        pattern = self.GetHash(0, sz)
        for i in range(start, end - sz + 2, sz):
            if self.GetHash(i, i + sz) != pattern:
                return False
        return True
    
    #[l, r)
    def Check(self, ls, le, rs, re):
        return self.GetHash(ls, le) == self.GetHash(rs, re)
    
    @staticmethod
    def calc(arr):
        if arr[0].isalpha():
            arr = [ord(c) for c in arr]
        else:
            pass
        mul = 131
        mod = 10 ** 9 + 7
        n = len(arr)
        res = 0
        
        for c in arr:
            res = (res * mul + c) % mod
        
        return res

# @TIME
def solve(testcase):
    s = I()
    x = I()
    y = I()
    n = len(s)

    xs, xt = 0, 0
    ys, yt = 0, 0

    for c in x:
        if c == '0':
            xs += 1
        else:
            xt += 1
    
    for c in y:
        if c == '0':
            ys += 1
        else:
            yt += 1
    
    if xt == yt:
        if xs == ys:
            print('Yes')
        else:
            print('No')
    else:
        tmp = (ys - xs) * len(s)
        if tmp % (xt - yt):
            print('No')
            return
        
        lent = tmp // (xt - yt)
        if lent < 0:
            print('No')
        elif lent == 0:
            print('Yes')
        else:
            uf = UnionFind(lent)
            return

            idxx, idxy = 0, 0
            while idxx < len(x) and idxy < len(y) and x[idxx] == y[idxy]:
                idxx += 1
                idxy += 1
            
            return
        
            idxxx = 0
            idxyy = 0

            rest = lent
            t = ['' for _ in range(lent)]

            while idxx < len(x) and idxy < len(y) and rest:
                xstate = x[idxx] == '0'
                ystate = y[idxy] == '0'

                if xstate:
                    if ystate:
                        if s[idxxx] != s[idxyy]:
                            print('No')
                            return
                        else:
                            pass

                        idxxx += 1
                        idxyy += 1

                        if idxxx == n:
                            idxx += 1
                            idxxx = 0
                        if idxyy == n:
                            idxy += 1
                            idxyy = 0
                    else:
                        if t[idxyy] == '':
                            t[idxyy] = s[idxxx]
                            rest -= 1
                        else:
                            if t[idxyy] != s[idxxx]:
                                print('No')
                                return
                        
                        idxxx += 1
                        idxyy += 1

                        if idxxx == n:
                            idxx += 1
                            idxxx = 0
                        if idxyy == lent:
                            idxy += 1
                            idxyy = 0
                else:
                    if ystate:
                        if t[idxxx] == '':
                            t[idxxx] = s[idxyy]
                            rest -= 1
                        else:
                            if t[idxxx] != s[idxyy]:
                                print('No')
                                return
                        
                        idxxx += 1
                        idxyy += 1

                        if idxxx == lent:
                            idxx += 1
                            idxxx = 0
                        if idxyy == n:
                            idxy += 1
                            idxyy = 0
                    else:
                        if uf.Union(idxxx, idxyy):
                            rest -= 1
                        
                        idxxx += 1
                        idxyy += 1

                        if idxxx == lent:
                            idxx += 1
                            idxxx = 0
                        if idxyy == lent:
                            idxy += 1
                            idxyy = 0
        

            mul = 19981220
            mod = 10 ** 9 + 7
            pws = pow(mul, n, mod)
            pwt = pow(mul, lent, mod)

            hx, hy = 0, 0

            mp = uf.all_group_members()

            for rt in mp:
                tmp = '_'
                for idxs in mp[rt]:
                    if t[idxs] != '':
                        tmp = t[idxs]
                        break
                for idxs in mp[rt]:
                    t[idxs] = tmp
            
            hs, ht = 0, 0

            for c in s:
                hs = (hs * mul + ord(c)) % mod
            for c in t:
                ht = (ht * mul + ord(c)) % mod

            for c in x:
                if c == '1':
                    hx = (hx * pwt + ht) % mod
                else:
                    hx = (hx * pws + hs) % mod
            
            for c in y:
                if c == '1':
                    hy = (hy * pwt + ht) % mod
                else:
                    hy = (hy * pws + hs) % mod
            print('Yes' if hx == hy else 'No')
            
            



for testcase in range(II()):
    solve(testcase)