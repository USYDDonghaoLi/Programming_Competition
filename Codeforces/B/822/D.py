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
    nums = [0] + LII() + [0]

    if k == 1 or k == n:
        print('YES')
        return
    
    curl = curr = nums[k]
    print(curl, curr)
    flagl = flagr = True
    lM, rM = 0, 0
    #linfo = []
    #lneed, learn = 0, 0
    for i in range(k - 1, 0, -1):
        # if nums[i] < 0:
        #     learn += nums[i]
        #     lneed = max(-learn, lneed)
        # else:
        #     learn += nums[i]
        curl += nums[i]
        if curl < 0:
            flagl = False
        if flagl:
            lM= max(lM, curl)
        #linfo.append((lneed, learn))
    #linfo = linfo[::-1]

    #rinfo = []
    #rneed, rearn = 0, 0
    for i in range(k + 1, n + 1):
        curr += nums[i]
        if curr < 0:
            flagr = False
        if flagr:
            rM = max(rM, curr)
        #rinfo.append((rneed, rearn))

    if flagl and curl >= 0:
        print('YES')
        return
    if flagr and curr >= 0:
        print('YES')
        return
    
    print('lrM', lM, rM)

    flagl = flagr = True
    for i in range(k - 1, 0, -1):
        rM += nums[i]
        if rM < 0:
            flagl = False
            break

    for i in range(k + 1, n + 1):
        lM += nums[i]
        if lM < 0:
            flagr = False
            break
    
    print('YES' if flagl or flagr else 'NO')

for _ in range(II()):solve()

