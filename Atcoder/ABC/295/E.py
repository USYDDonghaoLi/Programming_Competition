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

RANDOM = getrandbits(32)
 
class Wrapper(int):
    def __init__(self, x):
        int.__init__(x)
 
    def __hash__(self):
        return super(Wrapper, self).__hash__() ^ RANDOM

mod = 998244353

def inv(num):
    return pow(num, mod - 2, mod)

def solve(testcase):
    n, m, k = MI()
    A = LII()

    A2 = [a for a in A if a]
    A2.sort()
    mp = Counter(A2)
    zeroes = len(A) - len(A2)
    totinv = pow(pow(m, zeroes, mod), mod - 2, mod)
    if not zeroes:
        print(A2[k - 1])
        return

    res = 0
    
    for i in range(1, m + 1):
        actual_less = bisect_left(A2, i)
        actual_equal = mp[i]
        actual_more = len(A2) - actual_less - actual_equal

        if actual_less > k - 1:
            continue
        if actual_more > n - k:
            continue

        # for j in range(actual_equal + 1):
        #     left = actual_less + j
        #     # print(j, k - 1 - left, zeroes - k + left)
        #     if left > k - 1 or zeroes < k - left:
        #         continue
        #     res += i * pow(i, k - 1 - left, mod) * pow(m - i, zeroes - (k - left), mod) % mod
        #     res %= mod
        # print('ires1', res)
        
        # if actual_equal:
        for j in range(actual_equal):
            left = actual_less + j
            print('checkj', j, left, k - 1 - left, zeroes - k + 1 + left)
            if left > k - 1 or zeroes < k - left - 1:
                continue
            res += i * pow(i, k - 1 - left, mod) * pow(m - i, zeroes - (k - 1 - left), mod) % mod
            print('resj', res)
            res %= mod
        print('ires', i, res, actual_less, actual_equal, actual_more)

    
    print(res)

for testcase in range(1):
    solve(testcase)