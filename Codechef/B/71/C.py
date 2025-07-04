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

def ask():
    pass

def answer():
    pass

mod = 998244353

def solve(testcase):
    n, m = MI()

    #assert (n + m != mod)
    base = (n + 1) // 2
    down = n + m
    if not n & 1:
        up = n * (base + (m + 1) // 2)
    else:
        up = n * (base + m // 2)
    #print('ud', up, down)
    print(up * pow(down, mod - 2, mod) % mod)
    
    # def add(a, b, c, d):
    #     g = gcd(a * d + b * c, b * d)
    #     return (a * d + b * c) // g, (b * d) // g

    # @lru_cache(None)
    # def calc(a, b):
    #     if a == 1 and b == 0:
    #         return 1, 1
    #     if a == 0 and b == 1:
    #         return 0, 1
        
    #     r1, r2 = 0, 1
    #     if a >= 2:
    #         c, d = calc(a - 2, b)
    #         r1, r2 = add(r1, r2, a * (a - 1) * (c + d), (a + b) * (a + b - 1) * d)
    #         #res += a * (a - 1) / ((a + b) * (a + b - 1)) * (1 + calc(a - 2, b))
    #     if a >= 1 and b >= 1:
    #         c, d = calc(a - 1, b - 1)
    #         r1, r2 = add(r1, r2, a * b * (2 * c + d), (a + b) * (a + b - 1) * d)
    #         # res += a * b / ((a + b) * (a + b - 1)) * (1 + calc(a - 1, b - 1))
    #         # res += a * b / ((a + b) * (a + b - 1)) * (calc(a - 1, b - 1))
    #     if b >= 2:
    #         c, d = calc(a, b - 2)
    #         r1, r2 = add(r1, r2, b * (b - 1) * c, (a + b) * (a + b - 1) * d)
    #         #res += b * (b - 1) / ((a + b) * (a + b - 1)) * (calc(a, b - 2))
        
    #     print(a, b, f"{r1}/{r2}")
    #     return r1, r2
    
    # print(calc(n, m))

for testcase in range(II()):
    solve(testcase)