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
    n = II()
    nums = LII()

    res = []
    needa = []
    needb = []
    idxodd = []
    idxeven = []
    for i in range(n):
        if nums[i] & 1:
            idxodd.append(i)
        else:
            idxeven.append(i)
        
        if i & 1:
            needa.append(i)
        else:
            needb.append(i)
    k1, k2 = len(needa), len(needb)

    def dfs_1(idx):
        nonlocal k2
        if k2 == idx:
            return

        if needb[idx] <= idxodd[idx]:
            if (needb[idx] ^ idxodd[idx]) & 1:
                for i in range(idxodd[idx] - 2, needb[idx] - 1, -2):
                    res.append(('B', i + 1))
                res.append(('A', needb[idx] + 1))
            else:
                for i in range(idxodd[idx] - 2, needb[idx] - 2, -2):
                    res.append(('B', i + 1))
            dfs_1(idx + 1)
        else:
            dfs_1(idx + 1)
            if (needb[idx] ^ idxodd[idx]) & 1:
                for i in range(idxodd[idx], needb[idx] - 1, 2):
                    res.append(('B', i + 1))
                res.append(('A', needb[idx]))
            else:
                for i in range(idxodd[idx], needb[idx], 2):
                    res.append(('B', i + 1))

    if n & 1:
        dfs_1(0)
        #odd -> b, even -> a#
        even, odd = [], []
        for i in range(k2):
            odd.append([nums[idxodd[i]], needb[i]])
        for i in range(k1):
            even.append([nums[idxeven[i]], needa[i]])
        
        for i in range(1, n + 1, 2):
            idx = -1
            need = i - 1
            iidx = -1
            for j in range(k2):
                if odd[j][0] == i:
                    idx = odd[j][1]
                    iidx = j
                    break
            for k in range(idx - 2, need - 2, -2):
                res.append(('B', k + 1))
                odd[iidx - 1][0], odd[iidx][0] = odd[iidx][0], odd[iidx - 1][0]
        
        for i in range(2, n + 1, 2):
            idx = -1
            need = i - 1
            iidx = -1
            for j in range(k1):
                if even[j][0] == i:
                    idx = even[j][1]
                    iidx = j
                    break
            for k in range(idx - 2, need - 2, -2):
                res.append(('B', k + 1))
                even[iidx - 1][0], even[iidx][0] = even[iidx][0], even[iidx - 1][0]

    else:

        dfs_1(0)
        even, odd = [], []
        for i in range(k2):
            odd.append([nums[idxodd[i]], needb[i]])
        for i in range(k1):
            even.append([nums[idxeven[i]], needa[i]])
        
        for i in range(1, n + 1, 2):
            idx = -1
            need = i - 1
            iidx = -1
            for j in range(k2):
                if odd[j][0] == i:
                    idx = odd[j][1]
                    iidx = j
                    break
            for k in range(idx - 2, need - 2, -2):
                res.append(('B', k + 1))
                odd[iidx - 1][0], odd[iidx][0] = odd[iidx][0], odd[iidx - 1][0]
        
        for i in range(2, n + 1, 2):
            idx = -1
            need = i - 1
            iidx = -1
            for j in range(k1):
                if even[j][0] == i:
                    idx = even[j][1]
                    iidx = j
                    break
            for k in range(idx - 2, need - 2, -2):
                res.append(('B', k + 1))
                even[iidx - 1][0], even[iidx][0] = even[iidx][0], even[iidx - 1][0]


    print(len(res))
    for a, b in res:
        print(a, b)


for _ in range(1):solve()

