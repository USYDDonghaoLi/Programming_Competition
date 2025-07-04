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
from random import *
#dfs - stack#

# def test(n):
#     arr = []
#     for _ in range(n):
#         arr.append(randint(-5, 5))
#     print('arr', arr)
#     for i in range(n):
#         for j in range(i + 1, n):
#             for k in range(j + 1, n):
#                 if arr[i] + arr[j] + arr[k] not in arr:
#                     return arr
#     print('Right', end = ' ')
#     return arr

def solve():
    # #n = II()
    # n = randint(5, 20)
    # nums = test(n)
    n = II()
    nums = LII()
    if 0 in nums:
        lst = []
        for num in nums:
            if num:
                lst.append(num)
        if len(lst) < 2:
            print('YES')
        elif len(lst) == 2:
            if lst[0] + lst[1] == 0:
                print('YES')
            else:
                print('NO')
        else:
            print('NO')
    else:
        if n > 4:
            print('NO')
        elif n == 4:
            nums.sort()
            if nums[0] + nums[3] == 0 and nums[1] + nums[2] == 0:
                print('YES')
                return
            print('NO')
        else:
            for i in range(3):
                for j in range(i + 1, 3):
                    if nums[i] + nums[j] == 0:
                        print('YES')
                        return
            print('NO')
for _ in range(II()):solve()