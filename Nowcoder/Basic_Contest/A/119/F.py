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

def calc(a, seg):
    b, c = divmod(a - seg + 1, seg)
    return c * (b + 1) * (b + 2) // 2 + (seg - c) * b * (b + 1) // 2

# @TIME
def solve(testcase):
    n, k = MI()
    s = I()
    
    cnt = 0
    A = []

    l, r = 0, 0
    while r < n and s[r] == 'x':
        r += 1
    l = r

    while r < n:
        while r < n and s[r] == 'o':
            r += 1
        A.append(r - l)
        cnt += r - l
        l = r
        if r == n:
            break

        while r < n and s[r] == 'x':
            r += 1
        l = r
    
    if cnt <= k:
        print(0)
        return
    
    # print('A', A)



    pq = []
    res = 0
    for a in A:
        cur = a * (a + 1) // 2
        res += cur
        new = calc(a, 2)
        heappush(pq, (new - cur, cur, a, 1))
    
    # print('pq', pq)
    
    while k:
        diff, cur, a, seg = heappop(pq)
        res += diff
        cur += diff
        seg += 1
        new = calc(a, seg + 1)
        heappush(pq, (new - cur, cur, a, seg))
        k -= 1
        # print('respq', res, pq)
    
    print(res)

    # def check(mid):
    #     ans = 0
    #     for a in A:
    #         ans += a // (mid + 1)
    #     return ans <= k

    # l, r = 1, max(A) + 1
    # while l < r:
    #     mid = l + r >> 1
    #     if not check(mid):
    #         l = mid + 1
    #     else:
    #         r = mid
    
    # print('ok', l)

    # res = 0

    # mp = defaultdict(int)

    # for a in A:
    #     b = a // (l + 1)
    #     a -= b
    #     c, d = divmod(a, b + 1)
    #     res += (b + 1 - d) * c * (c + 1) // 2
    #     res += d * (c + 1) * (c + 2) // 2
    #     if c:
    #         mp[c] += b + 1 - d
    #     mp[c + 1] += d
    
    # print('mp', mp)

    # vals = sorted(list(mp.values()))
    # idx = 0

    # print('vals', vals)
    # # while k:
    # #     cur = mp[vals[idx]]
    # #     while idx < len(vals) and not mp[cur]:
    # #         idx += 1
    # #     cur = mp[vals[idx]]
    # #     res -= cur
    # #     k -= 1


    # print(res)

for testcase in range(II()):
    solve(testcase)