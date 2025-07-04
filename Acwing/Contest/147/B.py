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

'''
手写栈防止recursion limit
注意要用yield 不要用return
函数结尾要写yield None
'''
from types import GeneratorType
def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc

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

# @TIME
def solve(testcase):
    s = I()
    n = len(s)
    S = set()
    
    mp = defaultdict(lambda: defaultdict(bool))
    
    @bootstrap
    def search(idx, suf):
        if suf in mp[idx]:
            yield None
        # print('NO', idx, suf)
        if len(suf) <= 1:
            mp[idx][suf] = False
            yield None
        if idx + 1 == n:
            mp[idx][suf] = False
            yield None
        if idx == n:
            mp[idx][suf] = True
            yield None
        if idx > n:
            mp[idx][suf] = False
            yield None
            
        if len(suf) == 2:
            if idx + 3 <= n and s[idx: idx + 3] not in mp[idx + 3]:
                yield search(idx + 3, s[idx: idx + 3])
            if idx + 2 <= n and s[idx: idx + 2] not in mp[idx + 2]:
                yield search(idx + 2, s[idx: idx + 2])
            mp[idx][suf] = bool((False or mp[idx + 3][s[idx: idx + 3]]) or (mp[idx + 2][s[idx: idx + 2]] and s[idx: idx + 2] != suf))
        else:
            if idx + 3 <= n and s[idx: idx + 2] not in mp[idx + 2]:
                yield search(idx + 2, s[idx: idx + 2])
            if idx + 2 <= n and s[idx: idx + 3] not in mp[idx + 3]:
                yield search(idx + 3, s[idx: idx + 3])
            mp[idx][suf] = bool(False or mp[idx + 2][s[idx: idx + 2]] or (mp[idx + 3][s[idx: idx + 3]] and s[idx: idx + 3] != suf))
        
        # print(idx, suf, mp[idx][suf])
        
        yield None
            
    def check(idx):
        if idx + 2 <= n:
            search(idx + 2, s[idx: idx + 2])
            if mp[idx + 2][s[idx: idx + 2]]:
                # print(s[idx: idx + 2])
                S.add(s[idx: idx + 2])
        if idx + 3 <= n:
            search(idx + 3, s[idx: idx + 3])
            if mp[idx + 3][s[idx: idx + 3]]:
                # print(s[idx: idx + 3])
                S.add(s[idx: idx + 3])
    
    # print('n', n)
    for i in range(n - 1, 4, -1):
        check(i)
        # print(i, 2, mp[i + 2][s[i:i + 2]], s[i: i + 2])
        # print(i, 3, mp[i + 3][s[i:i + 3]], s[i: i + 3])
    
    # print('mp', mp[7], mp[9])
    
    print(len(S))
    for suf in sorted(list(S)):
        print(suf)

for testcase in range(1):
    solve(testcase)