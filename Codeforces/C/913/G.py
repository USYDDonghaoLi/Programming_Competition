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

# @TIME
def solve(testcase):
    n = II()
    s = I()
    state = [int(c == '1') for c in s]
    adj = defaultdict(int)
    deg = [0 for _ in range(n)]
    nxt = LII()
    
    for i, v in enumerate(nxt):
        v -= 1
        deg[v] += 1
        adj[i] = v
    
    q = deque()
    for i in range(n):
        if deg[i] == 0:
            q.append(i)
    
    # print('q', q)
    # print('adj', adj)
    
    res = []
    v = [False for _ in range(n)]
    while q:
        cur = q.popleft()
        # print('cur', cur, state[cur], deg)
        v[cur] = True
        if state[cur]:
            res.append(cur)
            state[cur] ^= 1
            state[adj[cur]] ^= 1
        deg[adj[cur]] -= 1
        if not deg[adj[cur]]:
            q.append(adj[cur])
    
    for i in range(n):
        if not v[i]:
            # print('i', i)
            cycle = []
            cycle_state = []
            
            cur = i
            while not v[cur]:
                v[cur] = True
                cycle.append(cur)
                cycle_state.append(state[cur])
                cur = adj[cur]
            
            # print(cycle)
            # print(cycle_state)
            
            if sum(cycle_state) & 1:
                print(-1)
                return
            else:
                ret1, ret2 = [], []
                state1, state2 = cycle_state[:], cycle_state[:]
                
                k = len(cycle)
                for i in range(k):
                    if i == 0 or state1[i]:
                        ret1.append(cycle[i])
                        state1[i] ^= 1
                        state1[(i + 1) % k] ^= 1
                
                for i in range(k):
                    if i != 0 and state2[i]:
                        ret2.append(cycle[i])
                        state2[i] ^= 1
                        state2[(i + 1) % k] ^= 1
                
                # print(state1)
                # print(state2)
                assert sum(state1) == 0
                assert sum(state2) == 0
                
                if len(ret1) < len(ret2):
                    res.extend(ret1)
                else:
                    res.extend(ret2)
    
    print(len(res))
    for i in range(len(res)):
        res[i] += 1
    print(*res)

for testcase in range(II()):
    solve(testcase)