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

seed(19981220)
RANDOM = getrandbits(64)
 
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
    n, k = MI()
    nums = LII()
    
    mp = defaultdict(list)
    
    for num in nums:
        mp[(num % k) ^ RANDOM].append(num // k)
        
    if n & 1:
        
        res = 0
    
        flag = False
        for val in mp:
            mp[val].sort()
            m = len(mp[val])
            if m & 1:
                if flag:
                    print(-1)
                    return
                else:
                    flag = True
                    if m == 1:
                        continue
                    front = []
                    back = []
                    for i in range(0, m, 2):
                        try:
                            front.append(mp[val][i + 1] - mp[val][i])
                        except:
                            break
                    for i in range(1, m, 2):
                        try:
                            back.append(mp[val][i + 1] - mp[val][i])
                        except:
                            break
                    
                    l = len(front)
                    for i in range(1, l):
                        front[i] += front[i - 1]
                    l = len(back)
                    for i in range(l - 2, -1, -1):
                        back[i] += back[i + 1]
                    
                    add = min(front[-1], back[0])
                    for i in range(1, l):
                        add = min(add, back[i] + front[i - 1])
                    res += add
            else:
                for i in range(0, m, 2):
                    res += mp[val][i + 1] - mp[val][i]
        
        print(res)
    
    else:
        
        res = 0
        
        for val in mp:
            mp[val].sort()
            m = len(mp[val])
            if m & 1:
                print(-1)
                return
            else:
                for i in range(0, m, 2):
                    res += mp[val][i + 1] - mp[val][i]
        
        print(res)
        

for testcase in range(II()):
    solve(testcase)