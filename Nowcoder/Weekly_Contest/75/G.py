'''
Hala Madrid!
https://github.com/USYDDonghaoLi/Programming_Competition
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


def LGMI():
    return list(map(lambda x: int(x) - 1, input().split()))


# ------------------------------FastIO---------------------------------

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
from time import *
from random import *
from math import log, gcd, sqrt, ceil

from types import GeneratorType


def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)

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


inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y


class LCA:
    def __init__(self, depth, parent):
        self.n = len(parent)
        self.num = self.n.bit_length()
        self.depth = depth
        self.parent = [[-1] * self.n for _ in range(self.num)]
        self.parent[0] = parent[:]

        for k in range(self.num - 1):
            for u in range(self.n):
                p = self.parent[k][u]
                if p != -1:
                    self.parent[k + 1][u] = self.parent[k][p]

    def get_lca(self, u, v):
        if self.depth[u] > self.depth[v]:
            u, v = v, u

        d = self.depth[v] - self.depth[u]
        for k in range(self.num):
            if d >> k & 1:
                v = self.parent[k][v]

        if u == v:
            return u

        for k in range(self.num - 1, -1, -1):
            if self.parent[k][u] != self.parent[k][v]:
                u = self.parent[k][u]
                v = self.parent[k][v]

        return self.parent[0][u]


def solve():
    n, q = MI()
    s = [1 if c == 'R' else 0 for c in I()]

    A = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = GMI()
        A[u].append(v)
        A[v].append(u)

    parent = [-1] * n
    depth = [0] * n
    order = []

    @bootstrap
    def dfs(u, fa):
        for v in A[u]:
            if v == fa:
                continue

            parent[v] = u
            depth[v] = depth[u] + 1
            order.append(v)
            yield dfs(v, u)

        yield

    dfs(0, -1)

    sz = [1] * n
    for u in reversed(order):
        sz[parent[u]] += sz[u]

    cols = [-1] * n
    cols[0] = 0

    for u in order:
        if sz[u] & 1:
            cols[u] = cols[parent[u]]
        else:
            cols[u] = cols[parent[u]] ^ 1

    for u in range(n):
        same = sum(cols[u] == cols[v] for v in A[u])
        if same != 1:
            print('\n'.join('-1' for _ in range(q)))
            return

    diff = [cols[u] ^ s[u] for u in range(n)]
    diff_r = [cols[u] ^ 1 for u in range(n)]
    total_diff = sum(diff)

    for u in order:
        diff[u] += diff[parent[u]]
        diff_r[u] += diff_r[parent[u]]

    lca = LCA(depth, parent)
    ans = []

    for _ in range(q):
        u, v = GMI()
        w = lca.get_lca(u, v)
        pw = parent[w]

        path_diff = diff[u] + diff[v] - diff[w]
        path_diff_r = diff_r[u] + diff_r[v] - diff_r[w]
        if pw != -1:
            path_diff -= diff[pw]
            path_diff_r -= diff_r[pw]

        x = total_diff - path_diff + path_diff_r
        ans.append(fmin(x, n - x))

    print('\n'.join(map(str, ans)))


solve()
