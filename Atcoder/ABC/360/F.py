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

# class FenwickTree:
#     def __init__(self, n):
#         self.n = n
#         self.tree = [0 for _ in range(n)]
    
#     def fill(self, a):
#         for i in range(self.n):
#             self.update(i, a[i])

#     def lowbit(self, x):
#         return x & (-x)

#     def update(self, pos, x):
#         while pos < self.n:
#             self.tree[pos] += x
#             pos += self.lowbit(pos)

#     def query(self, pos):
#         to_ret = 0
#         while pos:
#             to_ret += self.tree[pos]
#             pos -= self.lowbit(pos)
#         return to_ret

#     def query_sum(self, l, r):
#         return self.query(r) - self.query(l - 1)

#     def lower_bound(self, val):
#         ret, su = 0, 0
#         for i in reversed(range(self.n.bit_length())):
#             ix = ret + (1 << i)
#             if ix < self.n and su + self.tree[ix] < val:
#                 su += self.tree[ix]
#                 ret += 1 << i
#         return ret
    
#     def upper_bound(self, val):
#         ret, su = 0, 0
#         for i in reversed(range(self.n.bit_length())):
#             ix = ret + (1 << i)
#             if ix < self.n and su + self.tree[ix] <= val:
#                 su += self.tree[ix]
#                 ret += 1 << i
#         return ret

# class SegTree:

#     __slots__ = {'n', 'op', 'e', 'log', 'size', 'd'}

#     def __init__(self, V, OP, E):
#         '''
#         V: 原始数组
#         OP: 维护的运算(min, max, sum...)
#         E: 线段树初值
#         '''
#         self.n = len(V)
#         self.op = OP
#         self.e = E
#         self.log = (self.n - 1).bit_length()
#         self.size = 1 << self.log
#         self.d=[E for _ in range(2*self.size)]
#         for i in range(self.n):
#             self.d[self.size + i] = V[i]
#         for i in range(self.size - 1, 0, -1):
#             self.update(i)

#     def set(self, p, x):
#         assert 0 <= p and p < self.n
#         p += self.size
#         self.d[p] = x
#         for i in range(1, self.log + 1):
#             self.update(p >> i)

#     def get(self, p):
#         assert 0 <= p and p <self.n
#         return self.d[p + self.size]

#     def prod(self, l ,r):
#         #[l, r)
#         assert 0 <= l and l <= r and r <= self.n
#         sml = self.e
#         smr = self.e
#         l += self.size
#         r += self.size

#         while(l < r):
#             if (l & 1):
#                 sml = self.op(sml, self.d[l])
#                 l += 1
#             if (r & 1):
#                 smr = self.op(self.d[r - 1], smr)
#                 r -= 1
#             l >>= 1
#             r >>= 1
#         return self.op(sml, smr)

#     def all_prod(self):
#         return self.d[1]

#     def max_right(self, l, f):
#         assert 0 <= l and l <= self.n
#         assert f(self.e)
#         if l == self.n:
#             return self.n
#         l += self.size
#         sm = self.e
#         while(1):
#             while(l % 2 == 0):
#                 l >>= 1
#             if not(f(self.op(sm, self.d[l]))):
#                 while(l < self.size):
#                     l = 2 * l
#                     if f(self.op(sm, self.d[l])):
#                         sm = self.op(sm, self.d[l])
#                         l += 1
#                 return l - self.size
#             sm = self.op(sm,self.d[l])
#             l += 1
#             if (l & -l) == l:
#                 break
#         return self.n
#     def min_left(self, r, f):
#         assert 0 <= r and r < self.n
#         assert f(self.e)
#         if r == 0:
#             return 0
#         r += self.size
#         sm = self.e
#         while(1):
#             r -= 1
#             while(r > 1 & (r % 2)):
#                 r >>= 1
#             if not(f(self.op(self.d[r], sm))):
#                 while(r < self.size):
#                     r = (2 * r + 1)
#                     if f(self.op(self.d[r], sm)):
#                         sm=self.op(self.d[r], sm)
#                         r -= 1
#                 return r + 1 - self.size
#             sm = self.op(self.d[r] ,sm)
#             if (r & -r) == r:
#                 break
#         return 0

#     def update(self, k):
#         self.d[k] = self.op(self.d[2 * k], self.d[2 * k + 1])
        
#     def __str__(self):
#         return str([self.get(i) for i in range(self.n)])

# class SegmentTree:
#     def __init__(self, data):
#         n = len(data)
#         self.n = n
#         self.tree = [None] * (4 * n)
#         self.build(0, 0, n - 1, data)

#     def build(self, node, start, end, data):
#         if start == end:
#             self.tree[node] = {
#                 'sum': data[start],
#                 'prefix_sum': max(0, data[start]),
#                 'suffix_sum': max(0, data[start]),
#                 'max_sum': max(0, data[start])
#             }
#         else:
#             mid = (start + end) // 2
#             left_child = 2 * node + 1
#             right_child = 2 * node + 2
#             self.build(left_child, start, mid, data)
#             self.build(right_child, mid + 1, end, data)
#             self.tree[node] = self.merge(self.tree[left_child], self.tree[right_child])

#     def merge(self, left, right):
#         total_sum = left['sum'] + right['sum']
#         prefix_sum = max(left['prefix_sum'], left['sum'] + right['prefix_sum'])
#         suffix_sum = max(right['suffix_sum'], right['sum'] + left['suffix_sum'])
#         max_sum = max(left['max_sum'], right['max_sum'], left['suffix_sum'] + right['prefix_sum'])
#         return {
#             'sum': total_sum,
#             'prefix_sum': prefix_sum,
#             'suffix_sum': suffix_sum,
#             'max_sum': max_sum
#         }

#     def update(self, idx, value, node=0, start=0, end=None):
#         if end is None:
#             end = self.n - 1
#         if start == end:
#             self.tree[node] = {
#                 'sum': value,
#                 'prefix_sum': max(0, value),
#                 'suffix_sum': max(0, value),
#                 'max_sum': max(0, value)
#             }
#         else:
#             mid = (start + end) // 2
#             left_child = 2 * node + 1
#             right_child = 2 * node + 2
#             if start <= idx <= mid:
#                 self.update(idx, value, left_child, start, mid)
#             else:
#                 self.update(idx, value, right_child, mid + 1, end)
#             self.tree[node] = self.merge(self.tree[left_child], self.tree[right_child])

#     def query(self, l, r, node=0, start=0, end=None):
#         if end is None:
#             end = self.n - 1
#         if l > end or r < start:
#             return {
#                 'sum': 0,
#                 'prefix_sum': 0,
#                 'suffix_sum': 0,
#                 'max_sum': 0
#             }
#         if l <= start and end <= r:
#             return self.tree[node]
#         mid = (start + end) // 2
#         left_child = 2 * node + 1
#         right_child = 2 * node + 2
#         left_result = self.query(l, r, left_child, start, mid)
#         right_result = self.query(l, r, right_child, mid + 1, end)
#         return self.merge(left_result, right_result)

#     def get_max_prefix_sum(self, l, r):
#         return self.query(l, r)['prefix_sum']

# # 使用示例：
# data = [1, 2, -3, 4, 5, -6, 7, 8]
# seg_tree = SegmentTree(data)
# print(seg_tree.get_max_prefix_sum(0, len(data) - 1))  # 查询最大前缀和
# seg_tree.update(3, 10)  # 将位置3的值更新为10
# print(seg_tree.get_max_prefix_sum(0, len(data) - 1))  # 更新后查询最大前缀和

class LazySegmentTree():
    
    __slots__ = ['n', 'log', 'size', 'd', 'lz', 'e', 'op', 'mapping', 'composition', 'identity']
    
    def _update(self, k):
        self.d[k] = self.op(self.d[2 * k], self.d[2 * k + 1])
    
    def _all_apply(self, k, f):
        self.d[k] = self.mapping(f, self.d[k])
        if (k < self.size):
            self.lz[k] = self.composition(f, self.lz[k])
    
    def _push(self, k):
        self._all_apply(2 * k, self.lz[k])
        self._all_apply(2 * k + 1, self.lz[k])
        self.lz[k] = self.identity
        
    def __init__(self, V, OP, E, MAPPING, COMPOSITION, ID):
        self.n = len(V)
        self.log = (self.n - 1).bit_length()
        self.size = 1 << self.log
        self.d = [E for i in range(2 * self.size)]
        self.lz = [ID for i in range(self.size)]
        self.e = E
        self.op = OP
        self.mapping = MAPPING
        self.composition = COMPOSITION
        self.identity = ID
        for i in range(self.n):
            self.d[self.size + i] = V[i]
            
        for i in range(self.size - 1, 0, -1):
            self._update(i)
            
    def set(self, p, x):
        assert 0 <= p and p < self.n
        p += self.size
        for i in range(self.log, 0, -1):
            self._push(p >> i)
        self.d[p] = x
        for i in range(1,self.log + 1):
            self._update(p >> i)
            
    def get(self, p):
        assert 0 <= p and p < self.n
        p += self.size
        for i in range(self.log, 0, -1):
            self._push(p >> i)
        return self.d[p]
    
    def prod(self, l, r):
        assert 0 <= l and l <= r and r <= self.n
        if l == r:
            return self.e
        l += self.size
        r += self.size
        for i in range(self.log, 0, -1):
            if (((l >> i) << i) != l):
                self._push(l >> i)
            if (((r >> i) <<i) != r):
                self._push(r >> i)
        sml, smr = self.e, self.e
        while (l < r):
            if l & 1:
                sml = self.op(sml, self.d[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self.op(self.d[r], smr)
            l >>= 1
            r >>= 1
        return self.op(sml, smr)
    
    def all_prod(self):
        return self.d[1]
    
    def apply_point(self, p, f):
        assert 0 <= p and p < self.n
        p += self.size
        for i in range(self.log, 0, -1):
            self._push(p >> i)
        self.d[p] = self.mapping(f, self.d[p])
        for i in range(1, self.log + 1):
            self._update(p >> i)
            
    def apply(self, l, r, f):
        assert 0 <= l and l <= r and r <= self.n
        if l == r:
            return
        l += self.size
        r += self.size
        for i in range(self.log, 0, -1):
            if (((l >> i) << i) != l):
                self._push(l >> i)
            if (((r >> i) << i) != r):
                self._push((r - 1) >> i)
        l2, r2 = l, r
        while (l < r):
            if (l & 1):
                self._all_apply(l, f)
                l += 1
            if (r & 1):
                r -= 1
                self._all_apply(r, f)
            l >>= 1
            r >>= 1
        l, r = l2, r2
        for i in range(1, self.log + 1):
            if (((l >> i) << i) != l):
                self._update(l >> i)
            if (((r >> i) << i) != r):
                self._update((r - 1) >> i)
                
    def max_right(self, l, g):
        assert 0 <= l and l <= self.n
        assert g(self.e)
        if l == self.n:
            return self.n
        l += self.size
        for i in range(self.log, 0, -1):
            self._push(l >> i)
        sm = self.e
        while (1):
            while (l % 2 == 0):
                l >>= 1
            if not(g(self.op(sm, self.d[l]))):
                while(l < self.size):
                    self._push(l)
                    l = (2 * l)
                    if (g(self.op(sm,self.d[l]))):
                        sm = self.op(sm,self.d[l])
                        l += 1
                return l - self.size
            sm = self.op(sm, self.d[l])
            l += 1
            if (l & -l) == l:break
        return self.n
    
    def min_left(self,r,g):
        assert 0 <= r and r <= self.n
        assert g(self.e)
        if r == 0:
            return 0
        r += self.size
        for i in range(self.log, 0, -1):
            self._push((r - 1) >> i)
        sm = self.e
        while (1):
            r -= 1
            while(r > 1 and (r % 2)):
                r >>= 1
            if not(g(self.op(self.d[r], sm))):
                while (r < self.size):
                    self._push(r)
                    r = (2 * r + 1)
                    if g(self.op(self.d[r], sm)):
                        sm = self.op(self.d[r], sm)
                        r -= 1
                return r + 1 - self.size
            sm = self.op(self.d[r], sm)
            if (r & -r) == r:
                break
        return 0

# @TIME
def solve(testcase):
    n = II()
    S = set([0, 10 ** 9])
    intervals = []
    
    for _ in range(n):
        l, r = MI()
        S.add(l + 1)
        S.add(r)
        S.add(r + 1)
        intervals.append([l, r])
    
    lst = sorted(list(S))
    d2 = {i: v for i, v in enumerate(lst)}
    d = {v: i for i, v in enumerate(lst)}
    
    m = len(d)

    events = []
    
    for l, r in intervals:
        events.append((l + 1, 1, d[r + 1], m))
        events.append((r, -1, d[r + 1], m))
        
        if l + 1 < r:
            events.append((0, 1, d[l + 1], d[r]))
            events.append((l, -1, d[l + 1], d[r]))
    
    events.sort()
    # print(events)
    
    sg = LazySegmentTree(
        [0 for _ in range(m)],
        lambda x, y: x if x > y else y,
        0,
        lambda x, y: x + y,
        lambda x, y: x + y,
        0
    )
    
    M = 0
    l, r = 0, 1

    n = len(events)
    # print(m)
    # print('events', events)
    
    left, right = 0, 0
    while right < n:
        while right < n and events[right][0] == events[left][0]:
            # print(events[right][2], events[right][3], m)
            sg.apply(events[right][2], events[right][3], events[right][1])
            right += 1
        
        val = sg.all_prod()
        if val > M:
            M = val
            l = events[left][0]
            idx = sg.max_right(
                0, 
                lambda x: x < M
            )
            r = d2[idx]
        
        left = right
    
    print(l, r)

for testcase in range(1):
    solve(testcase)