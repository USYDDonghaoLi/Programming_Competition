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

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0 for _ in range(n)]

    def lowbit(self, x):
        return x & (-x)

    def update(self, pos, x):
        while pos < self.n:
            self.tree[pos] += x
            pos += self.lowbit(pos)

    def query(self, pos):
        to_ret = 0
        while pos:
            to_ret += self.tree[pos]
            pos -= self.lowbit(pos)
        return to_ret

    def query_sum(self, l, r):
        return self.query(r) - self.query(l - 1)

def solve(testcase):
    n = II()
    nums = LII()
    c = Counter(nums)
    print('c', c)

    res = 0
    not_one = []
    for i in range(c[1]):
        if nums[i] != 1:
            res += 1
            not_one.append(nums[i])
            nums[i] = 1
    not_one.sort()
    idx = 0
    for i in range(c[1], n):
        if nums[i] == 1:
            nums[i] = not_one[idx]
            idx += 1
    print('one', nums, res)
    
    not_two = []
    for i in range(c[1], c[1] + c[2]):
        print('debug_two', nums, i, nums[i], nums[i] != 2)
        if nums[i] != 2:
            res += 1
            not_two.append(nums[i])
            nums[i] = 2
    not_two.sort()
    idx = 0
    for i in range(c[1] + c[2], n):
        if nums[i] == 2:
            nums[i] = not_two[idx]
            idx += 1
    print('two', nums, res)

    not_three = []
    for i in range(c[1] + c[2], c[1] + c[2] + c[3]):
        if nums[i] != 3:
            res += 1
            not_three.append(nums[i])
            nums[i] = 3
    not_three.sort()
    idx = 0
    for i in range(c[1] + c[2] + c[3], n):
        if nums[i] == 3:
            nums[i] = not_three[idx]
            idx += 1

    print('nums', nums)
    print(res)
    # c = [deque() for _ in range(4)]
    # for i in range(n):
    #     c[nums[i] - 1].append(i)

    # res = 0
    # for num in range(1, 5):
    #     while idx < n and c[num]:
    #         print('c', c)
    #         if nums[idx] == num:
    #             c[num - 1].popleft()
    #             idx += 1
    #         else:
    #             c[nums[idx] - 1].popleft()
    #             c[nums[idx] - 1].appendleft(c[num - 1].popleft())
    #             res += 1
    #             idx += 1
    
    print(res)


for testcase in range(1):
    solve(testcase)