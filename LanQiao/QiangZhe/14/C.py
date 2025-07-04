# '''
# Hala Madrid!
# https://www.zhihu.com/people/li-dong-hao-78-74
# '''

# import sys
# import os
# from io import BytesIO, IOBase
# BUFSIZE = 8192
# class FastIO(IOBase):
#     newlines = 0
#     def __init__(self, file):
#         self._fd = file.fileno()
#         self.buffer = BytesIO()
#         self.writable = "x" in file.mode or "r" not in file.mode
#         self.write = self.buffer.write if self.writable else None
#     def read(self):
#         while True:
#             b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
#             if not b:
#                 break
#             ptr = self.buffer.tell()
#             self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
#         self.newlines = 0
#         return self.buffer.read()
#     def readline(self):
#         while self.newlines == 0:
#             b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
#             self.newlines = b.count(b"\n") + (not b)
#             ptr = self.buffer.tell()
#             self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
#         self.newlines -= 1
#         return self.buffer.readline()
#     def flush(self):
#         if self.writable:
#             os.write(self._fd, self.buffer.getvalue())
#             self.buffer.truncate(0), self.buffer.seek(0)
# class IOWrapper(IOBase):
#     def __init__(self, file):
#         self.buffer = FastIO(file)
#         self.flush = self.buffer.flush
#         self.writable = self.buffer.writable
#         self.write = lambda s: self.buffer.write(s.encode("ascii"))
#         self.read = lambda: self.buffer.read().decode("ascii")
#         self.readline = lambda: self.buffer.readline().decode("ascii")
# sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
# input = lambda: sys.stdin.readline().rstrip("\r\n")

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

seed(19981220)
RANDOM = getrandbits(48)
 
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

class Hash:
    def __init__(self, arr, mul = 131, mod = 10 ** 9 + 7) -> None:
        self.arr = arr
        self.mul = mul
        self.mod = mod
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
        mul = 131
        mod = 10 ** 9 + 7
        n = len(arr)
        res = 0
        
        for c in arr:
            res = (res * mul + c) % mod
        
        return res

# @TIME
def solve(testcase):
    n = II()
    s = list(I())
    H1 = Hash([ord(c) for c in s])
    H2 = Hash([ord(c) for c in s[::-1]])
    
    res = 0
    
    for length in range(1, n + 1):
        mp = defaultdict(int)
        for i in range(n):

            if i + length > n:
                break
            else:
                if s[i] == '0' or s[i + length - 1] == '0':
                    continue
                '''
                i, i + length - 1
                '''
                mp[H2.GetHash(n - 1 - (i + length - 1), n - i)] += 1
        
        r = 0
        for l in range(n):
            if l + length + length > n:
                break
            if s[l] == '0' or s[l + length - 1] == '0':
                continue
            h = H1.GetHash(l, l + length)

            
            while r < l + length:
                if r + length > n:
                    break
                if s[r] == '0' or s[r + length - 1] == '0':
                    r += 1
                    continue
                mp[H2.GetHash(n - 1 - (r + length - 1), n - r)] -= 1
                r += 1
            
            res += mp[h]
            
    
    print(res)

for testcase in range(1):
    solve(testcase)