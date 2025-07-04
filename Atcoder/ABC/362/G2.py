standard_input, packages, output_together = 1, 1, 0
dfs, hashing, read_from_file = 0, 0, 0
de = 1

if 1:

    if standard_input:
        import io, os, sys
        input = lambda: sys.stdin.readline().strip()

        import math
        inf = math.inf

        def I():
            return input()
        
        def II():
            return int(input())

        def MII():
            return map(int, input().split())

        def LI():
            return list(input().split())

        def LII():
            return list(map(int, input().split()))

        def LFI():
            return list(map(float, input().split()))

        def GMI():
            return map(lambda x: int(x) - 1, input().split())

        def LGMI():
            return list(map(lambda x: int(x) - 1, input().split()))

    if packages:
        from io import BytesIO, IOBase

        import random
        import os

        import bisect
        import typing
        from collections import Counter, defaultdict, deque
        from copy import deepcopy
        from functools import cmp_to_key, lru_cache, reduce
        from heapq import merge, heapify, heappop, heappush, heappushpop, nlargest, nsmallest
        from itertools import accumulate, combinations, permutations, count, product
        from operator import add, iand, ior, itemgetter, mul, xor
        from string import ascii_lowercase, ascii_uppercase, ascii_letters
        from typing import *
        BUFSIZE = 4096

    if output_together:
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

        sys.stdout = IOWrapper(sys.stdout)

    if dfs:
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

    if hashing:
        RANDOM = random.getrandbits(20)
        class Wrapper(int):
            def __init__(self, x):
                int.__init__(x)

            def __hash__(self):
                return super(Wrapper, self).__hash__() ^ RANDOM

    if read_from_file:
        file = open("input.txt", "r").readline().strip()[1:-1]
        fin = open(file, 'r')
        input = lambda: fin.readline().strip()
        output_file = open("output.txt", "w")
        def fprint(*args, **kwargs):
            print(*args, **kwargs, file=output_file)

    if de:
        def debug(*args, **kwargs):
            print('\033[92m', end='')
            print(*args, **kwargs)
            print('\033[0m', end='')

def sa_naive(s):
    n = len(s)
    return sorted(range(n), key=lambda i: s[i:])

def sa_doubling(s):
    def key(i):
        if i + k < n:
            return rank[i], rank[i + k]
        return rank[i], -1

    smax = max(s) + 1
    n = len(s)
    sa = list(range(n))
    rank = s[:]
    tmp = [0] * n

    k = 1
    while k < n:
        sa.sort(key=key)
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i-1]] + (key(sa[i-1]) < key(sa[i]))
        rank, tmp = tmp, rank
        k <<= 1
    return sa

def sa_is(s, upper, THRESHHOLD_NAIVE=20, THRESHHOLD_DOUBLE=100):
    def induce(lms):
        for i in range(n):
            sa[i] = -1
        buf = sum_s[:]
        for d in lms:
            if d == n:
                continue
            sa[buf[s[d]]] = d
            buf[s[d]] += 1

        buf = sum_l[:]
        sa[buf[s[n - 1]]] = n - 1
        buf[s[n - 1]] += 1
        for i in range(n):
            v = sa[i]
            if v >= 1 and not ls[v - 1]:
                sa[buf[s[v - 1]]] = v - 1
                buf[s[v - 1]] += 1

        buf = sum_l[:]
        for i in range(n)[::-1]:
            v = sa[i]
            if v >= 1 and ls[v - 1]:
                buf[s[v - 1] + 1] -= 1
                sa[buf[s[v - 1] + 1]] = v - 1

    n = len(s)
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n <= THRESHHOLD_NAIVE:
        return sa_naive(s)
    if n <= THRESHHOLD_DOUBLE:
        return sa_doubling(s)

    sa = [0] * n
    ls = [0] * n
    for i in range(n - 1)[::-1]:
        if s[i] == s[i + 1]:
            ls[i] = ls[i + 1]
        else:
            ls[i] = int(s[i] < s[i + 1])

    sum_l = [0] * (upper + 1)
    sum_s = [0] * (upper + 1)
    for i, x in enumerate(ls):
        if not x:
            sum_s[s[i]] += 1
        else:
            sum_l[s[i] + 1] += 1
    for i in range(upper + 1):
        sum_s[i] += sum_l[i]
        if i < upper:
            sum_l[i + 1] += sum_s[i]

    lms_map = [-1] * (n + 1)
    lms = []
    m = 0
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms_map[i] = m
            lms.append(i)
            m += 1

    induce(lms)

    if m:
        sorted_lms = []
        for v in sa:
            if v == -1:
                print("minuse")
            if lms_map[v] != -1:
                sorted_lms.append(v)

        rec_s = [0] * m
        rec_upper = 0
        rec_s[lms_map[sorted_lms[0]]] = 0
        for i in range(1, m):
            l = sorted_lms[i - 1]
            r = sorted_lms[i]
            end_l = lms[lms_map[l] + 1] if lms_map[l] + 1 < m else n
            end_r = lms[lms_map[r] + 1] if lms_map[r] + 1 < m else n
            same = 1
            if end_l - l != end_r - r:
                same = 0
            else:
                while l < end_l:
                    if s[l] != s[r]:
                        break
                    l += 1
                    r += 1
                if l == n or s[l] != s[r]:
                    same = 0
            if not same:
                rec_upper += 1
            rec_s[lms_map[sorted_lms[i]]] = rec_upper

        rec_sa = sa_is(rec_s, rec_upper)
        for i in range(m):
            sorted_lms[i] = lms[rec_sa[i]]
        induce(sorted_lms)
    return sa

def suffix_array(S, compress=True):
    if compress:
        ch = sorted(set(S))
        ctoi = {c: i for i, c in enumerate(ch, 1)}
        S = [ctoi[s] for s in S]

    upper = max(S) + 1
    return sa_is(S, upper)

def construct_lcp(s, sa):
    n = len(s)
    assert(n >= 1)
    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i

    lcp = [0] * n
    h = 0
    for i in range(n):
        if h > 0:
            h -= 1
        if rank[i] == 0:
            continue
        j = sa[rank[i] - 1]
        while j + h < n and i + h < n:
            if s[j + h] != s[i + h]:
                break
            h += 1
        lcp[rank[i] - 1] = h
    return lcp

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y
class UnionFind:
    def __init__(self, n, size=None):
        self.parent_or_size = [-1] * n if size is None else [-x for x in size]
        self.ls = list(range(n))
        self.rs = list(range(n))
 
    def find(self, a):
        a = self.parent_or_size[a] if self.parent_or_size[a] >= 0 else a
        acopy = a
        while self.parent_or_size[a] >= 0:
            a = self.parent_or_size[a]
        while acopy != a:
            self.parent_or_size[acopy], acopy = a, self.parent_or_size[acopy]
        return a
 
    def merge(self, a, b):
        pa, pb = self.find(a), self.find(b)
        if pa == pb: return False
        if self.parent_or_size[pa] > self.parent_or_size[pb]:
            pa, pb = pb, pa
        self.ls[pa] = fmin(self.ls[pa], self.ls[pb])
        self.rs[pa] = fmax(self.rs[pa], self.rs[pb])
        self.parent_or_size[pa] += self.parent_or_size[pb]
        self.parent_or_size[pb] = pa
        return True
 
    def getlr(self, a):
        a = self.find(a)
        return self.ls[a], self.rs[a]

s = I()
n = len(s)

q = II()
strs = [I() for _ in range(q)]
start_idx = [n + 1]
for i in range(q - 1):
    start_idx.append(start_idx[-1] + len(strs[i]) + 1)

ns = s + '#' + '#'.join(strs)

sa = suffix_array(ns)
lcp = construct_lcp(ns, sa)

sa_map = [0] * len(ns)
vis = [0] * len(ns)
for i in range(len(ns)):
    if sa[i] < n:
        vis[i] = 1
    sa_map[sa[i]] = i
print(vis)
vis = list(accumulate(vis, initial=0))
print(vis)
merge_order = [[] for _ in range(len(ns))]

for i in range(len(ns) - 1):
    merge_order[lcp[i]].append(i)

ans = [-1] * q
queries = sorted(range(q), key=lambda x: -len(strs[x]))
pt = 0


union = UnionFind(len(ns))
for i in range(len(ns) - 1, 0, -1):
    for x in merge_order[i]:
        union.merge(x, x + 1)
    while pt < q and len(strs[queries[pt]]) == i:
        l, r = union.getlr(sa_map[start_idx[queries[pt]]])
        ans[queries[pt]] = vis[r+1] - vis[l]
        pt += 1

print('\n'.join(map(str, ans)))