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

# def TIME(f):

#     def wrap(*args, **kwargs):
#         s = perf_counter()
#         ret = f(*args, **kwargs)
#         e = perf_counter()

#         print(e - s, 'sec')
#         return ret
    
#     return wrap

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *

class UnionFind:
    def __init__(self, n: int):
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.setCount = n
    
    def Find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.Find(self.parent[x])
        return self.parent[x]
    
    def Union(self, x: int, y: int) -> bool:
        root_x = self.Find(x)
        root_y = self.Find(y)
        if root_x == root_y:
            return False
        if self.size[root_x] > self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_x] = root_y
        self.size[root_y] += self.size[root_x]
        self.setCount -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.Find(x) == self.Find(y)

    def members(self, x):
        root = self.Find(x)
        return [i for i in range(self.n) if self.Find(i) == root]
    
    def roots(self):
        return [i for i, x in enumerate(self.parent) if i == x]
    
    def group_count(self):
        return len(self.roots())
    
    def all_group_members(self):
        mp = defaultdict(list)
        for member in range(self.n):
            mp[self.Find(member)].append(member)
        return mp
    
def merge_count(arr, temp_arr, left, mid, right, index_map):
    i, j, k = left, mid + 1, left
    inv_count = 0

    while i <= mid and j <= right:
        # 使用索引映射来比较元素在B中的顺序
        if index_map[arr[i]] <= index_map[arr[j]]:
            temp_arr[k] = arr[i]
            i += 1
        else:
            temp_arr[k] = arr[j]
            j += 1
            inv_count += (mid - i + 1)  # 计算交换次数
        k += 1

    while i <= mid:
        temp_arr[k] = arr[i]
        i += 1
        k += 1

    while j <= right:
        temp_arr[k] = arr[j]
        j += 1
        k += 1

    for i in range(left, right + 1):
        arr[i] = temp_arr[i]

    return inv_count

def merge_sort_count(arr, temp_arr, left, right, index_map):
    inv_count = 0
    if left < right:
        mid = (left + right) // 2

        inv_count += merge_sort_count(arr, temp_arr, left, mid, index_map)
        inv_count += merge_sort_count(arr, temp_arr, mid + 1, right, index_map)
        inv_count += merge_count(arr, temp_arr, left, mid, right, index_map)

    return inv_count

@lru_cache(None)
def calc(A, B):
    A, B = list(A), list(B)
    index_map = {val: idx for idx, val in enumerate(B)}
    temp_arr = [0] * len(A)
    return merge_sort_count(A, temp_arr, 0, len(A) - 1, index_map)


# @TIME
def solve(testcase):
    n, m = MI()
    A = [LII() for _ in range(n)]
    B = [LII() for _ in range(n)]

    # @lru_cache(None)
    # def calc(p):
    #     res = 0
    #     t = len(p)
    #     for i in range(t):
    #         if p[i] > i:

    #     # uf = UnionFind(t)
    #     # for i in range(t):
    #     #     uf.Union(i, p[i])
    #     # for i in range(t):
    #     #     if uf.Find(i) == i:
    #     #         res += uf.size[i] - 1
    #     # return res

    res = float('inf')
    for p1 in permutations([ii for ii in range(n)]):
        newA = [[-1 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                newA[i][j] = A[p1[i]][j]

                for p2 in permutations([jj for jj in range(m)]):
                    newA2 = [[-1 for _ in range(m)] for _ in range(n)]
                    for i2 in range(n):
                        for j2 in range(m):
                            newA2[i2][j2] = newA[i2][p2[j2]]

                    if newA2 == B:
                        # print(p1, p2, calc(p1, (ii for ii in range(n))), calc(p2, (jj for jj in range(m))))
                        res = min(res, calc(p1, (ii for ii in range(n))) + calc(p2, (jj for jj in range(m))))
    
    if res == float('inf'):
        print(-1)
    else:
        print(res)

    # def calc(A):
    #     mpr = defaultdict(list)
    #     mpc = defaultdict(list)
    #     for i in range(n):
    #         for j in range(m):
    #             tmp = []
    #             for k in range(m):
    #                 if j == k:
    #                     continue
    #                 tmp.append(A[i][k])
    #             mpr[A[i][j]].append(sorted(tmp))

    #             tmp = []
    #             for k in range(n):
    #                 if j == k:
    #                     continue
    #                 tmp.append(A[k][j])
    #             mpc[A[i][j]].append(sorted(tmp))
        
    #     for val in mpr:
    #         mpr[val].sort()
    #     for val in mpc:
    #         mpc[val].sort()
        
    #     return mpr, mpc
    
    # mpar, mpac = calc(A)
    # mpbr, mpbc = calc(B)

    # for val in mpar:
    #     if mpar[val] != mpbr[val]:



for testcase in range(1):
    solve(testcase)