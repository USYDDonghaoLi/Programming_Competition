'''
Hala Madrid!
https://www.zhihu.com/people/li-dong-hao-78-74
'''

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
from math import log, gcd, sqrt, ceil

dirs = [[-1,0],[0,1],[1,0],[0,-1],[0,0]]

# 定义炮弹
class Bullet:
    def __init__(self, period, speed, dir, x, y):
        self.period = period
        self.speed = speed
        self.dir = dir
        self.x = x
        self.y = y

def init_bullets(bullets, m, n, times, g, having):
    for bullet in bullets:
        for j in range(0, times+1, bullet.period):
            dist = 1
            while True:
                dx = bullet.x + dirs[bullet.dir][0] * dist
                dy = bullet.y + dirs[bullet.dir][1] * dist
                t = j+dist//bullet.speed
                if dx<0 or dx>m or dy<0 or dy>n or g[dx][dy]==1 or t > times:
                    break
                if dist % bullet.speed == 0:
                    having[dx][dy][t] = 1
                dist += 1


def bfs(m, n, times, g, having):
    q = deque()
    q.append((0, 0, 0))
    visited = [[[False for _ in range(times + 1)] for _ in range(n + 1)] for _ in range(m + 1)]
    visited[0][0][0] = True

    while q:
        x, y, step = q.popleft()
        if step > times:
            return -1
        if x == m and y == n:
            return step

        for dx, dy in dirs:
            nx, ny, nstep = x + dx, y + dy, step + 1
            if nstep > times:
                continue
            if 0 <= nx <= m and 0 <= ny <= n and g[nx][ny]==0 and having[nx][ny][nstep]==0 and not visited[nx][ny][nstep]:
                visited[nx][ny][nstep] = True
                q.append((nx, ny, nstep))

    return -1


while True:
    try:
        m, n, k, times = MI()
        g = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        having = [[[0 for _ in range(times + 1)] for _ in range(n + 1)] for _ in range(m + 1)]

        bullets = []
        for _ in range(k):
            op, period, speed, x, y = LI()
            period, speed, x, y = map(int, [period, speed, x, y])
            dir = {'N': 0, 'E': 1, 'S': 2, 'W': 3}[op]
            bullets.append(Bullet(period, speed, dir, x, y))
            g[x][y] = 1

        init_bullets(bullets, m, n, times, g, having)
        res = bfs(m, n, times, g, having)

        print(res if res != -1 else 'Bad luck!')

    except EOFError:
        break