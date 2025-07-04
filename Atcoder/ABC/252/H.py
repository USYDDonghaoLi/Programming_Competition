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
sys.setrecursionlimit(2 ** 31 - 1)

def solve():
    N, C, K = MI()
    V = [[] for _ in range(C)]

    for _ in range(N):
        c, v = MI()
        V[c - 1].append(v)
    V.sort(key = len)

    P = [[0], [0]]
    for a in V[::-1]:
        flag = len(P[0]) > len(P[1])
        new_arr = []
        for v in a:
            for x in P[flag]:
                new_arr.append(v ^ x)
        P[flag] = new_arr
    
    ans = 0
    P = [(P[0], P[1])]
    for B in range(59, -1, -1):
        arr = []
        cnt = 0
        for a, b in P:
            aa = [[], []]
            bb = [[], []]
            for x in a:
                aa[(x >> B) & 1].append(x)
            for x in b:
                bb[(x >> B) & 1].append(x)
            arr.append((aa,bb))
            cnt += len(aa[0]) * len(bb[1]) + len(aa[1]) * len(bb[0])
        print('B=', B, 'P=', P, 'aa', aa, 'bb', bb, 'arr', arr, 'cnt', cnt)
        
        if cnt < K:
            K -= cnt
            P = []
            for aa, bb in arr:
                if len(aa[0]) and len(bb[0]):
                    P.append((aa[0], bb[0]))
                if len(aa[1]) and len(bb[1]):
                    P.append((aa[1], bb[1]))
        
        else:
            ans += 1 << B
            P = []
            for aa, bb in arr:
                if len(aa[0]) and len(bb[1]):
                    P.append((aa[0], bb[1]))
                if len(aa[1]) and len(bb[0]):
                    P.append((aa[1], bb[0]))
    print(ans)
solve()