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

# for i in range(2, 11):
#     for p in permutations([val for val in range(1, i + 1)]):
#         flag = True
#         for j in range(1, i):
#             if 2 <= abs(p[j] - p[j - 1]) <= 4:
#                 continue
#             else:
#                 flag = False
#                 break        
#         if flag:
#             print(i, p)
#             break
# @TIME
def solve(testcase):
    n = II()
    if n <= 3:
        print(-1)
    elif n == 4:
        print(*[2, 4, 1, 3])
    else:
        res = []
        o, e = 1, 2
        while True:
            for _ in range(3):
                if o <= n:
                    res.append(o)
                    o += 2
            if e + 4 <= n:
                if e <= n:
                    res.append(e)
                e += 4
                if e <= n:
                    res.append(e)
                e -= 2
                if e <= n:
                    res.append(e)
                e += 4
            else:
                break
                
            if o > n and e > n:
                break
        
        need = []
        while e <= n:
            need.append(e)
            e += 2
        # print(need)
        
        k = len(need)
        assert k < 3
        if k == 0:
            pass
        elif k == 1:
            if n & 1:
                res = res[:-3] + need + res[-3:]
            else:
                res = res[:-2] + need + res[-2:]
        else:
            if n & 1:
                res = res[:-3] + need + res[-3:]
            else:
                res = res[:-2] + need + res[-2:]
        
        print(*res)
            
        
        for i in range(1, n):
            assert 2 <= abs(res[i] - res[i - 1]) <= 4


for testcase in range(II()):
    solve(testcase)