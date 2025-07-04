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

#f(a, a) = a#
class SpraseTable:
    def __init__(self, v, op, e) -> None:
        self.n = len(v)
        self.op = op
        self.e = e
        self.v = v
        self.l = (self.n).bit_length()
        self.info=[[e for _ in range(self.l + 1)] for _ in range(self.n)]
        for i in range(self.n):
            self.info[i][0] = self.v[i]
        
        for i in range(1, self.l):
            for j in range(self.n):
                if j + (1 << i) - 1 < self.n:
                    self.info[j][i] = self.op(self.info[j][i - 1], self.info[j + (1 << (i - 1))][i - 1])
    
        self.log2 = [-1 for _ in range(self.n + 1)]
        self.log2[1] = 0
        for i in range(2, self.n + 1):
            self.log2[i] = self.log2[i >> 1] + 1
    
    def query(self, l, r):
        s = self.log2[r - l + 1]
        return self.op(self.info[l][s], self.info[r - (1 << s) + 1][s])

def solve(nums):
    # n = II()
    # nums = LII()
    n = len(nums)
    st = SpraseTable(nums, gcd, 0)
    
    for i in range(n - 2, -1, -1):
        if nums[i] > nums[i + 1]:
            if st.query(0, i) > nums[i + 1]:
                return False
                print('NO')
                return
            l, r = 0, i - 1
            while l < r:
                mid = l + r >> 1
                if st.query(mid, i) <= nums[i + 1]:
                    r = mid
                else:
                    l = mid + 1
            nums[i] = st.query(l, i)
    
    return True
    print('YES')

def solve2(nums):
    # n = II()
    # nums = LII()
    n = len(nums)

    for i in range(n - 2, -1, -1):
        if nums[i] > nums[i + 1]:
            j = i - 1
            while j >= 0 and nums[i] > nums[i + 1]:
                nums[i] = gcd(nums[i], nums[j])
                j -= 1
            if nums[i] > nums[i + 1]:
                return False
                print('NO')
                return
            else:
                for k in range(j + 1, i):
                    nums[k + 1] = gcd(nums[k + 1], nums[k])

    return True    
    print('YES')

for _ in range(10):
    flag = True
    nums = [randint(1, 10 ** 3) * randint(1, 10 ** 3) for _ in range(200)]
    if solve(nums) != solve2(nums):
        flag = False
        print('Failed')
        print(nums)
    
if flag:
    print('Accepted')