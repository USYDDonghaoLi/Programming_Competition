"""
Fast IO（快速输入输出）

用于竞争编程的高性能 I/O 模板。

特点：
- 使用缓冲减少系统调用
- 快速读写整数和字符串
- 适合输入输出量大的题目

使用：
- input() / readline() 读取
- 自定义输出函数
"""

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

from collections import defaultdict


class UnionFind:
    """
    并查集（Union-Find）数据结构。
    支持快速的 find 和 union 操作，使用路径压缩和按大小的启发式合并。
    时间复杂度：近乎 O(1)（带路径压缩）
    """
    
    def __init__(self, n: int):
        """
        初始化并查集。
        Args:
            n: 元素个数
        """
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.L = [i for i in range(n)]
        self.R = [i for i in range(n)]
        self.n = n
        self.component_count = n
    
    def find(self, x: int) -> int:
        """
        查找元素 x 所在的集合代表（根节点）。
        使用迭代路径压缩优化，避免递归深度问题。
        时间复杂度：O(α(n))，其中 α 是反阿克曼函数
        Args:
            x: 元素
        Returns:
            x 所在集合的根节点
        """
        # 第一步：找到根节点
        root = self.parent[x]
        x_copy = root
        while root != self.parent[root]:
            root = self.parent[root]
        
        # 第二步：路径压缩，将 x_copy 到根的所有节点直接指向根
        while x_copy != root:
            self.parent[x_copy], x_copy = root, self.parent[x_copy]
        
        return root
    
    def union(self, x: int, y: int) -> bool:
        """
        合并包含 x 和 y 的两个集合。
        使用按大小的启发式合并（小树并入大树）。
        Args:
            x: 第一个元素
            y: 第二个元素
        Returns:
            True 表示成功合并（两个元素不在同一集合），False 表示它们已在同一集合
        """
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        
        # 将较小的树并入较大的树
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        self.L[root_x] = fmin(self.L[root_x], self.L[root_y])
        self.R[root_x] = fmax(self.R[root_x], self.R[root_y])
        self.component_count -= 1
        return True

    def is_connected(self, x: int, y: int) -> bool:
        """
        检查元素 x 和 y 是否在同一集合中。
        Args:
            x: 第一个元素
            y: 第二个元素
        Returns:
            True 表示连通，False 表示不连通
        """
        return self.find(x) == self.find(y)

    def get_component_size(self, x: int) -> int:
        """
        获取包含元素 x 的连通分量大小。
        Args:
            x: 元素
        Returns:
            连通分量中的元素个数
        """
        return self.size[self.find(x)]

    def get_members(self, x: int) -> list:
        """
        获取与元素 x 在同一集合中的所有元素。
        Args:
            x: 元素
        Returns:
            所有属于同一集合的元素列表
        """
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]
    
    def get_roots(self) -> list:
        """
        获取所有集合的根节点。
        Returns:
            根节点列表
        """
        return [i for i, x in enumerate(self.parent) if self.find(i) == i]
    
    def get_component_count(self) -> int:
        """
        获取当前的连通分量个数。
        Returns:
            连通分量个数
        """
        return self.component_count
    
    def get_all_components(self) -> dict:
        """
        获取所有连通分量及其成员。
        Returns:
            字典，key 为根节点，value 为该分量中的所有元素列表
        """
        components = defaultdict(list)
        for element in range(self.n):
            root = self.find(element)
            components[root].append(element)
        return dict(components)

# @TIME
def solve(testcase):
    n, m = MI()

    A = LII()
    B = [0]
    for a in A:
        B.append(B[-1] + a)
    
    uf = UnionFind(n)

    for _ in range(m):
        ops = LII()
        op = ops[0]

        if op == 1:

            l, r = ops[1] - 1, ops[2] - 1
            lrt = uf.find(l)
            rrt = uf.find(r)
            
            cur = lrt

            while cur <= rrt:
                uf.union(cur, lrt)
                right = uf.R[cur]
                if right == n - 1:
                    break
                cur = uf.find(right + 1)

        else:

            idx = ops[1] - 1
            rt = uf.find(idx)

            left, right = uf.L[rt], uf.R[rt]
            LEN = right - left + 1

            print((B[right + 1] - B[left]) / LEN)


for testcase in range(1):
    solve(testcase)