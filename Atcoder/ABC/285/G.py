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
函数结尾要写yield None
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

class DinicWithLowerBound:
    """
    使用方法:
      初始化
       mf = Dinic(n, S, T)
       ※ n为包含（虚拟）源点，汇点的点的个数
          给出S（虚拟源点）,T（虚拟汇点）的编号
 
      添加边
       仅给出S,T以及原始图的顶点间的边即可
       mf.add_link(from, to, capacity)
       mf.add_bound_link(from, to, lower_bound, capacity)
 
      求解最大流
       mf.max_flow()
    """
 
    def __init__(self, n: int, S: int, T: int):
        self.n = n
        self.S = S
        self.T = T
        self.links = [[] for _ in range(n)]
        # links[u] = [ [ v, capacity, index of rev-edge in links[v], is_original_edge ], ]
 
    def add_link(self, from_: int, to: int, capacity: int) -> None:
        fwd = [to, capacity, len(self.links[to]), True]
        bwd = [from_, 0, len(self.links[from_]), False]
        self.links[from_].append(fwd)
        self.links[to].append(bwd)
 
    def add_bounded_link(self, from_: int, to: int, lower_bound: int, capacity: int) -> None:
        assert capacity >= lower_bound
        if lower_bound > 0:
            self.add_link(self.S, to, lower_bound)
            self.add_link(from_, self.T, lower_bound)
        if capacity > lower_bound:
            self.add_link(from_, to, capacity - lower_bound)
 
    def bfs(self, s: int, t: int) -> bool:
        links = self.links
        INF = 1 << 60
        self.level = level = [INF] * self.n
        level[s] = 0
        q = deque([s])
        lim_level = 1 << 60
        while q:
            u = q.popleft()
            if level[u] >= lim_level:
                break
            nd = level[u] + 1
            for to, cap, _, _ in links[u]:
                if cap > 0 and level[to] == INF:
                    level[to] = nd
                    q.append(to)
                    if to == t:
                        lim_level = nd
        return level[t] != INF
 
    def dfs(self, s: int, t: int) -> int:
        links = self.links
        level = self.level
        progress = self.progress
        link_counts = self.link_counts
        # 逆から進めた方が速くなることが多いらしい
        stack = [t]
 
        while stack:
            u = stack[-1]
            if u == s:
                break
            for i in range(progress[u], link_counts[u]):
                progress[u] = i
                to, _, rev, _ = links[u][i]
                if level[u] <= level[to] or progress[to] >= link_counts[to]:
                    continue
                _, cap, _, _ = links[to][rev]
                if cap == 0 or progress[to] >= link_counts[to]:
                    continue
                stack.append(to)
                break
            else:
                progress[u] += 1
                stack.pop()
        else:
            return 0
 
        f = 1 << 60
        fwd_links = []
        bwd_links = []
        stack.pop()
        for u in stack:
            to, _, rev, _ = link = links[u][progress[u]]
            _, cap, _, _ = rev_link = links[to][rev]
            f = min(f, cap)
            fwd_links.append(rev_link)
            bwd_links.append(link)
 
        for link in fwd_links:
            link[1] -= f
 
        for link in bwd_links:
            link[1] += f
 
        return f
 
    def _max_flow(self, s: int, t: int) -> int:
        flow = 0
        while self.bfs(s, t):
            self.progress = [0] * self.n
            current_flow = 1  # Anything > 0 is ok
            while current_flow > 0:
                current_flow = self.dfs(s, t)
                flow += current_flow
        return flow
 
    def max_flow(self, s: int, t: int) -> int:
        self.link_counts = list(map(len, self.links))
        self._max_flow(self.S, self.T)
        self._max_flow(self.S, t)
        self._max_flow(s, self.T)
        result = self._max_flow(s, t)
        if not self.check_lower_bound():
            return -1
        return result
 
    def exists_fulfill_flow(self, s: int, t: int) -> bool:
        self.add_link(t, s, 1 << 60)
        self.link_counts = list(map(len, self.links))
        self._max_flow(self.S, self.T)
        return self.check_lower_bound()
 
    def check_lower_bound(self) -> bool:
        for _, cap, _, is_orig in self.links[self.S]:
            if is_orig and cap > 0:
                return False
        for to, _, rev, is_orig in self.links[self.T]:
            if is_orig:
                continue
            _, cap, _, _ = self.links[to][rev]
            if cap > 0:
                return False
        return True
 
    def cut_edges(self, s: int):
        """ max_flowしたあと、最小カットにおいてカットすべき辺を復元する """
        q = [s]
        reachable = [0] * self.n
        reachable[s] = 1
        while q:
            v = q.pop()
            for to, cap, _, _ in self.links[v]:
                if cap == 0 or reachable[to]:
                    continue
                reachable[to] = 1
                q.append(to)
        edges = []
        for v in range(self.n):
            if reachable[v] == 0:
                continue
            for to, cap, _, is_orig in self.links[v]:
                if is_orig and reachable[to] == 0:
                    edges.append((v, to))
        return edges

d = ((1, 0), (0, 1), (-1, 0), (0, -1))

def solve(testcase):
    n, m = MI()
    grid = [I() for _ in range(n)]

    s = n * m
    t = s + 1
    S = t + 1
    T = S + 1
    def id(x, y):
        return x * m + y

    MF = DinicWithLowerBound(n * m + 4, S, T)

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1':
                continue
            
            if i + j & 1:
                if grid[i][j] == '2':
                    MF.add_bounded_link(id(i, j), t, 1, 1)
                else:
                    MF.add_link(id(i, j), t, 1)
            else:
                if grid[i][j] == '2':
                    MF.add_bounded_link(s, id(i, j), 1, 1)
                else:
                    MF.add_link(s, id(i, j), 1)
                
                for dx, dy in d:
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] != '1':
                        MF.add_link(id(i, j), id(nx, ny), 1)
    
    res = MF.exists_fulfill_flow(s, t)
    if res:
        print('Yes')
    else:
        print('No')

for testcase in range(1):
    solve(testcase)