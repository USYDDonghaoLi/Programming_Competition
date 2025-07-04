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
    n, m, q = MI()

    elevators = defaultdict(list)
    allelevators = list()
    S = set()

    for _ in range(m):
        a, b, c = MI()
        elevators[a].append([b, c])

    def merge(arr):
        arr.sort()
        res = []
        for i in range(len(arr)):
            low, high = arr[i]
            while res and res[-1][1] >= low:
                ll, rr = res.pop()
                low = min(low, ll)
                high = max(high, rr)
            res.append([low, high])
        
        for low, high in res:
            S.add(low)
            S.add(high)

        return res     
    
    for i in range(1, n + 1):
        elevators[i] = merge(elevators[i])
        allelevators.extend(elevators[i])
        temp = list()
        for low, high in elevators[i]:
            temp.append(low)
            temp.append(high)
        elevators[i] = temp
    
    allelevators.sort()
    mergeallelevatrors = merge(allelevators)
    stages = list()
    for low, high in mergeallelevatrors:
        stages.append(low)
        stages.append(high)

    ss = sorted(S)
    mp = {s : i for i, s in enumerate(ss)}
    k = len(S)

    dp = [[-1 for _ in range(k)] for _ in range(20)]
    for low, high in allelevators:
        low, high = mp[low], mp[high]
        dp[0][low] = max(dp[0][low], high)
    
    for i in range(1, k):
        dp[0][i] = max(dp[0][i], dp[0][i - 1])
    
    for i in range(1, 20):
        for j in range(k):
            dp[i][j] = dp[i - 1][dp[i - 1][j]]

    for _ in range(q):
        x, y, z, w = MI()
        if y == w:
            print(0 if x == z else 1)
            continue

        if y > w:
            x, z = z, x
            y, w = w, y
        
        lowerbound = bisect_right(stages, y)
        upperbound = bisect_left(stages, w)
        
        if lowerbound != upperbound or not lowerbound & 1:
            print(-1)
            continue

        ans = w - y
        idx = bisect_right(elevators[x], y)
        if idx & 1:
            y = elevators[x][idx]
            y = mp[y]
        else:
            y = bisect_right(ss, y) - 1
        
        idx = bisect_left(elevators[z], w)
        if idx & 1:
            w = elevators[z][idx - 1]
            w = mp[w]
        else:
            w = bisect_left(ss, w)
        
        if w <= y:
            if x != z:
                ans += 1
            print(ans)
            continue

        for i in range(19, -1, -1):
            if dp[i][y] < w:
                ans += 1 << i
                y = dp[i][y]
        
        ans += 2
        print(ans)
solve()