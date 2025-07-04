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
#dfs - stack#
#check top!#

def solve():
    n, k = MI()
    nums = LII()
    k -= 1

    cur = nums[k]
    M = nums[k]
    l, r = k - 1, k + 1
    while r < n:
        while r < n and nums[r] + cur >= 0:
            cur += nums[r]
            M = max(M, cur)
            #print('1r', nums[r], cur, M)
            r += 1
        if r == n:
            break

        t = M
        tt = M
        d = 0
        idx = -1
        while l >= 0 and t + nums[l] >= 0:
            t += nums[l]
            M = max(M, t)
            #print('Mtt', M, tt)
            if M - tt > d:
                d = M - tt
                idx = l
            l -= 1
            #print('1l', l, t, d, M, idx)
        #print('lr', l, r, idx)
        if l == -1 or idx == -1:
            break
        if nums[r] + d + cur < 0:
            break
        else:
            #print('idx', idx)
            cur = cur + d - nums[r]
            l = idx - 1
            r += 1
    
    #print(l, r)
    if r == n or l == -1:
        print('YES')
        return
    
    nums = nums[::-1]
    cur = nums[n - 1 - k]
    M = cur
    l, r = n - 1 - k - 1, n - 1 - k + 1
    while r < n:
        while r < n and nums[r] + cur >= 0:
            cur += nums[r]
            M = max(M, cur)
            #print('2r', nums[r], cur, M)
            r += 1
        if r == n:
            break

        t = M
        tt = M
        d = 0
        idx = -1
        while l >= 0 and t + nums[l] >= 0:
            t += nums[l]
            M = max(M, t)
            if M - tt > d:
                d = M - tt
                idx = l
            #print('2l', l, d, M, tt)
            l -= 1
        #print('lr', l, r)
        if l == -1 or idx == -1:
            break
        if nums[r] + d + cur < 0:
            break
        else:
            cur = cur + d - nums[r]
            l = idx - 1
            r += 1
    #print('2lr', l, r)
    if r == n or l == -1:
        print('YES')
        return
    
    print('NO')
            

for _ in range(II()):solve()

