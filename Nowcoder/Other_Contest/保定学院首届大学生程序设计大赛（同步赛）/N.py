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

# @TIME
def solve(testcase):
    n = II()
    alphabets = [I() for _ in range(n)]
    formula = I()
    m = len(formula)

    def check():
        suffix = []
        tmp = []
        idx = 0
        while idx < m:
            c = formula[idx]
            if c in sheet:
                suffix.append(sheet[c])
            elif c == '(':
                tmp.append(c)
            elif c == ')':
                while tmp and tmp[-1] != '(':
                    suffix.append(tmp.pop())
                tmp.pop()
            elif c in '1234':
                while tmp and tmp[-1] != '(':
                    suffix.append(tmp.pop())
                tmp.append(c)
            idx += 1
        
        while tmp:
            suffix.append(tmp.pop())
        
        stack = []

        for token in suffix:
            if isinstance(token, bool):
                stack.append(token)
            elif token == '1':
                a = stack.pop()
                stack.append(not a)
            elif token == '2':
                b, a = stack.pop(), stack.pop()
                stack.append(a or b)
            elif token == '3':
                b, a = stack.pop(), stack.pop()
                stack.append(a and b)
            elif token == '4':
                b, a = stack.pop(), stack.pop()
                stack.append((not a) or b)
        return stack[0]

    for state in range(1 << n):
        sheet = {}
        for i in range(n):
            if state >> i & 1:
                sheet[alphabets[i]] = True
            else:
                sheet[alphabets[i]] = False
        
        if check():
            out = ['1' if state >> i & 1 else '0' for i in range(n)]
            print(''.join(out))

for testcase in range(1):
    solve(testcase)