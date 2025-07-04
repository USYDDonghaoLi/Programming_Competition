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

def solve():
    n, m = MI()
    A = LII()
    B = LII()
    C = LII()
    D = LII()

    boxes = sorted(zip(C, D))
    chos = sorted(zip(A, B))
    #print('boxes', boxes)
    #print('chos', chos)
    if chos[-1][0] > boxes[-1][0] or chos[-1][1] > boxes[-1][1]:
        print('No')
        return
    
    pqb = []
    pqc = []

    idxb = 0
    temp = boxes[0][0]
    idxc = 0
    while True:
        #print('temp', temp)
        while idxb < m and boxes[idxb][0] == temp:
            heappush(pqb, -boxes[idxb][1])
            idxb += 1
        
        while idxc < n and chos[idxc][0] <= temp:
            heappush(pqc, -chos[idxc][1])
            idxc += 1
        
        #print('b', pqb)
        #print('c', pqc)
        if idxb != m:
            temp = boxes[idxb][0]
        
        pqcc = []
        while True:
            if not pqc:
                break
            while pqc and pqc[0] < pqb[0]:
                heappush(pqcc, heappop(pqc))
            if not pqc:
                break
            heappop(pqb)
            heappop(pqc)
            if not pqb or not pqc:
                break
        
        pqc = pqcc
        
        if idxc == n and idxb == m:
            break
        pqb = []
    
    if pqc:
        print('No')
    else:
        print('Yes')
solve()