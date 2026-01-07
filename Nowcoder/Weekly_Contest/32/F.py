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

# RANDOM = getrandbits(32, seed = 19981220)
 
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





# @TIME
def solve(testcase):
    n, m = MI()
    grid = [I() for _ in range(n)]

    @lru_cache(None)
    def encode(s):
        res = 0
        for c in s:
            res *= 3
            if c == 'r':
                pass
            elif c == 'e':
                res += 1
            else:
                res += 2
        return res

    @lru_cache(None)
    def decode(num):
        string = ''
        for _ in range(n):
            t = num % 3
            if t == 0:
                string += 'r'
            elif t == 1:
                string += 'e'
            else:
                string += 'd'
            num //= 3
        return string[::-1]

    @lru_cache(None)
    def check(num1, num2):
        for _ in range(n):
            if num1 % 3 == num2 % 3:
                return False
            num1 //= 3
            num2 //= 3
        return True
    
    @lru_cache(None)
    def calc(num1, num2):
        res = 0
        for _ in range(n):
            res += num1 % 3 != num2 % 3
            num1 //= 3
            num2 //= 3
        return res
    
    
    availables = []
    for state in range(3 ** n):
        string = decode(state)
        # print(state, string)
        for i in range(1, n):
            if string[i] == string[i - 1]:
                break
        else:
            availables.append(state)
    # print('avail', availables)
    
    dp = [0 for _ in range(3 ** n)]
    for j in range(m):
        string = ''
        for i in range(n):
            string += grid[i][j]
        init = encode(string)
        newdp = [inf for _ in range(3 ** n)]
        for state1 in availables:
            for state2 in availables:
                if check(state1, state2):
                    newdp[state2] = min(newdp[state2], dp[state1] + calc(init, state2))
        dp = newdp

    print(min(dp))



for testcase in range(1):
    solve(testcase)