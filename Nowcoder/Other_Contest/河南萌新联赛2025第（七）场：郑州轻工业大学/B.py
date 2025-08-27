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

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

# class TrieNode:

#     __slots__ = {'count', 'children'}

#     def __init__(self):
#         self.count = 0
#         self.children = [None, None]

# class Trie:

#     __slots__ = {'root', 'MAX_BIT'}

#     def __init__(self):
#         self.root = TrieNode()
#         self.MAX_BIT = 30

#     def insert(self, num):
#         node = self.root
#         for bit in range(self.MAX_BIT, -1, -1):
#             bitVal = (num >> bit) & 1
#             if node.children[bitVal] is None:
#                 node.children[bitVal] = TrieNode()
#             node = node.children[bitVal]
#             node.count += 1

#     def delete(self, num):
#         node = self.root
#         for bit in range(self.MAX_BIT, -1, -1):
#             bitVal = (num >> bit) & 1
#             if node.children[bitVal] is None:
#                 return  # element does not exist
#             node = node.children[bitVal]
#             node.count -= 1

#     def maxXor(self, num):
#         node = self.root
#         max_xor = 0
#         for bit in range(self.MAX_BIT, -1, -1):
#             bitVal = (num >> bit) & 1
#             if node.children[1 - bitVal] and node.children[1 - bitVal].count > 0:
#                 max_xor |= (1 << bit)
#                 node = node.children[1 - bitVal]
#             else:
#                 node = node.children[bitVal]
#         return max_xor

#     def minXor(self, num):
#         node = self.root
#         min_xor = 0
#         for bit in range(self.MAX_BIT, -1, -1):
#             bitVal = (num >> bit) & 1
#             if node.children[bitVal] and node.children[bitVal].count > 0:
#                 node = node.children[bitVal]
#             else:
#                 min_xor |= (1 << bit)
#                 node = node.children[1 - bitVal]
#         return min_xor
    
#     def countXorLessThan(self, num, limit):
#         node = self.root
#         count = 0
#         for bit in range(self.MAX_BIT, -1, -1):
#             bitVal = (num >> bit) & 1
#             limitBit = (limit >> bit) & 1
#             if limitBit:
#                 if node.children[bitVal] is not None:
#                     count += node.children[bitVal].count
#                 if node.children[1 - bitVal] is not None:
#                     node = node.children[1 - bitVal]
#                 else:
#                     break
#             else:
#                 if node.children[bitVal] is not None:
#                     node = node.children[bitVal]
#                 else:
#                     break
#         return count
    
#     def countXorLessThanEqual(self, num, limit):
#         return self.countXorLessThan(num, limit + 1)

#     def countXorGreaterThan(self, num, limit):
#         total = sum(c.count for c in self.root.children if c is not None)
#         return total - self.countXorLessThanEqual(num, limit)

#     def countXorGreatThanEqual(self, num, limit):
#         total = sum(c.count for c in self.root.children if c is not None)
#         return total - self.countXorLessThan(num, limit)

class Trie:

    def __init__(self, n, mx) -> None:
        '''
        n: 数组长度
        mx: 最大值
        '''
        self.n = n
        self.mx = mx + 1
        self.k = self.mx.bit_length()
        self.LEN = self.n * self.k + 1

        self.zero_side = [-1 for _ in range(self.LEN)]
        self.one_side = [-1 for _ in range(self.LEN)]
        self.counts = [0 for _ in range(self.LEN)]
        self.nxt_node = 1
    
    def insert(self, num):
        node = 0
        for i in range(self.k - 1, -1, -1):
            self.counts[node] += 1
            if num >> i & 1:
                if self.one_side[node] == -1:
                    self.one_side[node] = self.nxt_node
                    self.nxt_node += 1
                node = self.one_side[node]
            else:
                if self.zero_side[node] == -1:
                    self.zero_side[node] = self.nxt_node
                    self.nxt_node += 1
                node = self.zero_side[node]
        self.counts[node] += 1
    
    def delete(self, num):
        node = 0
        for i in range(self.k - 1, -1, -1):
            self.counts[node] -= 1
            if num >> i & 1:
                node = self.one_side[node]
            else:
                node = self.zero_side[node]
    
    def findMaxXor(self, v):
        node = 0
        res = 0
        for i in range(self.k - 1, -1, -1):
            if v >> i & 1:
                if self.zero_side[node] and self.counts[self.zero_side[node]]:
                    node = self.zero_side[node]
                    res |= 1 << i
                else:
                    node = self.one_side[node]
            else:
                if self.one_side[node] and self.counts[self.one_side[node]]:
                    node = self.one_side[node]
                    res |= 1 << i
                else:
                    node = self.zero_side[node]
        return res

    def findMinXor(self, v):
        node = 0
        res = 0
        for i in range(self.k - 1, -1, -1):
            if v >> i & 1:
                if self.one_side[node] and self.counts[self.one_side[node]]:
                    node = self.one_side[node]
                else:
                    node = self.one_side[node]
                    res |= 1 << i
            else:
                if self.zero_side[node] and self.counts[self.zero_side[node]]:
                    node = self.zero_side[node]
                else:
                    node = self.zero_side[node]
                    res |= 1 << i
    
    def countXorLessThan(self, num, limit):
        node = 0
        count = 0
        for i in range(self.k - 1, -1, -1):
            bitVal = (num >> i) & 1
            limitBit = (limit >> i) & 1
            if limitBit:
                if self.zero_side[node] != -1:
                    count += self.counts[self.zero_side[node]]
                node = self.one_side[node] if bitVal == 0 else self.zero_side[node]
            else:
                node = self.zero_side[node] if bitVal == 0 else self.one_side[node]
            if node == -1:
                break
        return count

    def countXorLessThanEqual(self, num, limit):
        return self.countXorLessThan(num, limit + 1)

    def countXorGreaterThan(self, num, limit):
        total = self.counts[0]
        return total - self.countXorLessThanEqual(num, limit)

    def countXorGreaterThanEqual(self, num, limit):
        total = self.counts[0]
        return total - self.countXorLessThan(num, limit)
    
    

# @TIME
def solve(testcase):
    n, k = MI()
    T = Trie(n + 10, 32)

    T.insert(0)

    A = LII()
    cur = 0

    res = 0
    for a in A:
        cur ^= a
        res += T.countXorGreaterThanEqual(cur, k)
        # print(a, T.countXorGreatThanEqual(cur, k))
        T.insert(cur)
    
    print(res)

for testcase in range(1):
    solve(testcase)