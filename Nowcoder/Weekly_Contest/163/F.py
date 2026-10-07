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

class FenwickTree:
    """
    树状数组（Fenwick Tree / Binary Indexed Tree）。
    支持单点修改和前缀和查询，都在 O(log n) 时间内完成。
    """
    
    def __init__(self, n: int):
        """
        初始化树状数组。
        Args:
            n: 数组大小
        """
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed
    
    def _lowbit(self, x: int) -> int:
        """
        获取 x 的最低有效位（2 的幂）。
        Args:
            x: 正整数
        Returns:
            x 的最低有效位的值
        """
        return x & (-x)

    def build(self, arr: list) -> None:
        """
        用数组初始化树状数组。
        Args:
            arr: 输入数组（0-indexed），长度为 n
        """
        for i in range(len(arr)):
            self.update(i + 1, arr[i])

    def update(self, pos: int, delta: int) -> None:
        """
        将位置 pos（1-indexed）的值增加 delta。
        Args:
            pos: 位置（1-indexed）
            delta: 增量
        """
        while pos <= self.n:
            self.tree[pos] += delta
            pos += self._lowbit(pos)

    def query(self, pos: int) -> int:
        """
        查询前 pos 个元素的和（1-indexed）。
        Args:
            pos: 位置（1-indexed），查询 [1, pos] 的和
        Returns:
            前 pos 个元素的和
        """
        result = 0
        while pos > 0:
            result += self.tree[pos]
            pos -= self._lowbit(pos)
        return result

    def range_query(self, left: int, right: int) -> int:
        """
        查询区间 [left, right] 的和（1-indexed）。
        Args:
            left: 左端点（1-indexed）
            right: 右端点（1-indexed）
        Returns:
            区间和
        """
        return self.query(right) - self.query(left - 1)

    def lower_bound(self, target: int) -> int:
        """
        在树状数组中进行二分查找，找最小的 pos 使得 query(pos) >= target。
        前提：所有元素非负且累积和单调递增。
        Args:
            target: 目标值
        Returns:
            满足条件的最小位置（1-indexed），若不存在返回 n+1
        """
        pos, cum_sum = 0, 0
        for i in range(self.n.bit_length() - 1, -1, -1):
            next_pos = pos + (1 << i)
            if next_pos <= self.n and cum_sum + self.tree[next_pos] < target:
                cum_sum += self.tree[next_pos]
                pos = next_pos
        return pos + 1
    
    def upper_bound(self, target: int) -> int:
        """
        在树状数组中进行二分查找，找最小的 pos 使得 query(pos) > target。
        前提：所有元素非负且累积和单调递增。
        Args:
            target: 目标值
        Returns:
            满足条件的最小位置（1-indexed），若不存在返回 n+1
        """
        pos, cum_sum = 0, 0
        for i in range(self.n.bit_length() - 1, -1, -1):
            next_pos = pos + (1 << i)
            if next_pos <= self.n and cum_sum + self.tree[next_pos] <= target:
                cum_sum += self.tree[next_pos]
                pos = next_pos
        return pos + 1

# def test_fenwick_tree():
#     """测试树状数组"""
#     # 基本测试
#     ft = FenwickTree(5)
#     ft.build([1, 2, 3, 4, 5])
#     assert ft.query(3) == 6, "query(3) should be 1+2+3=6"
#     print("✓ test_build_query passed")
    
#     # 更新测试
#     ft.update(2, 5)  # arr[2] += 5，即变成 2+5=7
#     assert ft.query(3) == 11, "After update, query(3) should be 1+7+3=11"
#     print("✓ test_update passed")
    
#     # 区间查询
#     ft2 = FenwickTree(5)
#     ft2.build([1, 2, 3, 4, 5])
#     assert ft2.range_query(2, 4) == 9, "range_query(2,4) should be 2+3+4=9"
#     print("✓ test_range_query passed")


# if __name__ == "__main__":
#     test_fenwick_tree()
#     print("\n所有 Fenwick Tree 测试通过！✓")


# @TIME
def solve(testcase):
    n, k, t = MI()
    A = [0] + LII()

    vis = [False for _ in range(n + 1)]
    B = [[] for _ in range(n + 1)]

    for i in range(1, n + 1):
        if vis[i]:
            continue
        mn = i
        mx = i
        x = i

        while not vis[x]:
            vis[x] = True
            if x < mn:
                mn = x
            if x > mx:
                mx = x
            x = A[x]

        B[mx].append(mn)

    diff = [0 for _ in range(n + 2)]

    for mx in range(1, n + 1):
        for mn in B[mx]:
            if mx > mn:
                diff[mn] += 1
                diff[mx] -= 1

    C = [0 for _ in range(n + 1)]
    for c in range(1, n + 1):
        C[c] = C[c - 1] + diff[c]

    ft = FenwickTree(n)
    cnt = 0
    D = [0 for _ in range(n + 1)]
    idx = -1
    res = 0

    for r in range(1, n + 1):
        for mn in B[r]:
            ft.update(mn, 1)
            cnt += 1

        if t == 0:
            rm = r
        else:
            if cnt < t:
                continue

            tmp = ft.lower_bound(cnt - t + 1)
            rm = tmp if tmp < r else r

        target = k - C[r]
        while idx < rm - 1:
            idx += 1
            D[C[idx]] += 1

        if 0 <= target <= n:
            res += D[target]

    print(res)

for testcase in range(1):
    solve(testcase)