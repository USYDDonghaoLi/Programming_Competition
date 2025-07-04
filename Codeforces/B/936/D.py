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
debug = True

# @TIME
def solve(testcase):
    if not debug:
        n, x = MI()
        nums = LII()
    
    '''
    Rnd
    '''
    if debug:
        n, x = 5, randint(1, 8)
        nums = [randint(1, 16) for _ in range(n)]
        print(n, x, nums)
        
        ps = [0]
        for num in nums:
            ps.append(ps[-1] ^ num)
        
        def calc(l, r):
            return ps[r + 1] ^ ps[l]

        def check():
            for r in range(n, 0, -1):
                for c in combinations(range(n), r):
                    if c[-1] != n - 1:
                        continue
                    tmp = 0
                    for i in range(r):
                        if i:
                            tmp |= calc(c[i - 1] + 1, c[i])
                        else:
                            tmp |= calc(0, c[0])
                    if c == (2, 4):
                        print(tmp)
                    if tmp <= x:
                        print(c, tmp)
                        return r
            return -1
        
        DEBUG = check()
    
    x += 1
    
    res = -1
    for i in range(30, -1, -1):
        if (1 << i) > x:
            continue
        
        if x >> i & 1:
            '''
            Case 1: 30到第i + 1位都一样, 第i位是0
            '''
            tmp = x >> (i + 1) << 1
            values = []
            
            l, r = 0, 0
            while r < n:
                cur = nums[r]
                r += 1
                while r < n and (cur >> i) | tmp != tmp:
                    cur ^= nums[r]
                    r += 1
                # print('cur', cur)
                if (cur >> i) | tmp == tmp:
                    assert cur <= x
                    values.append(cur)

                else:
                    # print('values', values)
                    while values and (cur >> i) | tmp != tmp:
                        cur ^= values.pop()
                    
                    if (cur >> i) | tmp == tmp:
                        values.append(cur)
            print(tmp << i, values)
            
            res = max(res, len(values))
    
    print(res if res else -1)
    
    assert DEBUG == (res if res else -1), f"{n}, {x - 1}, {nums}, {DEBUG}, {res}"
    
    

for testcase in range(II()):
    solve(testcase)