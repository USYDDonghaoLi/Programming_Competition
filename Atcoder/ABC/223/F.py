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
    n, q = MI()
    sz = int(sqrt(n))
    s = I()
    buckets = [[] for _ in range(sz + 10)]
    for i, c in enumerate(s):
        buckets[i // sz].append(c)
    # print('buckets', buckets)
    # print('sz', sz)
    
    desc = [0 for _ in range(sz + 10)]
    add = [0 for _ in range(sz + 10)]

    def modify(where):
        cur = 0
        desc[where] = 0
        for c in buckets[where]:
            if c == '(':
                cur += 1
            else:
                cur -= 1
            desc[where] = min(desc[where], cur)
        add[where] = cur

    for i in range(sz + 10):
        modify(i)

    # print('desc', desc)
    # print('add', add)

    for _ in range(q):
        op, l, r = MI()
        l -= 1
        r -= 1
        lb, lid = divmod(l, sz)
        rb, rid = divmod(r, sz)
        # print('l_info', l, lb, lid)
        # print('r_info', r, rb, rid)

        if op == 1:
            buckets[lb][lid], buckets[rb][rid] = buckets[rb][rid], buckets[lb][lid]
            modify(lb)
            modify(rb)
        else:
            if lb == rb:
                cur = 0
                for i in range(lid, rid + 1):
                    if buckets[lb][i] == '(':
                        cur += 1
                    else:
                        cur -= 1
                    if cur < 0:
                        print('No')
                        break
                else:
                    print('Yes' if cur == 0 else 'No')
            else:
                cur = 0
                flag = True
                for i in range(lid, len(buckets[lb])):
                    if buckets[lb][i] == '(':
                        cur += 1
                    else:
                        cur -= 1
                    if cur < 0:
                        flag = False
                        break
                if not flag:
                    print('No')
                    continue
                    
                lb += 1
                for i in range(lb, rb):
                    if cur + desc[i] < 0:
                        flag = False
                        break
                    else:
                        cur += add[i]
                if not flag:
                    print('No')
                    continue

                for i in range(rid + 1):
                    if buckets[rb][i] == '(':
                        cur += 1
                    else:
                        cur -= 1
                    if cur < 0:
                        flag = False
                        break
                if not flag:
                    print('No')
                    continue
                print('Yes' if cur == 0 else 'No')
                    



for testcase in range(1):
    solve(testcase)