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
    n = II()
    ax, ay = GMI()
    bx, by = GMI()

    grid = [[' ' for _ in range(n)] for _ in range(n)]

    for i in range(n):
        word = I()
        for j in range(n):
            grid[i][j] = word[j]
    
    if (ax + bx - bx - by) & 1:
        print(-1)
        return
    #print('grid', grid)
    
    d1 = set()
    d2 = set()
    
    qs = deque()
    ss = set()
    qs.append((ax, ay))
    ss.add((ax, ay))

    qt = deque()
    st = set()
    qt.append((bx, by))
    st.add((bx, by))

    step = 0
    while qs or qt:
        #print('qs', qs)
        #print('qt', qt)
        k = len(qs)
        for _ in range(k):
            x, y = qs.popleft()
            if (x, y) in st:
                print(step)
                return
            curx, cury = x - 1, y + 1
            while 0 <= curx < n and 0 <= cury < n and grid[curx][cury] != '#':
                if (curx, cury) not in d2:
                    d2.add((curx, cury))
                    if (curx, cury) not in ss:
                        qs.append((curx, cury))
                        ss.add((curx, cury))
                curx -= 1
                cury += 1

            curx, cury = x + 1, y - 1
            while 0 <= curx < n and 0 <= cury < n and grid[curx][cury] != '#':
                if (curx, cury) not in d2:
                    d2.add((curx, cury))
                    if (curx, cury) not in ss:
                        qs.append((curx, cury))
                        ss.add((curx, cury))
                curx += 1
                cury -= 1

            curx, cury = x - 1, y - 1
            while 0 <= curx < n and 0 <= cury < n and grid[curx][cury] != '#':
                if (curx, cury) not in d1:
                    d1.add((curx, cury))
                    if (curx, cury) not in ss:
                        qs.append((curx, cury))
                        ss.add((curx, cury))
                curx -= 1
                cury -= 1
            
            curx, cury = x + 1, y + 1
            while 0 <= curx < n and 0 <= cury < n and grid[curx][cury] != '#':
                if (curx, cury) not in d1:
                    d1.add((curx, cury))
                    if (curx, cury) not in ss:
                        qs.append((curx, cury))
                        ss.add((curx, cury))
                curx += 1
                cury += 1
            
        
        step += 1
        #print('qs', qs)
        #print('qt', qt)
        k = len(qt)
        for _ in range(k):
            x, y = qt.popleft()
            if (x, y) in ss:
                print(step)
                return
            curx, cury = x - 1, y + 1
            while 0 <= curx < n and 0 <= cury < n and grid[curx][cury] != '#':
                if (curx, cury) not in d2:
                    d2.add((curx, cury))
                    if (curx, cury) not in st:
                        qt.append((curx, cury))
                        st.add((curx, cury))
                curx -= 1
                cury += 1

            curx, cury = x + 1, y - 1
            while 0 <= curx < n and 0 <= cury < n and grid[curx][cury] != '#':
                if (curx, cury) not in d2:
                    d2.add((curx, cury))
                    if (curx, cury) not in st:
                        qt.append((curx, cury))
                        st.add((curx, cury))
                curx += 1
                cury -= 1

            curx, cury = x - 1, y - 1
            while 0 <= curx < n and 0 <= cury < n and grid[curx][cury] != '#':
                if (curx, cury) not in d1:
                    d1.add((curx, cury))
                    if (curx, cury) not in st:
                        qt.append((curx, cury))
                        st.add((curx, cury))
                curx -= 1
                cury -= 1
            
            curx, cury = x + 1, y + 1
            while 0 <= curx < n and 0 <= cury < n and grid[curx][cury] != '#':
                if (curx, cury) not in d1:
                    d1.add((curx, cury))
                    if (curx, cury) not in st:
                        qt.append((curx, cury))
                        st.add((curx, cury))
                curx += 1
                cury += 1
        step += 1

solve()