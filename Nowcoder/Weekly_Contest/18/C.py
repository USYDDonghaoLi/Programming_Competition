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

# @TIME
def solve(testcase):
    n, k = MI()
    nums = LII()

    if k == 1:
        print(sum(nums))
        return

    mp = defaultdict(int)
    res = 0
    for num in nums:
        t = num % k
        if t == 0:
            res += 1
        else:
            mp[t] += 1
    
    # print('mp', mp)
    
    for r in mp:
        need = -r % k
        if need == r:
            res += mp[r] >> 1
            mp[r] &= 1
        else:
            if need not in mp:
                pass
            else:
                m = min(mp[need], mp[r])
                res += m
                mp[need] -= m
                mp[r] -= m
    
    print(res)
    # for r in mp:
    #     mp[r].sort(reverse = True)
    
    # vals = mp.keys()
    # for val in vals:
    #     need = -val % k
    #     if val == need:
    #         m = len(mp[val])
    #         if m & 1:
    #             res += sum(mp[val]) - mp[val][-1]
    #             mp[val] = [mp[val][-1]]
    #         else:
    #             res += sum(mp[val])
    #             mp[val].clear()
    #     else:
    #         m1, m2 = len(mp[val]), len(mp[need])
    #         if m1 >= m2:
    #             for i in range(m2):
    #                 res += mp[val][i] + mp[need][i]
    #             mp[val] = mp[val][m2:]
    #             mp[need] = mp[need][m2:]
    #         else:
    #             for i in range(m1):
    #                 res += mp[val][i] + mp[need][i]
    #             mp[val] = mp[val][m1:]
    #             mp[need] = mp[need][m1:]
    
    # print(res)

for testcase in range(1):
    solve(testcase)