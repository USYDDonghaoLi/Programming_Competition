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

RANDOM = getrandbits(32)
 
class Wrapper(int):
    def __init__(self, x):
        int.__init__(x)
 
    def __hash__(self):
        return super(Wrapper, self).__hash__() ^ RANDOM

def solve(testcase):
    s = I()
    n = len(s)
    c = Counter(s)

    A = ['' for _ in range(n)]
    B = ['' for _ in range(n)]
    Aidx, Bidx = 0, 0
    res = 'z' * n

    rest = []
    for char in sorted(list(c.keys())):
        # print('char', char, c[char])
        while c[char] >= 2:
            A[Aidx] = B[Bidx] = B[n - 1 - Aidx] = A[n - 1 - Bidx] = char
            Aidx += 1
            Bidx += 1
            c[char] -= 2
        # print('AB', A, B)
        if c[char]:
            rest.append(char)
        if len(rest) == 2:
            A[Aidx] = B[n - 1 - Aidx] = rest.pop()
            B[Bidx] = A[n - 1 - Bidx] = rest.pop()
            c[A[Aidx]] -= 1
            c[B[Bidx]] -= 1
            Aidx += 1
            Bidx += 1
        if len(rest) == 1:
            AA, BB = A[:], B[:]
            AAidx = Aidx
            cc = {i : c[i] for i in c if c[i]}
            # print('cc', cc)
            i = 0
            KEYS = sorted(list(cc.keys()))
            BB[Aidx] = AA[n - 1 - Aidx] = KEYS[0]
            cc[KEYS[0]] -= 1
            while AAidx < n and AA[AAidx] == '':
                while i < len(KEYS) and not cc[KEYS[i]]:
                    i += 1
                # print(AA, BB, AAidx, n - 1 - AAidx, KEYS, i)
                AA[AAidx] = BB[n - 1 - AAidx] = KEYS[i]
                cc[KEYS[i]] -= 1
                AAidx += 1
            # print('AABB', AA, BB)
            res = min(res, max(''.join(AA), ''.join(BB)))
    
    if len(rest):
        # print(Aidx, Bidx)
        A[Aidx] = B[Bidx] = rest.pop()

    res = min(res, max(''.join(A), ''.join(B)))
    
    print(res)

for testcase in range(II()):
    solve(testcase)