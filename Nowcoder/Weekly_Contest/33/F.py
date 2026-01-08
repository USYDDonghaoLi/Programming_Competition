'''
Hala Madrid!
https://github.com/USYDDonghaoLi/Programming_Competition
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
    A = LII()

    stack = []

    res = 0

    def f(l, r, nxt):
        left, right = 0, 6 * 10 ** 9
        LEN = r - l + 1
        while left < right:
            mid = left + right >> 1
            sub = mid // LEN
            
            if r - sub >= nxt + mid:
                left = mid + 1
            else:
                right = mid
            # print("Check f", mid, sub, r - sub, nxt + mid, left, right, r - sub > nxt + mid)
            
        return left

    def g(a):
        nonlocal res
        # print("Check Input of g", a)
        l, r = inf, -inf

        while a <= stack[-1][1]:
            # print("Check a: ", a, stack)
            l, r = stack.pop()
            LEN = r - l + 1
            if not stack:
                need = f(l, r, a)
                tot, rest = divmod(need, LEN)
                if rest == 0:

                    res += LEN * (LEN + 1) // 2 * tot

                    a += need
                    if a == r - tot + 1:
                        stack.append([l - tot, r - tot + 1])
                    else:
                        stack.append([l - tot, r - tot])
                        stack.append([a, a])
                else:
                    '''
                    l, l + rest - 1, 减去tot + 1
                    l + rest, r, 减去tot
                    '''

                    res += LEN * (LEN + 1) // 2 * tot + (LEN + LEN - rest + 1) * rest // 2

                    a += need
                    stack.append([l - tot - 1, l + rest - 1 - tot - 1])
                    if a == r - tot + 1:
                        stack.append([l + rest - tot, r + 1 - tot])
                    else:
                        stack.append([l + rest - tot, r - tot])
                        stack.append([r + 1 - tot, r + 1 - tot])
                break
            
            # print("Check stack in g 1:", stack)

            r2 = stack[-1][1]
            MAX = l - r2 - 1
            # print("Check l, r, r2, MAX", l, r, r2, MAX, stack)
            # assert MAX > 0

            need = f(l, r, a)
            tot, rest = divmod(need, LEN)
            # print("Need", need, tot, rest)
            
            if rest == 0:
                # print("Rest == 0", tot < MAX, tot == MAX)
                if tot < MAX:

                    res += LEN * (LEN + 1) // 2 * tot

                    a += need
                    if a == r - tot + 1:
                        stack.append([l - tot, r - tot + 1])
                    else:
                        stack.append([l - tot, r - tot])
                        stack.append([a, a])
                    break
                elif tot == MAX:

                    res += LEN * (LEN + 1) // 2 * tot

                    a += need
                    l2, r2 = stack.pop()
                    if a == r - tot + 1:
                        stack.append([l2, r - tot + 1])
                    else:
                        stack.append([l2, r - tot])
                        stack.append([a, a])
                    # print("Case 2:", stack)
                    break
                else:

                    res += LEN * (LEN + 1) // 2 * MAX

                    tot_sub = MAX * LEN
                    l2, r2 = stack.pop()
                    stack.append([l2, r - MAX])
                    a += tot_sub
                    # print("Case 3:", stack, a)
            else:
                if tot + 1 < MAX:

                    res += LEN * (LEN + 1) // 2 * tot + (LEN + LEN - rest + 1) * rest // 2

                    a += need
                    stack.append([l - tot - 1, l + rest - 1 - tot - 1])
                    if a == r + 1 - tot:
                        stack.append([l + rest - tot, r + 1 - tot])
                    else:
                        stack.append([l + rest - tot, r + rest - tot])
                        stack.append([a, a])
                elif tot + 1 == MAX:

                    res += LEN * (LEN + 1) // 2 * tot + (LEN + LEN - rest + 1) * rest // 2

                    a += need
                    l2, r2 = stack.pop()
                    stack.append([l2, l + rest - 1 - tot - 1])
                    if a == r + 1 - tot:
                        stack.append([l + rest - tot, r - tot + 1])
                    else:
                        stack.append([l + rest - tot, r + rest - tot])
                        stack.append([a, a])
                else:

                    res += LEN * (LEN + 1) // 2 * MAX

                    tot_sub = MAX * LEN
                    l2, r2 = stack.pop()
                    stack.append([l2, r - MAX])
                    a += tot_sub


    for a in A:
        if not stack:
            stack.append([a, a])
            continue

        # print("Check stack 1")

        l, r = stack[-1]
        if a > r + 1:
            stack.append([a, a])
        elif a == r + 1:
            stack[-1][1] = r
        else:
            g(a)
        
    #     print("Check stack 2", stack)
    
    # print("Final Answer", stack)

    final = []
    for l, r in stack:
        for i in range(l, r + 1):
            final.append(i)
    
    print(res)
    print(*final)

for testcase in range(1):
    solve(testcase)