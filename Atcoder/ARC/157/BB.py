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

def solve(testcase):
    n, k = MI()
    s = I()
    if n == 1:
        print(0)
        return
    x, y = [], []
    for i, c in enumerate(s):
        if c == 'X':
            x.append(i)
        else:
            y.append(i)
    
    if s == 'X' * n:
        print(max(0, k - 1))
        return
    if s == 'Y' * n:
        print(max(0, n - 1 - k))
        return

    if k > len(x):
        have_to = k - len(x)
        res = n - 1
        l, r = 0, 0
        nums = []
        while r < n:
            while r < n and s[r] == 'X':
                r += 1
            l = r
            if r == n:
                break
            while r < n and s[r] == 'Y':
                r += 1
            nums.append((r - l + 1 - (l == 0) - (r == n), r - l, l, r))
        nums.sort(key = lambda x: x[0] / x[1])
        # print('nums', nums)
        for i in range(len(nums)):
            if have_to >= nums[i][1]:
                have_to -= nums[i][1]
                res -= nums[i][0]
            else:
                res -= have_to + 1 - (nums[i][2] == 0) - (nums[i][3] == n)
                break
            if not have_to:
                break
        
        print(res)
        return

    if k == len(x):
        print(n - 1)
        return
    
    l, r = 0, 0
    res = 0
    for i in range(1, n):
        res += (s[i] == s[i - 1] == 'Y')
    
    nums = []
    while r < n:
        while r < n and s[r] == 'Y':
            r += 1
        l = r
        if r == n:
            break

        while r < n and s[r] == 'X':
            r += 1
        nums.append((r - l + 1 - (l == 0) - (r == n), r - l))
    # print(nums)

    nums.sort(key = lambda x: x[0] / x[1], reverse = True)
    # print(nums)

    for i in range(len(nums)):
        if k >= nums[i][1]:
            res += nums[i][0]
            k -= nums[i][1]
        else:
            res += k
            break
        if not k:
            break

    print(res)

for testcase in range(1):
    solve(testcase)