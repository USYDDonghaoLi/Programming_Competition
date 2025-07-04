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

lg = [0 for _ in range(4010)]
for i in range(2, 4010):
    lg[i] = lg[i >> 1] + 1

def solve(testcase):
    n = II()
    mp = defaultdict(int)
    intervals = []
    cnt = 1
    for i in range(1, n + 1):
        #print(i, i, flush = True)
        mp[(i, i)] = cnt
        intervals.append((i, i))
        cnt += 1
        for j in range(12):
            new = i + (1 << j)
            if new > n:
                break
            else:
                mp[(i, new)] = cnt
                #print(i, new, flush = True)
                intervals.append((i, new))
                cnt += 1

    print(len(intervals), flush = True)
    for a, b in intervals:
        print(a, b, flush = True)
    
    #print('check', intervals, flush = True)
    
    q = II()
    for _ in range(q):
        l, r = MI()
        if l == r:
            a = b = mp[(l, l)]
            print(a, b, flush = True)
            #print('check', intervals[a - 1], flush = True)
        else:
            d = lg[r - l]
            a = mp[(l, l + (1 << d))]
            b = mp[(r - (1 << d), r)]
            print(a, b, flush = True)
            #print('check', intervals[a - 1], intervals[b - 1], flush = True)


for testcase in range(1):
    solve(testcase)