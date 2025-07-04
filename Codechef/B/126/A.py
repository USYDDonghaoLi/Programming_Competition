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

mul = randint(10 ** 6, 10 ** 9)
mod = getrandbits(64)

class Hash:
    def __init__(self, arr) -> None:
        self.mul = mul
        self.mod = mod
        self.n = len(arr)
        self.mulpw = [1 for _ in range(self.n + 1)]
        for i in range(1, self.n + 1):
            self.mulpw[i] = self.mulpw[i - 1] * self.mul % self.mod

        self.HASH = [0]
        for c in arr:
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
    

# @TIME
def solve(testcase):
    n = II()
    s = [ord(c) for c in I()]
    # if n == 3:
    #     print(1)
    #     return
    
    H = Hash(s)
    S = set()
    
    for i in range(n - 2):
        a, b, c = s[i], s[i + 1], s[i + 2]
        tmp = Hash([b, c, a]).GetHash(0, 3)
        l = H.GetHash(0, i)
        r = H.GetHash(i + 3, n)
        # print('lr', l, r, tmp)
        assert ((l * H.mulpw[n - i] + tmp * H.mulpw[n - i - 3] + r) % H.mod == Hash(s[:i] + [s[i + 1]] + [s[i + 2]] + [s[i]] + s[i + 3:]).GetHash(0, n))
        S.add((l * H.mulpw[n - i] % H.mod + tmp * H.mulpw[n - i - 3] % H.mod + r) % H.mod)
    
    print(len(S))
    

for testcase in range(II()):
    solve(testcase)