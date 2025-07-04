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

class Factorial:
    def __init__(self, N, mod) -> None:
        self.mod = mod
        self.f = [1 for _ in range(N)]
        self.g = [1 for _ in range(N)]
        for i in range(1, N):
            self.f[i] = self.f[i - 1] * i % self.mod
        self.g[-1] = pow(self.f[-1], mod - 2, mod)
        for i in range(N - 2, -1, -1):
            self.g[i] = self.g[i + 1] * (i + 1) % self.mod
    
    def comb(self, n, m):
        if n < m:
            return 0
        return self.f[n] * self.g[m] % self.mod * self.g[n - m] % self.mod
    
    def perm(self, n, m):
        return self.f[n] * self.g[n - m] % self.mod

    def catalan(self, n):
        #TODO: check 2 * n < N#
        return (self.comb(2 * n, n) - self.comb(2 * n, n - 1)) % self.mod
    
FACTORIAL = Factorial(100, mod)

pw = [[1 for _ in range(12)] for _ in range(100005)]
for i in range(100005):
    for j in range(1, 12):
        pw[i][j] = pw[i][j - 1] * i % mod

class lazy_segtree():
    def update(self, k):
        self.d[k] = self.op(self.d[2 * k], self.d[2 * k + 1])

    def all_apply(self, k, f):
        self.d[k] = self.mapping(f, self.d[k])
        if (k < self.size):
            self.lz[k] = self.composition(f, self.lz[k])

    def push(self, k):
        self.all_apply(2 * k, self.lz[k])
        self.all_apply(2 * k + 1 ,self.lz[k])
        self.lz[k] = self.identity

    def __init__(self, V, OP, E, MAPPING, COMPOSITION, ID):
        '''
        V -> 初始数组
        OP -> 线段树上维护的运算(min, max, sum等等)
        E -> 线段树上的初始值
        MAPPING -> 懒更新数组对线段树的影响
        COMPOSITION -> 懒更新叠加的方式
        ID -> 懒更新数组初值
        '''
        self.n = len(V)
        self.log = (self.n - 1).bit_length()
        self.size = 1 << self.log
        self.d = [E for _ in range(2*self.size)]
        self.lz = [ID for _ in range(self.size)]
        self.e = E
        self.op = OP
        self.mapping = MAPPING
        self.composition = COMPOSITION
        self.identity = ID
        for i in range(self.n):
            self.d[self.size + i] = V[i]
        for i in range(self.size-1, 0, -1):
            self.update(i)

    def set(self,p,x):
        assert 0 <= p and p < self.n
        p += self.size
        for i in range(self.log, 0, -1):
            self.push(p >> i)
        self.d[p] = x
        for i in range(1, self.log + 1):
            self.update(p >> i)

    def get(self, p):
        assert 0 <= p and p < self.n
        p += self.size
        for i in range(self.log, 0, -1):
            self.push(p >> i)
        return self.d[p]

    def prod(self, l, r):
        assert 0 <= l and l <= r and r <= self.n
        if l == r:
            return self.e
        l += self.size
        r += self.size
        for i in range(self.log ,0 ,-1):
            if (((l >> i) << i) != l):self.push(l >> i)
            if (((r >> i) << i) != r):self.push(r >> i)
        sml, smr = self.e ,self.e
        while(l < r):
            if l & 1:
                sml = self.op(sml, self.d[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self.op(self.d[r], smr)
            l >>= 1
            r >>= 1
        return self.op(sml, smr)

    def all_prod(self):
        return self.d[1]

    def apply_point(self, p, f):
        assert 0 <= p and p < self.n
        p += self.size
        for i in range(self.log, 0, -1):
            self.push(p >> i)
        self.d[p] = self.mapping(f, self.d[p])
        for i in range(1,self.log + 1):
            self.update(p >> i)

    '''
    更新lz数组
    '''
    def apply(self, l, r, f):
        assert 0 <= l and l <= r and r <= self.n
        if l == r:return
        l += self.size
        r += self.size
        for i in range(self.log, 0, -1):
            if (((l >> i) << i) != l):self.push(l >> i)
            if (((r >> i) << i) != r):self.push((r - 1) >> i)
        l2, r2 = l, r
        while l < r:
            if l & 1:
                self.all_apply(l, f)
                l += 1
            if (r & 1):
                r -= 1
                self.all_apply(r, f)
            l >>= 1
            r >>= 1
        l, r = l2, r2
        for i in range(1, self.log + 1):
            if (((l >> i) << i) != l):self.update(l >> i)
            if (((r >> i) << i) != r):self.update((r - 1) >> i)

    def max_right(self, l, g):
        assert 0 <= l and l <= self.n
        assert g(self.e)
        if l == self.n:
            return self.n
        l += self.size
        for i in range(self.log, 0, -1):
            self.push(l >> i)
        sm = self.e
        while(1):
            while(l%2 == 0):
                l >>= 1
            if not(g(self.op(sm, self.d[l]))):
                while (l < self.size):
                    self.push(l)
                    l = (2 * l)
                    if (g(self.op(sm, self.d[l]))):
                        sm = self.op(sm, self.d[l])
                        l += 1
                return l - self.size
            sm = self.op(sm, self.d[l])
            l += 1
            if (l & -l) == l:
                break
        return self.n

    def min_left(self, r, g):
        assert (0 <= r and r <= self.n)
        assert g(self.e)
        if r == 0:
            return 0
        r += self.size
        for i in range(self.log, 0, -1):
            self.push((r - 1) >> i)
        sm = self.e
        while(1):
            r -= 1
            while(r > 1 and (r % 2)):
                r >>= 1
            if not(g(self.op(self.d[r], sm))):
                while(r < self.size):
                    self.push(r)
                    r = (2 * r + 1)
                    if g(self.op(self.d[r], sm)):
                        sm = self.op(self.d[r], sm)
                        r -= 1
                return r + 1- self.size
            sm = self.op(self.d[r] ,sm)
            if (r & -r) == r:
                break
        return 0

def solve(testcase):
    n, k = MI()
    nums = LII()
    
    V = [[1, 0, 0, 0, 0, 0] for _ in range(n)]
    E = [0 for _ in range(6)]
    ID = 0
    def OP(A, B):
        return [(a + b) % mod for a, b in zip(A, B)]
    def MAPPING(f, x):
        for i in range(5, 0, -1):
            for j in range(i - 1, -1, -1):
                x[i] += x[j] * FACTORIAL.comb(i, j) % mod * pw[f][i - j] % mod
                x[i] %= mod
        return x
    def COMPOSITION(f, g):
        return f + g
    
    sg = lazy_segtree(V, OP, E, MAPPING, COMPOSITION, ID)
    mp = defaultdict(lambda : -1)
    res = 0
    # print('self.d', sg.d)

    for i, v in enumerate(nums):
        sg.apply(mp[v] + 1, i + 1, 1)
        # print('self.d', sg.d)
        # print('node[1]', sg.all_prod())
        # print('prod', sg.prod(1, n)[k])
        res += sg.d[1][k]
        res %= mod
        mp[v] = i

    print(res)

for testcase in range(II()):
    solve(testcase)