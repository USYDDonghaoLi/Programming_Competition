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

# '''
# 手写栈防止recursion limit
# 注意要用yield 不要用return
# 函数结尾要写yield None
# '''
# from types import GeneratorType
# def bootstrap(f, stack=[]):
#     def wrappedfunc(*args, **kwargs):
#         if stack:
#             return f(*args, **kwargs)
#         else:
#             to = f(*args, **kwargs)
#             while True:
#                 if type(to) is GeneratorType:
#                     stack.append(to)
#                     to = next(to)
#                 else:
#                     stack.pop()
#                     if not stack:
#                         break
#                     to = stack[-1].send(to)
#             return to
#     return wrappedfunc

# RANDOM = getrandbits(32)
 
# class Wrapper(int):
#     def __init__(self, x):
#         int.__init__(x)
 
#     def __hash__(self):
#         return super(Wrapper, self).__hash__() ^ RANDOM

# class FFT():
#     def primitive_root_constexpr(self, m):
#         if m == 2 :
#             return 1
#         if m == 167772161:
#             return 3
#         if m == 469762049:
#             return 3
#         if m == 754974721:
#             return 11
#         if m == 998244353:return 3
#         divs = [0 for _ in range(20)]
#         divs[0] = 2
#         cnt = 1
#         x= (m - 1) // 2
#         while x % 2==0:
#             x //= 2
#         i = 3
#         while i * i <= x:
#             if x % i == 0:
#                 divs[cnt] = i
#                 cnt += 1
#                 while x % i == 0:
#                     x //= i
#             i += 2
#         if x > 1:
#             divs[cnt] = x
#             cnt += 1
#         g = 2
#         while 1:
#             ok = True
#             for i in range(cnt):
#                 if pow(g, (m - 1) // divs[i], m) == 1:
#                     ok = False
#                     break
#             if ok:
#                 return g
#             g += 1
    
#     def bsf(self, x):
#         res = 0
#         while x % 2 == 0 :
#             res += 1
#             x //= 2
#         return res
#     butterfly_first = True
#     butterfly_inv_first = True
#     sum_e = [0 for _ in range(30)]
#     sum_ie = [0 for _ in range(30)]

#     def __init__(self, MOD):
#         self.mod = MOD
#         self.g = self.primitive_root_constexpr(self.mod)

#     def butterfly(self, a):
#         n = len(a)
#         h = (n - 1).bit_length()
#         if self.butterfly_first:
#             self.butterfly_first = False
#             es = [0 for _ in range(30)]
#             ies = [0 for _ in range(30)]
#             cnt2 = self.bsf(self.mod - 1)
#             e = pow(self.g, (self.mod - 1) >> cnt2, self.mod)
#             ie = pow(e, self.mod-2, self.mod)
#             for i in range(cnt2, 1, -1):
#                 es[i - 2] = e
#                 ies[i - 2] = ie
#                 e=(e * e) % self.mod
#                 ie=(ie * ie) % self.mod
#             now = 1
#             for i in range(cnt2 - 2):
#                 self.sum_e[i] = ((es[i] * now) % self.mod)
#                 now *= ies[i]
#                 now %= self.mod
#         for ph in range(1, h + 1):
#             w = 1 << (ph - 1)
#             p = 1 << (h - ph)
#             now = 1
#             for s in range(w):
#                 offset = s << (h - ph + 1)
#                 for i in range(p):
#                     l = a[i + offset]
#                     r = a[i + offset + p] * now
#                     r %= self.mod
#                     a[i + offset] = l + r
#                     a[i + offset] %= self.mod
#                     a[i + offset + p] = l - r
#                     a[i + offset + p] %= self.mod
#                 now *= self.sum_e[(~s & -~s).bit_length() - 1]
#                 now %= self.mod
#     def butterfly_inv(self, a):
#         n = len(a)
#         h = (n - 1).bit_length()
#         if self.butterfly_inv_first:
#             self.butterfly_inv_first = False
#             es = [0 for _ in range(30)]
#             ies = [0 for _ in range(30)]
#             cnt2 = self.bsf(self.mod - 1)
#             e = pow(self.g, (self.mod - 1) >> cnt2, self.mod)
#             ie = pow(e, self.mod - 2, self.mod)
#             for i in range(cnt2, 1, -1):
#                 es[i - 2] = e
#                 ies[i - 2] = ie
#                 e = (e * e) % self.mod
#                 ie = (ie * ie) % self.mod
#             now = 1
#             for i in range(cnt2 - 2):
#                 self.sum_ie[i] = ((ies[i] * now) % self.mod)
#                 now *= es[i]
#                 now %= self.mod
#         for ph in range(h, 0, -1):
#             w=1 << (ph - 1)
#             p=1 << (h - ph)
#             inow = 1
#             for s in range(w):
#                 offset = s << (h - ph + 1)
#                 for i in range(p):
#                     l = a[i + offset]
#                     r = a[i + offset + p]
#                     a[i + offset] = l + r
#                     a[i + offset] %= self.mod
#                     a[i + offset + p] = (l - r) * inow
#                     a[i + offset + p] %= self.mod
#                 inow *= self.sum_ie[(~s & -~s).bit_length() - 1]
#                 inow %= self.mod
#     def convolution(self, a, b):
#         n = len(a); m = len(b)
#         if not(a) or not(b):
#             return []
#         if min(n, m)<=40:
#             if n < m:
#                 n, m = m, n
#                 a, b = b, a
#             res=[0 for _ in range(n + m - 1)]
#             for i in range(n):
#                 for j in range(m):
#                     res[i + j] += a[i] * b[j]
#                     res[i + j] %= self.mod
#             return res
#         z = 1 << ((n + m - 2).bit_length())
#         a = a + [0 for _ in range(z - n)]
#         b = b + [0 for _ in range(z - m)]
#         self.butterfly(a)
#         self.butterfly(b)
#         c=[0 for _ in range(z)]
#         for i in range(z):
#             c[i] = (a[i] * b[i]) % self.mod
#         self.butterfly_inv(c)
#         iz=pow(z, self.mod - 2, self.mod)
#         for i in range(n + m - 1):
#             c[i] = (c[i] * iz) % self.mod
#         return c[: n+ m -1]

# CALC = FFT(469762049)

#FFT for mod 998244353
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
    # fo = open('Atcoder/ABC/307/random_45.txt')
    # n, m = map(int, fo.readline().rstrip('\n').split())
    # t = fo.readline().rstrip('\n')
    # p = fo.readline().rstrip('\n')

    n, m = MI()
    t = I()
    p = I()

    t = t + '.' * (m - 1) + t
    if n == m:
        t = t[::-1]
    else:
        t = t + '.' * (m - n - 1)
    
    t = t[::-1]

    '''
    (x - y) ** 2 * x * y
    = (x ** 2 - 2 * x * y + y ** 2) * x * y
    = x ** 3 * y - 2 * x ** 2 * y ** 2 + x * y ** 3
    '''

    def ops(c):
        if c == '_':
            return 0
        elif c == '.':
            return 1
        elif c.islower():
            return ord(c) - ord('a') + 28
        else:
            return ord(c) - ord('A') + 2
    
    # for i in range(65, 65 + 26):
    #     print(chr(i), ops(chr(i)))
    # for i in range(97, 97 + 26):
    #     print(chr(i), ops(chr(i)))
    
    T = list(map(ops, t))
    P = list(map(ops, p))
    if len(T) > len(P):
        P.extend([0 for _ in range(len(T) - len(P))])
    else:
        P = P[:len(T)]
    T2 = [0] + [t * t for t in T]
    P2 = [p * p for p in P]
    T3 = [0] + [t * t * t for t in T]
    P3 = [0] + [p * p * p for p in P]

    res1 = CALC.convolution(T3, P)
    res2 = CALC.convolution(T2, P2)
    res3 = CALC.convolution(T, P3)
    MAX = n + m + m - 2
    if len(res1) < MAX:
        res1.extend([0 for _ in range(MAX - len(res1))])
    if len(res2) < MAX:
        res2.extend([0 for _ in range(MAX - len(res2))])
    if len(res3) < MAX:
        res3.extend([0 for _ in range(MAX - len(res3))])

    res = 0
    for i in range(m, n + m + m - 2):
        if res1[i] - 2 * res2[i] + res3[i] == 0:
            res += 1
        else:
            continue
    
    print(res)

for testcase in range(1):
    solve(testcase)