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

class Node:
    
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.tail = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, node):
        node.prev = self.tail
        node.next = None
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self.size += 1

    def pop_front(self):
        if not self.head:
            return None
        node = self.head
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return node

    def remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self.size -= 1

# @TIME
def solve(testcase):
    n, k, q = MI()
    
    memo = LinkedList()
    mp = defaultdict(set)
    freq = defaultdict(int)
    fridge = set()
    pq = []

    def Delete(ID):
        for node in mp[ID]:
            memo.remove_node(node)
        mp[ID].clear()
        freq[ID] = 0
    
    def Add(x):
        node = Node(x)
        memo.append(node)
        mp[x].add(node)
        freq[x] += 1

        if x in fridge:
            heappush(pq, (freq[x], x))
        
        res = -1
        while memo.size > k:
            node = memo.pop_front()
            if node:
                val = node.val
                mp[val].remove(node)
                freq[val] -= 1

                if val in fridge:
                    heappush(pq, (freq[val], val))
                
                if freq[val] == 0 and val in fridge:
                    fridge.remove(val)
                    res = val
        return res
    
    res = []

    for _ in range(q):
        op, x = MI()
        ans = -1

        if op == 1:
            if x not in fridge:
                while len(fridge) >= n:
                    flag = False
                    while pq:
                        f, ID = heappop(pq)
                        if freq[ID] == f and ID in fridge:
                            ans = ID
                            fridge.remove(ans)
                            Delete(ans)
                            flag = True
                            break
                    if not flag:
                        break

            if x not in fridge:
                fridge.add(x)

            eaten = Add(x)
            if ans == -1:
                ans = eaten
        else:
            if x not in fridge:
                ans = -1
            else:
                ans = x
                fridge.remove(x)
                Delete(x)
        
        res.append(ans)
    
    print(*res)
    
    if not fridge:
        print(-1)
        return
    
    fridge = list(fridge)
    fridge.sort(key = lambda x: (-freq[x], -x))
    print(' '.join(map(str, fridge)))


for testcase in range(1):
    solve(testcase)