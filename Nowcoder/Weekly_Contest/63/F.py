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
def LGMI():
    return list(map(lambda x: int(x) - 1, input().split()))

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

class LinearBase:

    def __init__(self, nums) -> None:
        """
        初始化线性基。
        作用：把原数组中的所有数构造成一个可以高效处理异或相关问题的线性基。
        使用方法：
            lb = LinearBase([1, 2, 4, 7])
        """
        self.n = len(nums)
        self.nums = nums
        self.bases = {}  # pivot_bit -> (value, index_mask)
        self.max_bit = 0
        self._next_idx = 0
        for idx, num in enumerate(nums):
            self.add(num, idx)

    def add(self, x, idx=None):
        """
        向线性基中插入一个数。
        作用：把一个新元素加入基中，保持线性基的性质不变。
        使用方法：
            lb.add(10)
            lb.add(13, idx=2)  # 额外记录该元素对应的原数组下标
        """
        if idx is None:
            idx = self._next_idx
            self._next_idx += 1
        else:
            self._next_idx = max(self._next_idx, idx + 1)
        self.n = max(self.n, self._next_idx)
        cur = x
        mask = 1 << idx
        for bit in range(cur.bit_length() - 1, -1, -1):
            if (cur >> bit) & 1:
                if bit not in self.bases:
                    self.bases[bit] = (cur, mask)
                    self.max_bit = max(self.max_bit, bit + 1)
                    return True
                cur ^= self.bases[bit][0]
                mask ^= self.bases[bit][1]
        return False

    def _reduce(self, x):
        """
        内部辅助函数：把 x 化简到线性基表示下。
        作用：判断 x 是否能由当前线性基表示的元素异或得到，并顺便得到对应的系数掩码。
        通常不直接调用，供 can_make / get_indices 使用。
        """
        cur = x
        coeff_mask = 0
        for bit in range(self.max_bit - 1, -1, -1):
            if (cur >> bit) & 1:
                if bit not in self.bases:
                    return cur, None
                cur ^= self.bases[bit][0]
                coeff_mask ^= self.bases[bit][1]
        return cur, coeff_mask

    def can_make(self, x):
        """
        判断某个值能不能由原数组中的若干元素异或得到。
        作用：用于快速判断是否存在一个子集，使其异或结果等于 x。
        使用方法：
            lb.can_make(5)  # True / False
        """
        return self.get_indices(x) is not None

    def get_indices(self, x):
        """
        返回能异或出 x 的原数组下标集合。
        作用：不仅判断可行，还能给出具体用到了哪些原数组下标。
        使用方法：
            lb.get_indices(5)  # 返回例如 [0, 2]
            若不可达，则返回 None。
        """
        rem, coeff_mask = self._reduce(x)
        if rem != 0 or coeff_mask is None:
            return None
        return [i for i in range(self.n) if (coeff_mask >> i) & 1]

    def kthlargestxor(self, k):
        """
        求第 k 大的异或值（从 0 开始计数）。
        作用：在一个集合中，求所有子集异或结果按大小排序后的第 k 个结果。
        使用方法：
            lb.kthlargestxor(1)  # 第 1 大的异或值
            lb.kthlargestxor(3)  # 第 3 大的异或值
        """
        ans = 0
        k -= 1
        basis_values = [value for _, (value, _) in sorted(self.bases.items())]
        for base in basis_values:
            if k & 1:
                ans ^= base
            k >>= 1

        if k == 0:
            return ans
        else:
            return -1

class LinearBase2:

    def __init__(self, n) -> None:
        """
        另一种常见的线性基写法，按位维护基底数组。
        作用：适合做基础的线性基判断和插入操作。
        使用方法：
            lb = LinearBase2(31)
        """
        self.n = n
        self.base = [0 for _ in range(n)]
    
    def reduce(self, x):
        """
        消元，判断 x 是否能被当前基底线性表示。
        作用：用于检查某个数是否能由已有基底表示出来。
        使用方法：
            lb.reduce(10)
        """
        for i in range(self.n - 1, -1, -1):
            if x >> i & 1:
                x ^= self.base[i]
        return x

    def add(self, x):
        """
        向当前线性基中插入一个数。
        作用：维护基底，使其保持线性无关。
        使用方法：
            lb.add(5)
        """
        x = self.reduce(x)
        if x:
            for i in range(self.n - 1, -1, -1):
                if (x >> i) & 1:
                    self.base[i] = x
                    return True
        return False
    
    def check(self, x):
        """
        判断某个数是否能由当前线性基表示出来。
        作用：常用于快速判断一个值是否在当前集合的线性空间中。
        使用方法：
            lb.check(10)
        """
        return self.reduce(x) == 0

# @TIME
def solve(testcase):
    n = II()
    s = I()

    target = 0
    for i, c in enumerate(s):
        if c == '0':
            target |= 1 << i
    
    X = defaultdict(int)
    Y = defaultdict(int)

    A = []

    for i in range(n):
        x, y = MI()
        X[x] |= 1 << i
        Y[y] |= 1 << i
        A.append((x, y))
    
    LB = LinearBase([])

    for i in range(n):
        x, y = A[i]
        LB.add(X[x] | Y[y], i)
        # print(X[x] | Y[y])
    
    # print('target', target)
    res = LB.get_indices(target)
    # print('res', res)

    if not res:
        print(-1)
    else:
        m = len(res)
        print(m)

        for i in range(m):
            res[i] += 1
        
        print(*res)

for testcase in range(1):
    solve(testcase)