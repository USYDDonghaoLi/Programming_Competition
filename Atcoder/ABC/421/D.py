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

d = ((1, 0), (0, 1), (-1, 0), (0, -1))
dd = {'D': 0, 'R': 1, 'U': 2, 'L': 3}

# @TIME
def solve(testcase):
    sx, sy, tx, ty = MI()
    n, m, l = MI()

    A = deque()
    B = deque()

    for _ in range(m):
        s, a = LI()
        a = int(a)
        idx = dd[s]
        if a < 0:
            idx, a = (idx + 2) % 4, -a
        dx, dy = d[idx]
        if a:
            A.append((dx, dy, a))
    
    for _ in range(l):
        s, a = LI()
        a = int(a)
        idx = dd[s]
        if a < 0:
            idx, a = (idx + 2) % 4, -a
        dx, dy = d[idx]
        if a:
            B.append((dx, dy, a))
    
    
    
    res = 0
    while A and B:
        # if sx == tx and sy == ty:
        #     res += 1
        
        dxa, dya, stepa = A.popleft()
        dxb, dyb, stepb = B.popleft()

        step = fmin(stepa, stepb)

        if dxa == 1:
            if dxb == 1:
                if sx == sy and tx == ty:
                    res += step - 1
                # res += step
                sx += step
                tx += step
            elif dxb == -1:
                if sy != ty:
                    sx += step
                    tx -= step
                    # res += step
                else:
                    x_diff = tx - sx
                    if not x_diff & 1 and 0 < x_diff < 2 * step:
                        res += 1
                        # print(res + (x_diff >> 1))
                    # res += step
                    sx += step
                    tx -= step
            else:
                if dyb == 1:
                    x_diff = tx - sx
                    y_diff = sy - ty
                    if x_diff == y_diff and 0 < x_diff < step:
                        res += 1
                        # print(res + x_diff)

                    # res += step
                    sx += step
                    ty += step
                else:
                    x_diff = tx - sx
                    y_diff = ty - sy
                    if x_diff == y_diff and 0 < x_diff < step:
                        # print(res + x_diff)
                        res += 1
                        # return
                    # res += step
                    sx += step
                    ty -= step
        
        elif dxa == -1:
            if dxb == -1:
                # res += step
                if sx == sy and tx == ty:
                    res += step - 1
                sx -= step
                tx -= step
            elif dxb == 1:
                if sy != ty:
                    # res += step
                    sx -= step
                    tx += step
                else:
                    x_diff = sx - tx
                    if not x_diff & 1 and 0 < x_diff < 2 * step:
                        res += 1
                        # print(res + (x_diff >> 1))
                    # res += step
                    sx -= step
                    tx += step
            else:
                if dyb == 1:
                    # print('h2')
                    x_diff = sx - tx
                    y_diff = sy - ty
                    if x_diff == y_diff and 0 < x_diff < step:
                        # print(res + x_diff)
                        res += 1
                    # res += step
                    sx -= step
                    ty += step
                else:
                    x_diff = sx - tx
                    y_diff = ty - sy
                    if x_diff == y_diff and 0 < x_diff < step:
                        # print(res + x_diff)
                        res += 1
                    # res += step
                    sx -= step
                    ty -= step
        
        elif dya == 1:
            assert dxa == 0
            if dyb == 1:
                if sx == sy and tx == ty:
                    res += step - 1
                # res += step
                sy += step
                ty += step
            elif dyb == -1:
                if sx != tx:
                    # res += step
                    sy += step
                    ty -= step
                else:
                    y_diff = ty - sy
                    if not y_diff & 1 and 0 < y_diff < 2 * step:
                        # print(res + (y_diff >> 1))
                        res += 1
                    # res += step
                    sy += step
                    ty -= step
            else:
                if dxb == 1:
                    x_diff = sx - tx
                    y_diff = ty - sy
                    if x_diff == y_diff and 0 < x_diff < step:
                        # print(res + x_diff)
                        res += 1
                    # res += step
                    sy += step
                    tx += step
                else:
                    x_diff = tx - sx
                    y_diff = ty - sy
                    if x_diff == y_diff and 0 < x_diff < step:
                        # print(res + x_diff)
                        res += 1
                    # res += step
                    sy += step
                    tx -= step
        
        else:
            assert dxa == 0
            assert dya == -1
            if dyb == -1:
                if sx == sy and tx == ty:
                    res += step - 1
                # res += step
                sy -= step
                ty -= step
            elif dyb == 1:
                if sx != tx:
                    # res += step
                    sy -= step
                    ty += step
                else:
                    y_diff = sy - ty
                    if not y_diff & 1 and 0 < y_diff < step:
                        # print(res + (y_diff >> 1))
                        res += 1
                    # res += step
                    sy -= step
                    ty += step
            else:
                if dxb == 1:
                    x_diff = sx - tx
                    y_diff = sy - ty
                    if x_diff == y_diff and 0 < x_diff < step:
                        # print(res + x_diff)
                        res += 1
                    # res += step
                    sy -= step
                    tx += step
                else:
                    x_diff = tx - sx
                    y_diff = sy - ty
                    if x_diff == y_diff and 0 < x_diff < step:
                        # print(res + x_diff)
                        res += 1
                    # res += step
                    sy -= step
                    tx -= step
        
        stepa -= step
        stepb -= step

        if stepa:
            A.appendleft((dxa, dya, stepa))
        if stepb:
            B.appendleft((dxb, dyb, stepb))
        
        # print(sx, sy, tx, ty, A, B)
    
        if sx == tx and sy == ty:
            res += 1
    
    print(res)




for testcase in range(1):
    solve(testcase)