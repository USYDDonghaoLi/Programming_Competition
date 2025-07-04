# '''
# Hala Madrid!
# https://www.zhihu.com/people/li-dong-hao-78-74
# '''

# import sys
# import os
# from io import BytesIO, IOBase
# BUFSIZE = 8192
# class FastIO(IOBase):
#     newlines = 0
#     def __init__(self, file):
#         self._fd = file.fileno()
#         self.buffer = BytesIO()
#         self.writable = "x" in file.mode or "r" not in file.mode
#         self.write = self.buffer.write if self.writable else None
#     def read(self):
#         while True:
#             b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
#             if not b:
#                 break
#             ptr = self.buffer.tell()
#             self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
#         self.newlines = 0
#         return self.buffer.read()
#     def readline(self):
#         while self.newlines == 0:
#             b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
#             self.newlines = b.count(b"\n") + (not b)
#             ptr = self.buffer.tell()
#             self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
#         self.newlines -= 1
#         return self.buffer.readline()
#     def flush(self):
#         if self.writable:
#             os.write(self._fd, self.buffer.getvalue())
#             self.buffer.truncate(0), self.buffer.seek(0)
# class IOWrapper(IOBase):
#     def __init__(self, file):
#         self.buffer = FastIO(file)
#         self.flush = self.buffer.flush
#         self.writable = self.buffer.writable
#         self.write = lambda s: self.buffer.write(s.encode("ascii"))
#         self.read = lambda: self.buffer.read().decode("ascii")
#         self.readline = lambda: self.buffer.readline().decode("ascii")
# sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
# input = lambda: sys.stdin.readline().rstrip("\r\n")

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

# @TIME
def solve(testcase):
    n, m = MI()
    
    A = []
    B = []
    mpa = defaultdict(list)
    mpb = defaultdict(list)
    
    S = set()
    SA, SB = set(), set()
    
    for _ in range(n):
        s = I()
        A.append(s)
        mpa[s[0]].append(s)
        S.add(s[0])
        SA.add(s[0])
    
    for _ in range(m):
        s = I()
        B.append(s)
        mpb[s[0]].append(s)
        S.add(s[0])
        SB.add(s[0])
    
    chars = sorted(list(S))
    k = len(chars)
    
    def calc(arra, arrb, lasta, lastb):
        nn, mm = len(arra), len(arrb)
        cura = lasta
        curb = lastb
        statea = [False for _ in range(nn)]
        stateb = [False for _ in range(mm)]
        
        idxa, idxb = nn - 1, mm - 1
        while idxa >= 0 and idxb >= 0:
            s, t = arra[idxa], arrb[idxb]
            if s >= t:
                statea[idxa] = not curb
                cura |= statea[idxa]
                idxa -= 1
                
            else:
                stateb[idxb] = not cura
                curb |= stateb[idxb]
                idxb -= 1
        
        while idxa >= 0:
            statea[idxa] = not curb
            cura |= statea[idxa]
            idxa -= 1
        
        while idxb >= 0:
            stateb[idxb] = not cura
            curb |= stateb[idxb]
            idxb -= 1
        
        return statea, stateb, cura, curb
    
    for i in range(k - 1, -1, -1):
        c = chars[i]
        if i == k - 1:
            sa, sb, fa, fb = calc(mpa[c], mpb[c], False, False)
        else:
            nc = chars[i + 1]
            if ord(nc) - ord(c) != 1:
                fa = False
                fb = False
            if nc not in SA:
                fa = False
            if nc not in SB:
                fb = False
            sa, sb, fa, fb = calc(mpa[c], mpb[c], fa, fb)
    
    print('L' if sa[0] else 'Q')
    
    

for testcase in range(1):
    solve(testcase)