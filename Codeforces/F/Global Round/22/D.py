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
from math import log, gcd
#dfs - stack#
#check top!#

def solve():
    n = II()
    nums = LII()
    adj = defaultdict(list)
    u, d = n, 0

    for i in range(n):
        adj[nums[i]].append(i + 1)
        if i + 1 > nums[i]:
            u = min(u, i + 1)
            d = max(d, nums[i])
        else:
            u = min(u, nums[i])
            d = max(d, i + 1)

    q = deque()
    arr = []
    if adj[0]:
        flag = 0
        print(d)
        q.append(0)
        while q:
            cur = q.popleft()
            s = None
            arr.append(cur)
            if flag == 0:
                for e in adj[cur][::-1]:
                    if len(adj[e]):
                        s = e
                        continue
                    q.append(e)
                if s:
                    q.append(s)
            else:
                for e in adj[cur]:
                    if len(adj[e]):
                        s = e
                        continue
                    q.append(e)
                if s:
                    q.append(s)
            flag ^= 1
        print(*arr[1:])

    else:
        print(d)
        q.append(n + 1)
        flag = 1
        while q:
            cur = q.popleft()
            s = None
            arr.append(cur)
            if flag == 0:
                for e in adj[cur][::-1]:
                    if len(adj[e]):
                        s = e
                        continue
                    q.append(e)
                if s:
                    q.append(s)
            else:
                for e in adj[cur]:
                    if len(adj[e]):
                        s = e
                        continue
                    q.append(e)
                if s:
                    q.append(s)
            flag ^= 1
        print(*arr[1:])

for _ in range(II()):solve()