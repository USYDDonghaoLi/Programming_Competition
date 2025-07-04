import sys
import os
from io import BytesIO, IOBase
from tkinter import N
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

def nxt(string):
    
    m = len(string)
    nnxt = [0 for _ in range(m)]
    nnxt[0] = 0
    k = 0
    for i in range(1, m):
        while k > 0 and string[k] != string[i]:
            k = nnxt[k - 1]
        if string[k] == string[i]:
            k += 1
        nnxt[i] = k
    return nnxt, k

def solve():
    s = I()
    n = len(s)
    nnxt, k = nxt(s)
    q = II()
    t = ''

    def judge(kk, i):
        if kk >= n:
            kk -= n
            return t[kk] != t[i]
        else:
            return s[kk] != t[i]
    
    def judge2(kk, i):
        if kk >= n:
            kk -= n
            return t[kk] == t[i]
        else:
            return s[kk] == t[i]

    mp = defaultdict(tuple)

    for _ in range(q):
        t = I()
        m = len(t)
        kk = k
        temp = [0 for _ in range(m)]
        for i in range(m):
            if t[:i + 1] in mp:
                kk = mp[t[:i + 1]]
                temp[i] = kk
                continue
            while kk > 0 and judge(kk, i):
                kk = nnxt[kk - 1] if kk - 1 < n else temp[kk - 1 - n]
            if judge2(kk, i):
                kk += 1
            mp[t[:i + 1]] = kk
            temp[i] = kk
        print(*temp)

for _ in range(1):solve()