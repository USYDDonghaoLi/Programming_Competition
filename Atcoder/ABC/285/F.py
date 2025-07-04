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

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0 for _ in range(n)]

    def lowbit(self, x):
        return x & (-x)

    def update(self, pos, x):
        while pos < self.n:
            self.tree[pos] += x
            pos += self.lowbit(pos)

    def query(self, pos):
        to_ret = 0
        while pos:
            to_ret += self.tree[pos]
            pos -= self.lowbit(pos)
        return to_ret

    def query_sum(self, l, r):
        return self.query(r) - self.query(l - 1)

class SegTree:

    def __init__(self, V, OP, E):
        '''
        V: 原始数组
        OP: 维护的运算(min, max, sum...)
        E: 线段树初值
        '''
        self.n = len(V)
        self.op = OP
        self.e = E
        self.log = (self.n - 1).bit_length()
        self.size = 1 << self.log
        self.d=[E for i in range(2*self.size)]
        for i in range(self.n):
            self.d[self.size + i] = V[i]
        for i in range(self.size - 1, 0, -1):
            self.update(i)

    def set(self, p, x):
        assert 0 <= p and p < self.n
        p += self.size
        self.d[p] = x
        for i in range(1, self.log + 1):
            self.update(p >> i)

    def get(self, p):
        assert 0 <= p and p <self.n
        return self.d[p + self.size]

    def prod(self,l,r):
        #[l, r)
        assert 0 <= l and l <= r and r <= self.n
        sml = self.e
        smr = self.e
        l += self.size
        r += self.size

        while(l < r):
            if (l & 1):
                sml = self.op(sml, self.d[l])
                l += 1
            if (r & 1):
                smr = self.op(self.d[r - 1], smr)
                r -= 1
            l >>= 1
            r >>= 1
        return self.op(sml, smr)

    def all_prod(self):
        return self.d[1]

    def max_right(self, l, f):
        assert 0 <= l and l <= self.n
        assert f(self.e)
        if l == self.n:
            return self.n
        l += self.size
        sm = self.e
        while(1):
            while(l % 2 == 0):
                l >>= 1
            if not(f(self.op(sm, self.d[l]))):
                while(l < self.size):
                    l = 2 * l
                    if f(self.op(sm, self.d[l])):
                        sm = self.op(sm, self.d[l])
                        l += 1
                return l - self.size
            sm = self.op(sm,self.d[l])
            l += 1
            if (l & -l) == l:
                break
        return self.n
    def min_left(self, r, f):
        assert 0 <= r and r < self.n
        assert f(self.e)
        if r == 0:
            return 0
        r += self.size
        sm = self.e
        while(1):
            r -= 1
            while(r > 1 & (r % 2)):
                r >>= 1
            if not(f(self.op(self.d[r], sm))):
                while(r < self.size):
                    r = (2 * r + 1)
                    if f(self.op(self.d[r], sm)):
                        sm=self.op(self.d[r], sm)
                        r -= 1
                return r + 1 - self.size
            sm = self.op(self.d[r] ,sm)
            if (r & -r) == r:
                break
        return 0

    def update(self, k):
        self.d[k] = self.op(self.d[2 * k], self.d[2 * k + 1])
        
    def __str__(self):
        return str([self.get(i) for i in range(self.n)])

def solve(testcase):
    n = II()
    trees = [FenwickTree(n + 1) for _ in range(26)]
    s = list(I())

    freq = [0 for _ in range(26)]
    V = []
    for i, c in enumerate(s):
        freq[ord(c) - ord('a')] += 1
        if i:
            if s[i] >= s[i - 1]:
                V.append(1)
            else:
                V.append(0)
        trees[ord(c) - ord('a')].update(i + 1, 1)

    def OP(a, b):
        return a & b
    sg = SegTree(V, OP, 1)


    q = II()
    for _ in range(q):
        ops = LI()
        if ops[0] == '1':
            idx = int(ops[1])
            idx -= 1
            trees[ord(s[idx]) - ord('a')].update(idx + 1, -1)
            new = ops[2]
            trees[ord(new) - ord('a')].update(idx + 1, 1)
            freq[ord(s[idx]) - ord('a')] -= 1
            freq[ord(new) - ord('a')] += 1
            s[idx] = new
            if idx:
                if s[idx] >= s[idx - 1]:
                    sg.set(idx - 1, 1)
                else:
                    sg.set(idx - 1, 0)
            if idx != n - 1:
                if s[idx] <= s[idx + 1]:
                    sg.set(idx, 1)
                else:
                    sg.set(idx, 0)
        else:
            l, r = int(ops[1]) - 1, int(ops[2]) - 1
            if l == r:
                print('Yes')
                continue
            else:
                if not sg.prod(l, r):
                    #print('sg', sg.prod(l, r - 1))
                    print('No')
                    continue
                else:
                    freq2 = [trees[i].query_sum(l + 1, r + 1) for i in range(26)]
                    #print('f', freq)
                    #print('f2', freq2)
                    start = -1
                    end = -1
                    for i in range(26):
                        if freq2[i]:
                            start = i
                            break
                    for i in range(25, -1, -1):
                        if freq2[i]:
                            end = i
                            break
                    #print('se', start, end)

                    flag = True
                    if freq[start] < freq2[start] or freq[end] < freq2[end]:
                        flag = False

                    for i in range(start + 1, end):
                        if freq[i] != freq2[i]:
                            flag = False
                            break
                    
                    print('Yes' if flag else 'No')


for testcase in range(1):
    solve(testcase)