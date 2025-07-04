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

'''
手写栈防止recursion limit
注意要用yield 不要用return
'''
from types import GeneratorType
def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc

'''
max(***), mp可能为空 -> error
'''


def solve():
    n, m = MI()
    def id(x, y):
        return x * m + y
    grid = [0 for _ in range(n * m)]
    Mrow = [float('-inf') for _ in range(n)]
    mrow = [float('inf') for _ in range(n)]
    #adj =  defaultdict(set)
    adj = defaultdict(list)
    intervals = []
    degree = [0 for _ in range(m * n + m)]
    for i in range(n):
        line = LII()
        for j in range(m):
            grid[id(i, j)] = line[j]
            if line[j]:
                Mrow[i] = max(Mrow[i], line[j])
                mrow[i] = min(mrow[i], line[j])
        if mrow[i] != float('inf') and Mrow != float('-inf'):
            intervals.append((mrow[i], Mrow[i]))
    
    #判断每行的最大值最小值是否相交#
    intervals.sort()
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            print('No')
            return
    
    #虚拟节点的下标#
    index = m - 1
    mp = defaultdict(int)
    for i in range(n):
        tmp = index
        for j in range(m):
            if not grid[id(i, j)]:
                continue
            if mp[grid[id(i, j)]] <= tmp:
                index += 1
                mp[grid[id(i, j)]] = index
            adj[mp[grid[id(i, j)]]].append(j)
        
        idxs = [j for j in range(m)]
        idxs.sort(key = lambda x: grid[id(i, x)])
        for j in range(m - 1):
            if not grid[id(i, idxs[j])]:
                continue
            if grid[id(i, idxs[j])] < grid[id(i, idxs[j + 1])]:
                newpoint = mp[id(i, idxs[j - 1])]
                for k in range(j, -1, -1):
                    if grid[id(i, idxs[k])] != grid[id(i, idxs[j])]:
                        break
                    adj[idxs[k]].append(newpoint)
        
    for i in range(m, index + 1):
        for e in adj[i]:
            degree[e] += 1
    
    q = deque()
    cnt = 0
    for i in range(index + 1):
        if not degree[i]:
            q.append(i)
    
    while q:
        cur = q.popleft()
        cnt += 1
        for e in adj[cur]:
            degree[e] -= 1
            if not degree[e]:
                q.append(e)

    if cnt == index + 1:
        print('Yes')
    else:
        print('No')

for _ in range(1):solve()