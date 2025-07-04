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
#check top!#

def solve():
    n, c = MI()
    orright, andright = [-1 for _ in range(30)], [-1 for _ in range(30)]
    xorlist = [[0 for _ in range(n)] for _ in range(30)]
    BIN = [0 for _ in range(30)]
    for bit in range(30):
        if (c >> bit) & 1:
            BIN[bit] = 1
    ortemp = [-1 for _ in range(30)]
    andtemp = [-1 for _ in range(30)]
    xortemp = [0 for _ in range(30)]
    cnt = [0 for _ in range(30)]

    for i in range(n):
        t, a = MI()
        for bit in range(30):
            if (a >> bit) & 1:
                if t == 2:
                    orright[bit] = i
                if t == 3:
                    xorlist[bit][i] = 1
                    cnt[bit] += 1
            else:
                if t == 1:
                    andright[bit] = i
        
        res = 0
        for bit in range(30):
            temp = BIN[bit]

            if orright[bit] == -1 and andright[bit] == -1:
                xortemp[bit] += cnt[bit]
                temp ^= xortemp[bit] & 1
            else:
                if orright[bit] > andright[bit]:
                    if orright[bit] == i:
                        ortemp[bit] = 1
                        andtemp[bit] = -1
                    else:
                        if t == 1:
                            ortemp[bit] &= (a >> bit) & 1
                        elif t == 2:
                            ortemp[bit] |= (a >> bit) & 1
                        else:
                            ortemp[bit] ^= (a >> bit) & 1
                    temp = ortemp[bit]
                else:
                    if andright[bit] == i:
                        andtemp[bit] = 0
                        ortemp[bit] = -1
                    else:
                        if t == 1:
                            andtemp[bit] &= (a >> bit) & 1
                        elif t == 2:
                            andtemp[bit] |= (a >> bit) & 1
                        else:
                            andtemp[bit] ^= (a >> bit) & 1
                    temp = andtemp[bit]
                
            res ^= temp << bit
        print(res)

for _ in range(1):solve()