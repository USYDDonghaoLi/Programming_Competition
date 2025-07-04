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
#dfs - stack#

def solve():
    n = II()
    nums = LII()

    mp = Counter(nums)

    res = 0
    
    for num in mp:
        #print('num', num)
        l, r = 0, 0
        tmp = defaultdict(int)
        M = 0
        flag = -1
        ans = 0

        while r < n:
            while r < n and nums[r] != num:
                tmp[nums[r]] += 1
                if tmp[nums[r]] > M:
                    M = tmp[nums[r]]
                    flag = nums[r]
                r += 1

            d = r - l
            if M > d // 2:
                ans -= M - (d - M)
                tmp = defaultdict(int)
                tmp[flag] = M - (d - M)
                M = M - (d - M)
            else:
                if d & 1:
                    ans -= 1
                tmp = defaultdict(int)
                M = 0
                flag = -1

            while r < n and nums[r] == num:
                ans += 1
                if tmp[flag]:
                    tmp[flag] = max(0, tmp[flag] - 1)
                    M = max(0, M - 1)
                r += 1
            l = r
        
        print('na', num, ans)
        res = max(res, ans)
    print(res)
            
for _ in range(II()):solve()