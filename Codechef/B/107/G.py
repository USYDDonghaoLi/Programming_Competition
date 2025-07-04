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

pw = [1 for _ in range(6)]
for i in range(1, 6):
    pw[i] = pw[i - 1] * 3
ok = [1 for _ in range(pw[5])]

for i in range(pw[5]):
    q = [0 for _ in range(5)]
    for j in range(5):
        q[j] = (i // pw[j]) % 3
    for j in range(5):
        for k in range(5):
            if j == k:
                continue
            if q[j] == 2 and q[k] >= 1 and (2 * j + k) % 5 == 0:
                ok[i] = False
            for l in range(5):
                if j == l or k == l:
                    continue
                if q[j] and q[k] and q[l] and (j + k + l) % 5 == 0:
                    ok[i] = False
                
# @TIME
def solve(testcase):
    n = II()
    nums = LII()

    c = [[] for _ in range(5)]
    need = 0
    tot = 0
    for num in nums:
        if num == -1:
            need += 1
        else:
            c[num % 5].append(num)
            tot += num

    mask = 0
    for i in range(5):
        c[i].sort()
        mask += min(len(c[i]), 2) * pw[i]

    if not ok[mask]:
        print(-1)
        return

    res = float('inf')
    for i in range(pw[5]):
        if not ok[i]:
            continue
        flag = True
        cur = 0
        s = []
        q = [0 for _ in range(5)]
        for j in range(5):
            q[j] = (i // pw[j]) % 3
            if q[j] == 2:
                if j == 0:
                    mx = 2
                else:
                    mx = n
            else:
                mx = q[j]

            if len(c[j]) > mx:
                flag = False
                break

        if not flag:
            continue

        for j in range(5):
            if j == 0:
                start = 5
            else:
                start = j
            k = 0
            
            if q[j] == 2:
                if j == 0:
                    mx = 2
                else:
                    mx = n
            else:
                mx = q[j]
            mx -= len(c[j])

            while mx > 0:
                while k < len(c[j]) and start == c[j][k]:
                    start += 5
                    k += 1

                if len(s) == need:
                    if -start < s[0]:
                        break
                    cur += heappop(s)
                    heappush(s, -start)
                    cur += start
                else:
                    heappush(s, -start)
                    cur += start
                start += 5
                mx -= 1
            
        if len(s) == need:
            # print('s', s, sum(s))
            res = min(res, cur)
    
    if res == float('inf'):
        print(-1)
    else:
        print(res + tot)

for testcase in range(II()):
    solve(testcase)