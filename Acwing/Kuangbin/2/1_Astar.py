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

def f(state):
    ans = 0
    for i in range(9):
        if state[i] == 'x':
            continue
        else:
            t = int(state[i]) - 1
            ans += abs(i // 3 - t // 3) + abs(i % 3 - t % 3)
    return ans

d = ((-1, 0), (0, 1), (1, 0), (0, -1))
op = 'urdl'

def Astar(start):
    end = '12345678x'
    dist = defaultdict(int)
    prev = defaultdict(tuple)
    pq = []
    dist[start] = 0
    heappush(pq, (f(start), start))

    while pq:
        t = heappop(pq)
        state = t[1]
        if state == end:
            break
        for i in range(9):
            if state[i] == 'x':
                x, y = divmod(i, 3)
                break
        
        source = state
        for i in range(4):
            dx, dy = d[i]
            a, b = x + dx, y + dy
            state = list(state)
            if 0 <= a < 3 and 0 <= b < 3:
                state[a * 3 + b], state[x * 3 + y] = state[x * 3 + y], state[a * 3 + b]
                state = ''.join(state)
                if state not in dist or dist[state] > dist[source] + 1:
                    dist[state] = dist[source] + 1
                    prev[state] = (op[i], source)
                    heappush(pq, (dist[state] + f(state), state))
            state = source
    
    ans = ''
    while end != start:
        ans = prev[end][0] + ans
        end = prev[end][1]
    print(ans)

# @TIME
def solve(testcase):
    start = ''.join(LI())
    idx = start.index('x')
    s = start[:idx] + start[idx + 1:]

    cnt = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if s[i] > s[j]:
                cnt += 1
    if cnt & 1:
        print('unsolvable')
    else:
        Astar(start)

for testcase in range(1):
    solve(testcase)