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

# def mysqrt(num):
#     l, r = 1, num
#     while l < r:
#         mid = l + r >> 1
#         if mid * mid < num:
#             l = mid + 1
#         else:
#             r = mid
#     while l * l > num:
#         l -= 1
#     return l

# @TIME
def solve(testcase):
    
    s = I()
    n = len(s)
    res = 0
    nums = [1, 80, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
    num = int(s)
    for val in nums:
        if val <= num:
            res += 1
        else:
            break
    
    if num < 100:
        print(res)
        return
    
    for i in range(3, n + 1):
        if i & 1:
            l = int('1' + '0' * (i - 1))
            r = int('1' + '0' * (i // 2) + '9' * (i // 2))
            # print(l, r)
            
            # while l < r:
            #     mid = l + r >> 1
            #     tmp = mysqrt(mid)
            #     if str(mid).startswith(str(tmp)):
            #         l = mid + 1
            #     else:
            #         r = mid
            
            # l -= 1
            # print('l', l)
            res += max(0, min(r, num) - l + 1)
        
        else:
            l = int('9' * (i // 2) + '0' * (i // 2))
            r = int('9' * i)
            
            # while l < r:
            #     mid = l + r >> 1
            #     tmp = mysqrt(mid)
            #     if not str(mid).startswith(str(tmp)):
            #         l = mid + 1
            #     else:
            #         r = mid
            
            # print('lr', l, r)
            res += max(0, min(r, num) - l + 1)
            if int('9' * (i // 2 - 1) + '8' + '0' * (i // 2)) <= num:
                res += 1
    
    print(res)
    
    # def force(num):
    #     res = 0
    #     for i in range(1, num + 1):
    #         t = int(sqrt(i))
    #         if str(i).startswith(str(t)):
    #             res += 1
    #     return res
    
    # print('force', num, force(num))

for testcase in range(II()):
    solve(testcase)