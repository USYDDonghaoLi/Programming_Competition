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
pw = dict()
for i in range(0, 20):
    pw[2 ** i] = i

def solve():
    n = II()
    adj = defaultdict(lambda : defaultdict(list))
    st = [[-1 for _ in range(20)] for _ in range(n + 1)]
    red = [0 for _ in range(n + 1)]
    blue = [0 for _ in range(n + 1)]
    d = [0 for _ in range(n + 1)]
    
    for i in range(2, n + 1):
        p, r, b = MI()
        adj[p][i] = [r, b]
        st[i][0] = p

    q = deque()
    q.append(1)
    res = [0 for _ in range(n + 1)]

    while q:
        k = len(q)
        for _ in range(k):
            cur = q.popleft()
            for e in adj[cur]:
                red[e] = red[cur] + adj[cur][e][0]
                blue[e] = blue[cur] + adj[cur][e][1]
                d[e] = d[cur] + 1
                q.append(e)
    
    for j in range(1, 20):
        for i in range(1, n + 1):
            st[i][j] = st[st[i][j - 1]][j - 1]
    
    def judge(now, depth, target):
        #print('target', target)
        source = now
        up = depth - target
        while up:
            lb = up & (-up)
            d = pw[lb]
            now = st[now][d]
            up -= lb
        return blue[now] <= red[source]

    def calc(i):
        l, r = 1, d[i] + 1
        while l < r:
            mid = l + r >> 1
            if judge(i, d[i], mid):
                l = mid + 1
            else:
                r = mid
        return l - 1

    res = [-1 for _ in range(n + 1)]
    for i in range(2, n + 1):
        res[i] = calc(i)
    
    print(*res[2:])
for _ in range(II()):solve()