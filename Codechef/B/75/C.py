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

'''
手写栈防止recursion limit
注意要用yield 不要用return
函数结尾要写yield None
'''
from types import GeneratorType
def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc

@lru_cache(None)
def f(x):
    if x == 1:
        return 0
    else:
        if x & 1:
            return f(x >> 1)
        else:
            return f(x >> 1) + 1

@lru_cache(None)
def g(x):
    if x == 1:
        return 1
    else:
        if x & 1:
            return 2 * g(x >> 1)
        else:
            return 2 * g(x >> 1) + 1

pw = [1 << i for i in range(32)]

def solve(testcase):
    # for i in range(4, 128, 4):
    #     print(i, f(i), g(i), f(i) + g(i))
    l, r = MI()
    left = pw[bisect_left(pw, l)]
    right = pw[bisect_right(pw, r) - 1]
    if left > right:
        res = max(f(l) + g(l), f(r) + g(r))
        new = (l + 7) // 8 * 8
        for _ in range(10):
            if new <= r:
                res = max(res, f(new) + g(new))
                new += 8
            else:
                break
        new = r // 8 * 8
        for _ in range(10):
            if new >= l:
                res = max(res, f(new) + g(new))
                new -= 8
            else:
                break
        print(res)
    else:
        print(f(right) + g(right))

for testcase in range(II()):
    solve(testcase)