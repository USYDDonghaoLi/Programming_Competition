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
up = [chr(ord('A') + i) for i in range(26)]
down = [chr(ord('a') + i) for i in range(26)]
digit = [chr(ord('0') + i) for i in range(10)]
special = ',.?!'

# @TIME
def solve(testcase):
    s = I()
    n = len(s)

    cnt = [0 for _ in range(5)]
    for c in s:
        if c.isupper():
            cnt[0] += 1
        elif c.islower():
            cnt[1] += 1
        elif c.isdigit():
            cnt[2] += 1
        elif c in special:
            cnt[3] += 1
        else:
            cnt[4] += 1
    
    fail = 0
    for i in range(4):
        fail += cnt[i] == 0
    fail += cnt[4] != 0

    res = 0

    for c in s:
        if c.isupper():
            cnt[0] -= 1
            if not cnt[0]:
                fail += 1
        elif c.islower():
            cnt[1] -= 1
            if not cnt[1]:
                fail += 1
        elif c.isdigit():
            cnt[2] -= 1
            if not cnt[2]:
                fail += 1
        elif c in special:
            cnt[3] -= 1
            if not cnt[3]:
                fail += 1
        else:
            cnt[4] -= 1
            if not cnt[4]:
                fail -= 1
        
        for ch in up:
            if ch == c:
                continue
            else:
                cnt[0] += 1
                if cnt[0] == 1:
                    fail -= 1
                if not fail:
                    res += 1
                cnt[0] -= 1
                if not cnt[0]:
                    fail += 1
        
        for ch in down:
            if ch == c:
                continue
            else:
                cnt[1] += 1
                if cnt[1] == 1:
                    fail -= 1
                if not fail:
                    res += 1
                cnt[1] -= 1
                if not cnt[1]:
                    fail += 1
        
        for ch in digit:
            if ch == c:
                continue
            else:
                cnt[2] += 1
                if cnt[2] == 1:
                    fail -= 1
                if not fail:
                    res += 1
                cnt[2] -= 1
                if not cnt[2]:
                    fail += 1
        
        for ch in special:
            if ch == c:
                continue
            else:
                cnt[3] += 1
                if cnt[3] == 1:
                    fail -= 1
                if not fail:
                    res += 1
                cnt[3] -= 1
                if not cnt[3]:
                    fail += 1
        
        if c.isupper():
            cnt[0] += 1
            if cnt[0] == 1:
                fail -= 1
        elif c.islower():
            cnt[1] += 1
            if cnt[1] == 1:
                fail -= 1
        elif c.isdigit():
            cnt[2] += 1
            if cnt[2] == 1:
                fail -= 1
        elif c in special:
            cnt[3] += 1
            if cnt[3] == 1:
                fail -= 1
        else:
            cnt[4] += 1
            if cnt[3] == 1:
                fail += 1
    
    print(res)
                

for testcase in range(II()):
    solve(testcase)