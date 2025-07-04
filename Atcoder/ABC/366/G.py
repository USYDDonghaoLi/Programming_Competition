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

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *

# @TIME
def solve(testcase):
    n, m = MI()
    
    adj = [[0 for _ in range(n)] for _ in range(n)]

    for _ in range(m):
        u, v = MI()
        u -= 1
        v -= 1
        adj[u][v] = 1
        adj[v][u] = 1
    
    res = [1 << i for i in range(n)]

    for i in range(n):
        ans = [0 for _ in range(n)]

        mat = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
        for j in range(n):
            for k in range(n):
                if adj[j][k]:
                    if k == i:
                        mat[j][-1] ^= 1
                    else:
                        mat[j][k] = 1
        mat[-1][i] = 1
        mat[-1][-1] = 1

        for col in range(n):
            r = col
            for row in range(col + 1, n + 1):
                if mat[row][col] > mat[r][col]:
                    r = row
            
            mat[r], mat[col] = mat[col], mat[r]

            if mat[col][col]:
                for row in range(n + 1):
                    if row == col:
                        continue
                    else:
                        if mat[row][col]:
                            for col2 in range(col, n + 1):
                                mat[row][col2] = (mat[row][col2] - mat[col][col2]) % 2
            
            # print('mat', i, mat)

        ans = []
        for row in range(n):
            if mat[row][-1]:
                if mat[row][row]:
                    ans.append(mat[row][row])
                else:
                    print('No')
                    return
            else:
                ans.append(0)
        
        # print('ans', i, ans)
        
        for j in range(n):
            if i != j:
                res[j] ^= ans[j] << i
    

    for i in range(n):
        cur = 0
        for j in range(n):
            if adj[i][j]:
                cur ^= res[j]
        if cur:
            print('No')
            return

    print('Yes')
    print(*res)


for testcase in range(1):
    solve(testcase)