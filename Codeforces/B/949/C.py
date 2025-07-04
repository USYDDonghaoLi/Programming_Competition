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

# @TIME
def solve(testcase):
    
    n = II()
    nums = LII()
    
    res = nums[:]
    
    for i in range(1, n):
        if res[i] != -1 and res[i - 1] != -1:
            if res[i] == res[i - 1] >> 1 or res[i] >> 1 == res[i - 1]:
                pass
            else:
                print(-1)
                return
    
    if all(num == -1 for num in nums):
        res[0] = 1
        for i in range(1, n):
            if res[i - 1] * 2 <= 10 ** 9:
                res[i] = res[i - 1] << 1
            else:
                res[i] = res[i - 1] >> 1
        print(*res)
        return
    
    intervals = []
    l, r = 0, 0
    
    while r < n and nums[r] != -1:
        r += 1
    
    l = r
    
    while r < n:
        while r < n and nums[r] == -1:
            r += 1
        intervals.append((l, r))
        l = r
        if r == n:
            break
        while r < n and nums[r] != -1:
            r += 1
        l = r
    
    # print(intervals)
    
    for l, r in intervals:
        if l == 0:
            # NXT = nums[r + 1]
            for i in range(r - 1, l - 1, -1):
                if res[i + 1] * 2 <= 10 ** 9:
                    res[i] = res[i + 1] << 1
                else:
                    res[i] = res[i + 1] >> 1
        elif r == n:
            for i in range(l, r):
                if res[i - 1] * 2 <= 10 ** 9:
                    res[i] = res[i - 1] << 1
                else:
                    res[i] = res[i - 1] >> 1
        else:
            PRE, NXT = nums[l - 1], nums[r]
            LEN = r - l + 1
            pre = bin(PRE)[2:].lstrip('0')
            nxt = bin(NXT)[2:].lstrip('0')
            
            # print(PRE, pre, NXT, nxt)
            
            if PRE == NXT:
                need = 0
            else:
            
                for i in range(10 ** 9):
                    if pre[:i] == nxt[:i]:
                        continue
                    else:
                        break
                need = max(0, len(pre) - i + 1) + max(0, len(nxt) - i + 1)
            # print('need', need, LEN, (need - LEN) & 1)
            
            if need > LEN:
                print(-1)
                return
            
            elif not ((need - LEN) & 1):
                LEFT, RIGHT = l, r - 1
                # print('res', res, LEFT, RIGHT)
                if need:
                    for _ in range(max(0, len(pre) - i + 1)):
                        res[LEFT] = res[LEFT - 1] >> 1
                        LEFT += 1               
                    for _ in range(max(0, len(nxt) - i + 1)):
                        res[RIGHT] = res[RIGHT + 1] >> 1
                        RIGHT -= 1
                # print('res', res)
                
                flag = res[LEFT - 1] >= 2
                
                for ii in range(LEFT, RIGHT + 1):
                    if ii & 1 == LEFT & 1:
                        if not flag:
                            res[ii] = res[ii - 1] << 1
                        else:
                            res[ii] = res[ii - 1] >> 1
                    else:
                        if not flag:
                            res[ii] = res[ii - 1] >> 1
                        else:
                            res[ii] = res[ii - 1] << 1
            
            else:
                print(-1)
                return
    
    print(*res)
    
    for i in range(1, n):
        assert res[i - 1] != -1 and res[i] != -1 and (res[i - 1] == res[i] >> 1 or res[i - 1] >> 1 == res[i])
                

for testcase in range(II()):
    solve(testcase)