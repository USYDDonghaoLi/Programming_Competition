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

# @TIME
def solve(testcase):
    '''
    n * a - b = 
    '''
    n = II()
    res = []
    cur = 0
    m = str(n)
    
    for i in range(1, 1001):
        if n == 1:
            print(0)
            return
        if 1 < n < 10:
            cur = cur * 10 + n
            if (cur - i) % (n - 1) == 0:
                a = (cur - i) // (n - 1)
                b = a - i
                if 1 <= a <= 10000 and 1 <= b <= 10000:
                    res.append((a, b))
        elif n < 100:
            cur = cur * 10 + int(m[0])
            if (cur - 2 * i + 1) % (n - 2) == 0:
                a = (cur - 2 * i + 1) // (n - 2)
                b = 2 * a - (2 * i - 1)
                if 1 <= a <= 10000 and 1 <= b <= 10000:
                    res.append((a, b))
                    
            cur = cur * 10 + int(m[1])
            if (cur - 2 * i) % (n - 2) == 0:
                a = (cur - 2 * i) // (n - 2)
                b = 2 * a - (2 * i)
                if 1 <= a <= 10000 and 1 <= b <= 10000:
                    res.append((a, b))

        else:
            cur = cur * 10 + int(m[0])
            if (cur - 3 * i + 2) % (n - 3) == 0:
                a = (cur - 3 * i + 2) // (n - 3)
                b = 3 * a - (3 * i - 2)
                if 1 <= a <= 10000 and 1 <= b <= 10000:
                    res.append((a, b))
                    
            cur = cur * 10 + int(m[1])
            if (cur - 3 * i + 1) % (n - 3) == 0:
                a = (cur - 3 * i + 1) // (n - 3)
                b = 3 * a - (3 * i + 1)
                if 1 <= a <= 10000 and 1 <= b <= 10000:
                    res.append((a, b))
                    
            cur = cur * 10 + int(m[2])
            if (cur - 3 * i) % (n - 3) == 0:
                a = (cur - 3 * i) // (n - 3)
                b = 3 * a - (3 * i)
                if 1 <= a <= 10000 and 1 <= b <= 10000:
                    res.append((a, b))
                    
        '''
        一位数
        a * n - b = cur
        a - b = i
        两位数
        a * n - b = cur
        2 * a - b = 2 * i - 1
        '''
        if cur > 20000 * n:
            break
    
    print(len(res))
    for a, b in res:
        print(a, b)
    
    # for i in range(1, 3001):
    #     for j in range(1, 3001):
    #         if str(i * n - j) == (m * i)[:-j]:
    #             print(i, j)
            

for testcase in range(II()):
    solve(testcase)