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

"""
位运算工具库。

包含：
- 位计数（popcount）：计算整数的二进制表示中 1 的个数
- 子集枚举（enumerate_subsets）：枚举一个掩码的所有非空子集
"""


def popcount(n: int) -> int:
    """
    计算整数 n 的二进制表示中 1 的个数（汉明权重）。
    
    使用 Brian Kernighan 算法的位运算优化版本。
    该实现采用"分治"的思路：
    1. 将相邻的位两两相加（汉明距离）
    2. 递归地将结果合并，最终得到总计数
    
    时间复杂度：O(1)（对 64 位整数）
    
    Args:
        n: 非负整数
        
    Returns:
        n 的二进制表示中 1 的个数
        
    示例:
        >>> popcount(7)        # 0b111 = 3
        3
        >>> popcount(12)       # 0b1100 = 2
        2
        >>> popcount(15)       # 0b1111 = 4
        4
    """
    # 第一步：相邻1位分组计算
    # 0x5555555555555555 = 0101010101...（奇数位掩码）
    c = (n & 0x5555555555555555) + ((n >> 1) & 0x5555555555555555)
    
    # 第二步：2位数据分组计算
    # 0x3333333333333333 = 0011001100...（每4位中的低2位掩码）
    c = (c & 0x3333333333333333) + ((c >> 2) & 0x3333333333333333)
    
    # 第三步：4位数据分组计算
    # 0x0F0F0F0F0F0F0F0F = 00001111...（每8位的低4位掩码）
    c = (c & 0x0F0F0F0F0F0F0F0F) + ((c >> 4) & 0x0F0F0F0F0F0F0F0F)
    
    # 第四步：8位数据分组计算
    c = (c & 0x00FF00FF00FF00FF) + ((c >> 8) & 0x00FF00FF00FF00FF)
    
    # 第五步：16位数据分组计算
    c = (c & 0x0000FFFF0000FFFF) + ((c >> 16) & 0x0000FFFF0000FFFF)
    
    # 第六步：32位数据分组计算（得到最终结果）
    c = (c & 0x00000000FFFFFFFF) + ((c >> 32) & 0x00000000FFFFFFFF)
    
    return c


def popcount_builtin(n: int) -> int:
    """
    使用 Python 内置函数计算位数（推荐）。
    
    Python 3.10+ 内置 int.bit_count()，速度更快。
    对于旧版本，此函数可作为备选。
    
    时间复杂度：O(1)
    
    Args:
        n: 非负整数
        
    Returns:
        n 的二进制表示中 1 的个数
    """
    return bin(n).count('1')


def enumerate_subsets(mask: int) -> list:
    """
    枚举一个掩码的所有非空子集。
    
    子集的定义：S 是 mask 的子集当且仅当 S & mask == S。
    
    算法：
    1. 从 mask 开始
    2. 重复执行 sub = (sub - 1) & mask
    3. 直到 sub == 0（即已枚举所有子集）
    
    时间复杂度：O(3^popcount(mask))
    空间复杂度：O(2^popcount(mask))
    
    Args:
        mask: 掩码（通常是某些位的组合）
        
    Returns:
        mask 的所有非空子集列表
        
    示例:
        >>> enumerate_subsets(0b101)
        [5, 4, 1]  # 0b101, 0b100, 0b001
        
        >>> enumerate_subsets(0b111)
        [7, 6, 5, 4, 3, 2, 1]  # 所有从 7 到 1 的子集
    """
    if mask == 0:
        return []
    
    subsets = []
    sub = mask
    
    while sub > 0:
        subsets.append(sub)
        sub = (sub - 1) & mask  # 得到下一个子集
    
    return subsets


def enumerate_subsets_including_empty(mask: int) -> list:
    """
    枚举一个掩码的所有子集，包括空集。
    
    Args:
        mask: 掩码
        
    Returns:
        mask 的所有子集列表（包括空集）
        
    示例:
        >>> enumerate_subsets_including_empty(0b11)
        [3, 2, 1, 0]  # 0b11, 0b10, 0b01, 0b00
    """
    subsets = []
    sub = mask
    
    while True:
        subsets.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask
    
    return subsets


def is_power_of_two(n: int) -> bool:
    """
    判断一个整数是否是 2 的幂次。
    
    时间复杂度：O(1)
    
    Args:
        n: 正整数
        
    Returns:
        True 如果 n 是 2 的幂次，否则 False
        
    示例:
        >>> is_power_of_two(8)
        True
        >>> is_power_of_two(6)
        False
    """
    return n > 0 and (n & (n - 1)) == 0


def count_trailing_zeros(n: int) -> int:
    """
    计算 n 的二进制表示末尾 0 的个数。
    
    时间复杂度：O(1)
    
    Args:
        n: 正整数
        
    Returns:
        n 的末尾 0 的个数
        
    示例:
        >>> count_trailing_zeros(8)  # 0b1000
        3
        >>> count_trailing_zeros(12)  # 0b1100
        2
    """
    if n == 0:
        return 0
    return (n & -n).bit_length() - 1


def highest_power_of_two(n: int) -> int:
    """
    找到不超过 n 的最大 2 的幂次。
    
    时间复杂度：O(log n)
    
    Args:
        n: 正整数
        
    Returns:
        不超过 n 的最大 2 的幂次
        
    示例:
        >>> highest_power_of_two(10)
        8
        >>> highest_power_of_two(16)
        16
    """
    return 1 << (n.bit_length() - 1)


# @TIME
def solve(testcase):
    n, k = MI()
    A = LII()
    k -= 1

    A.sort(key = lambda x: (popcount(x), x & - x, x))
    print(A[k])

for testcase in range(1):
    solve(testcase)