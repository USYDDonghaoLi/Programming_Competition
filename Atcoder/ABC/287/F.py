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

mod = 998244353

##FFT for mod 998244353
class FPS:
    sum_e = (911660635, 509520358, 369330050, 332049552, 983190778, 123842337, 238493703, 975955924, 603855026, 856644456, 131300601, 842657263, 730768835, 942482514, 806263778, 151565301, 510815449, 503497456, 743006876, 741047443, 56250497)
    sum_ie = (86583718, 372528824, 373294451, 645684063, 112220581, 692852209, 155456985, 797128860, 90816748, 860285882, 927414960, 354738543, 109331171, 293255632, 535113200, 308540755, 121186627, 608385704, 438932459, 359477183, 824071951)
    mod = 998244353
    g = 3
    def butterfly(self, a):
        n = len(a)
        h = (n - 1).bit_length()
        for ph in range(1, h + 1):
            w = 1 << (ph - 1)
            p = 1 << (h - ph)
            now = 1
            for s in range(w):
                offset = s << (h - ph + 1)
                for i in range(p):
                    l = a[i + offset]
                    r = a[i + offset + p] * now
                    r %= self.mod
                    a[i + offset] = l + r
                    a[i + offset] %= self.mod
                    a[i + offset + p] = l - r
                    a[i + offset + p] %= self.mod
                now *= self.sum_e[(~s & -~s).bit_length() - 1]
                now %= self.mod
    def butterfly_inv(self, a):
        n = len(a)
        h = (n - 1).bit_length()
        for ph in range(h, 0, -1):
            w = 1 << (ph - 1)
            p = 1 << (h - ph)
            inow = 1
            for s in range(w):
                offset = s << (h - ph + 1)
                for i in range(p):
                    l = a[i + offset]
                    r = a[i + offset + p]
                    a[i + offset] = l + r
                    a[i + offset] %= self.mod
                    a[i + offset + p] = (l - r) * inow
                    a[i + offset + p] %= self.mod
                inow *= self.sum_ie[(~s & -~s).bit_length()-1]
                inow %= self.mod
    def convolution(self, a, b):
        n = len(a);m = len(b)
        if not(a) or not(b):
            return []
        if min(n, m) <= 40:
            if n < m:
                n, m = m, n
                a, b = b, a
            res = [0 for _ in range(n + m - 1)]
            for i in range(n):
                for j in range(m):
                    res[i+j] += a[i] * b[j]
                    res[i+j] %= self.mod
            return res
        z = 1 << ((n + m - 2).bit_length())
        a = a + [0 for _ in range(z - n)]
        b = b + [0 for _ in range(z - m)]
        self.butterfly(a)
        self.butterfly(b)
        c=[0 for _ in range(z)]
        for i in range(z):
            c[i] = (a[i] * b[i]) % self.mod
        self.butterfly_inv(c)
        iz = pow(z, self.mod - 2, self.mod)
        for i in range(n + m - 1):
            c[i] = (c[i] * iz) % self.mod
        return c[:n+m-1]

CALC = FPS()
    
def solve(testcase):
    n = II()
    adj = defaultdict(list)
    for _ in range(n - 1):
        u, v = MI()
        adj[u].append(v)
        adj[v].append(u)
    
    child = defaultdict(list)
    q = deque()
    q.append((1, 0))

    while q:
        cur, fa = q.popleft()
        for o in adj[cur]:
            if o == fa:
                continue
            q.append((o, cur))
            child[cur].append(o)
    
    '''
    以i为根节点的子树，选或不选，j个连通块的方案数
    '''
    dp1 = [[] for _ in range(n + 1)]
    dp2 = [[] for _ in range(n + 1)]
    @bootstrap
    def dfs(node):

        mul1 = [1]
        mul2 = [1]

        for o in child[node]:
            yield dfs(o)
            m = max(len(dp1[o]), len(dp2[o]))
            t1 = [0 for _ in range(m)]
            t2 = [0 for _ in range(m)]
            for i in range(len(dp1[o])):
                t2[i] += dp1[o][i]
                if i:
                    t1[i - 1] += dp1[o][i]
            for i in range(len(dp2[o])):
                t1[i] += dp2[o][i]
                t2[i] += dp2[o][i]
                t1[i] %= mod
                t2[i] %= mod

            mul1 = CALC.convolution(mul1, t1)
            mul2 = CALC.convolution(mul2, t2)
            # while not mul1[-1]:
            #     mul1.pop()
            # while not mul2[-1]:
            #     mul2.pop()
        
        dp1[node] = CALC.convolution([0, 1], mul1)
        dp2[node] = CALC.convolution([1, 0], mul2)
        # while not dp1[node][-1]:
        #     dp1[node].pop()
        # while not dp2[node][-1]:
        #     dp2[node].pop()
        # print(node, dp1[node], dp2[node])

        yield None
    
    dfs(1)
    dp1[1].extend([0 for _ in range(n + 1 - len(dp1[1]))])
    dp2[1].extend([0 for _ in range(n + 1 - len(dp2[1]))])

    for j in range(1, n + 1):
        print((dp1[1][j] + dp2[1][j]) % mod)

for testcase in range(1):
    solve(testcase)