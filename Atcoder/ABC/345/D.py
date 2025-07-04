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
    n, h, w = MI()
    rects = [LII() for _ in range(n)]
    rects.sort(key = lambda x: -x[0] * x[1])
    area = h * w
    
    def check(state):
        valid = []
        total = 0
        for i in range(n):
            if state >> i & 1:
                x, y = rects[i]
                valid.append((x, y))
                total += x * y
        
        if total != area:
            return False
        
        # print('Valid!', valid)
        
        m = len(valid)
        grid = [[False for _ in range(w)] for _ in range(h)]
        
        def TRY(idx):
            # print(idx, valid[idx], grid)
            if idx == m:
                return True
            else:
                x, y = valid[idx]
                '''
                (x, y)
                '''
                # final = False
                for i in range(h - x + 1):
                    for j in range(w - y + 1):
                        if grid[i][j]:
                            continue
                        else:
                            flag = True
                            for k in range(i, i + x):
                                for l in range(j, j + y):
                                    if grid[k][l]:
                                        flag = False
                                        break
                                if not flag:
                                    break
                            
                            if flag:
                                # final = True
                                for k in range(i, i + x):
                                    for l in range(j, j + y):
                                        grid[k][l] = True
                                
                                if TRY(idx + 1):
                                    return True
                                
                                for k in range(i, i + x):
                                    for l in range(j, j + y):
                                        grid[k][l] = False
                
                x, y = y, x
                
                for i in range(h - x + 1):
                    for j in range(w - y + 1):
                        if grid[i][j]:
                            continue
                        else:
                            flag = True
                            for k in range(i, i + x):
                                for l in range(j, j + y):
                                    if grid[k][l]:
                                        flag = False
                                        break
                                if not flag:
                                    break
                            
                            if flag:
                                # final = True
                                for k in range(i, i + x):
                                    for l in range(j, j + y):
                                        grid[k][l] = True
                                
                                if TRY(idx + 1):
                                    return True
                                
                                for k in range(i, i + x):
                                    for l in range(j, j + y):
                                        grid[k][l] = False
                
                
                return False
        
        # print('TRY', valid, TRY(0))
        return TRY(0)
                
        
        
    
    for state in range(1, 1 << n):
        if check(state):
            print('Yes')
            return
    
    print('No')

for testcase in range(1):
    solve(testcase)