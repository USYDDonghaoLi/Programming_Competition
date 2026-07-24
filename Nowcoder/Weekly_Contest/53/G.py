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

fmax = lambda x, y: x if x > y else y

def solve():
    n = II()
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = GMI()
        adj[u].append(v)
        adj[v].append(u)

    children = [[] for _ in range(n)]
    down_h = [0] * n   # 子树最大高度
    down_d = [0] * n   # 子树直径
    FA = [-1] * n

    @bootstrap
    def dfs1(u, fa):
        FA[u] = fa
        maxh1 = maxh2 = 0
        max_cd = 0
        for v in adj[u]:
            if v == fa:
                continue
            yield dfs1(v, u)
            children[u].append(v)
            h = down_h[v] + 1
            if h > maxh1:
                maxh2 = maxh1
                maxh1 = h
            elif h > maxh2:
                maxh2 = h
            if down_d[v] > max_cd:
                max_cd = down_d[v]
        down_h[u] = maxh1
        down_d[u] = fmax(maxh1 + maxh2, max_cd)
        yield

    dfs1(0, -1)

    up_h = [0] * n  # 从父方向来的最大高度
    up_d = [0] * n  # 上方连通块的直径

    @bootstrap
    def dfs2(u, fa):
        chs = children[u]
        # 预处理子树直径的最大值和次大值，方便 O(1) 排除
        max_d = sec_d = 0
        idx_max = -1
        for v in chs:
            d = down_d[v]
            if d > max_d:
                sec_d = max_d
                max_d = d
                idx_max = v
            elif d > sec_d:
                sec_d = d

        # 子节点高度降序
        child_hs = sorted((down_h[v] + 1 for v in chs), reverse=True)
        up_arm = up_h[u] if fa != -1 else 0

        for v in chs:
            hv = down_h[v] + 1
            # 去掉当前子节点后的前两大高度
            temp = []
            skipped = False
            for a in child_hs:
                if not skipped and a == hv:
                    skipped = True
                    continue
                temp.append(a)
                if len(temp) == 2:
                    break
            oc1 = temp[0] if temp else 0
            oc2 = temp[1] if len(temp) > 1 else 0

            # 加上 up 方向，取前两大臂长
            cands = [up_arm, oc1, oc2]
            cands.sort(reverse=True)
            o1 = cands[0]
            o2 = cands[1] if len(cands) > 1 else 0
            through = o1 + o2

            # 其他部分的最大直径
            other_d = sec_d if v == idx_max else max_d
            max_other = fmax(up_d[u], other_d)

            up_d[v] = fmax(through, max_other)
            max_arm = fmax(up_arm, oc1)
            up_h[v] = max_arm + 1

        for v in chs:
            yield dfs2(v, u)
        yield

    dfs2(0, -1)

    for u in range(n):
        res = up_d[u]
        for v in children[u]:
            res = fmax(res, down_d[v])
        print(res)

solve()