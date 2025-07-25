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

# seed(19981220)
# RANDOM = getrandbits(64)
 
# class Wrapper(int):
#     def __init__(self, x):
#         int.__init__(x)

#     def __hash__(self):
#         return super(Wrapper, self).__hash__() ^ RANDOM

# def TIME(f):

#     def wrap(*args, **kwargs):
#         s = perf_counter()
#         ret = f(*args, **kwargs)
#         e = perf_counter()

#         print(e - s, 'sec')
#         return ret
    
#     return wrap

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class lazy_segtree():
    def update(self,k):self.d[k]=self.op(self.d[2*k],self.d[2*k+1])
    def all_apply(self,k,f):
        self.d[k]=self.mapping(f,self.d[k])
        if (k<self.size):self.lz[k]=self.composition(f,self.lz[k])
    def push(self,k):
        self.all_apply(2*k,self.lz[k])
        self.all_apply(2*k+1,self.lz[k])
        self.lz[k]=self.identity
    def __init__(self,V,OP,E,MAPPING,COMPOSITION,ID):
        self.n=len(V)
        self.log=(self.n-1).bit_length()
        self.size=1<<self.log
        self.d=[E for i in range(2*self.size)]
        self.lz=[ID for i in range(self.size)]
        self.e=E
        self.op=OP
        self.mapping=MAPPING
        self.composition=COMPOSITION
        self.identity=ID
        for i in range(self.n):self.d[self.size+i]=V[i]
        for i in range(self.size-1,0,-1):self.update(i)
    def set(self,p,x):
        assert 0<=p and p<self.n
        p+=self.size
        for i in range(self.log,0,-1):self.push(p>>i)
        self.d[p]=x
        for i in range(1,self.log+1):self.update(p>>i)
    def get(self,p):
        assert 0<=p and p<self.n
        p+=self.size
        for i in range(self.log,0,-1):self.push(p>>i)
        return self.d[p]
    def prod(self,l,r):
        assert 0<=l and l<=r and r<=self.n
        if l==r:return self.e
        l+=self.size
        r+=self.size
        for i in range(self.log,0,-1):
            if (((l>>i)<<i)!=l):self.push(l>>i)
            if (((r>>i)<<i)!=r):self.push(r>>i)
        sml,smr=self.e,self.e
        while(l<r):
            if l&1:
                sml=self.op(sml,self.d[l])
                l+=1
            if r&1:
                r-=1
                smr=self.op(self.d[r],smr)
            l>>=1
            r>>=1
        return self.op(sml,smr)
    def all_prod(self):return self.d[1]
    def apply_point(self,p,f):
        assert 0<=p and p<self.n
        p+=self.size
        for i in range(self.log,0,-1):self.push(p>>i)
        self.d[p]=self.mapping(f,self.d[p])
        for i in range(1,self.log+1):self.update(p>>i)
    def apply(self,l,r,f):
        assert 0<=l and l<=r and r<=self.n
        if l==r:return
        l+=self.size
        r+=self.size
        for i in range(self.log,0,-1):
            if (((l>>i)<<i)!=l):self.push(l>>i)
            if (((r>>i)<<i)!=r):self.push((r-1)>>i)
        l2,r2=l,r
        while(l<r):
            if (l&1):
                self.all_apply(l,f)
                l+=1
            if (r&1):
                r-=1
                self.all_apply(r,f)
            l>>=1
            r>>=1
        l,r=l2,r2
        for i in range(1,self.log+1):
            if (((l>>i)<<i)!=l):self.update(l>>i)
            if (((r>>i)<<i)!=r):self.update((r-1)>>i)
    def max_right(self,l,g):
        assert 0<=l and l<=self.n
        assert g(self.e)
        if l==self.n:return self.n
        l+=self.size
        for i in range(self.log,0,-1):self.push(l>>i)
        sm=self.e
        while(1):
            while(l%2==0):l>>=1
            if not(g(self.op(sm,self.d[l]))):
                while(l<self.size):
                    self.push(l)
                    l=(2*l)
                    if (g(self.op(sm,self.d[l]))):
                        sm=self.op(sm,self.d[l])
                        l+=1
                return l-self.size
            sm=self.op(sm,self.d[l])
            l+=1
            if (l&-l)==l:break
        return self.n
    def min_left(self,r,g):
        assert (0<=r and r<=self.n)
        assert g(self.e)
        if r==0:return 0
        r+=self.size
        for i in range(self.log,0,-1):self.push((r-1)>>i)
        sm=self.e
        while(1):
            r-=1
            while(r>1 and (r%2)):r>>=1
            if not(g(self.op(self.d[r],sm))):
                while(r<self.size):
                    self.push(r)
                    r=(2*r+1)
                    if g(self.op(self.d[r],sm)):
                        sm=self.op(self.d[r],sm)
                        r-=1
                return r+1-self.size
            sm=self.op(self.d[r],sm)
            if (r&-r)==r:break
        return 0

'''
a1, a1^a2, a1^a2^a3, a1^a2^a3^a4 0

1 2 4 x
a1, a1^a2^x, a1^a2^a3, a1^a2^a3^a4^x

1 3 4 y
a1, a1^a2^x, a1^a2^a3^y, a1^a2^a3^a4^x


和第一个变的下标奇偶的，亦或上x

2 2 3
a2^x, a2^a3^y

2 2 4
a2^x a2^a3^y, a2^a3^a4^x
'''

'''
4 1 6 3 7

4 4 3 6 2

[0, 0, 5]
[4, 3, 7]

6 6 1 6 2
[0, 0, 7]
[6, 1, 5]
'''

# @TIME
def solve(testcase):
    
    n = II()
    A = LII()
    A = [0] + A
    n = len(A)
    cur = [0 for _ in range(20)]

    '''
    B A[0], A[0] ^ A[1] ^ A[2], A[0] ^ ... ^ A[4] ,...
    '''
    B = []
    '''
    C A[0] ^ A[1], A[0] ^ A[1] ^ A[2] ^ A[3] ,...
    '''
    C = []
    '''
    D: 0 2 4 6, .... 的xorsum
    '''
    D = []
    '''
    E: 1 3 5 7, .... 的xorsum
    '''
    E = []

    for i in range(n):
        for bit in range(20):
            if A[i] >> bit & 1:
                cur[bit] ^= 1
        if i & 1:
            C.append(cur[:] + [1])
            assert len(C[-1]) == 21
            E.append(A[i])
        else:
            B.append(cur[:] + [1])
            assert len(B[-1]) == 21
            D.append(A[i])
    
    # print('B', B)
    # print('C', C)
    
    xor_sum_even = lazy_segtree(
        D,
        lambda x, y: x ^ y,
        0,
        lambda y, x: x ^ y,
        lambda y, x: x ^ y,
        0
    )

    xor_sum_odd = lazy_segtree(
        E,
        lambda x, y: x ^ y,
        0,
        lambda y, x: x ^ y,
        lambda y, x: x ^ y,
        0
    )

    helper_even = lazy_segtree(
        B,
        lambda x, y: [x[i] + y[i] for i in range(21)],
        [0 for _ in range(20)] + [1],
        lambda y, x: [x[20] - x[i] if y >> i & 1 else x[i] for i in range(20)] + [x[20]],
        lambda y, x: x ^ y,
        0
    )

    helper_odd = lazy_segtree(
        C,
        lambda x, y: [x[i] + y[i] for i in range(20)] + [x[20] + y[20]],
        [0 for _ in range(20)] + [1],
        lambda y, x: [x[20] - x[i] if y >> i & 1 else x[i] for i in range(20)] + [x[20]],
        lambda y, x: x ^ y,
        0
    )

    q = II()

    def change_to_sum_even_idx(l, r):
        while l & 1:
            l += 1
        while r & 1:
            r -= 1
        return l >> 1, r >> 1

    def change_to_sum_odd_idx(l, r):
        while not l & 1:
            l += 1
        while not r & 1:
            r -= 1
        return l >> 1, r >> 1
    
    n, m = len(B), len(C)

    for _ in range(q):
        ops = LII()
        if ops[0] == 1:
            l, r, x = ops[1], ops[2], ops[3]
            left, right = change_to_sum_even_idx(l, r)
            if left <= right:
                xor_sum_even.apply(left, right + 1, x)
            left, right = change_to_sum_odd_idx(l, r)
            if left <= right:
                xor_sum_odd.apply(left, right + 1, x)
            if l & 1:
                if not r & 1:
                    r -= 1
                    l >>= 1
                    r >>= 1
                    helper_odd.apply(l, r + 1, x)
                    print('apply_odd', l, r, x)
                else:
                    l >>= 1
                    r = (r + 1) >> 1
                    helper_odd.apply(l, m, x)
                    helper_even.apply(r, n, x)
            else:
                if r & 1:
                    r -= 1
                    l >>= 1
                    r >>= 1
                    helper_even.apply(l, r + 1, x)
                    # print('apply_even', l, r, x)
                else:
                    l >>= 1
                    r = (r + 1) >> 1
                    helper_even.apply(l, n, x)
                    helper_odd.apply(r, m, x)
            
            # print('B', [helper_even.get(i) for i in range(len(B))])
            # print('C', [helper_odd.get(i) for i in range(len(C))])
            
        else:
            l, r = ops[1], ops[2]
            xor_sum = 0
            left, right = change_to_sum_even_idx(0, l - 1)
            xor_sum ^= xor_sum_even.prod(left, right + 1)
            left, right = change_to_sum_odd_idx(0, l - 1)
            xor_sum ^= xor_sum_odd.prod(left, right + 1)

            # print('xor_sum', xor_sum)

            res = [0 for _ in range(20)]

            left, right = change_to_sum_even_idx(l, r)
            even_part = helper_even.prod(left, right + 1)
            # print('debug', even_part)
            for i in range(20):
                res[i] += even_part[i]
            
            left, right = change_to_sum_odd_idx(l, r)
            odd_part = helper_odd.prod(left, right + 1)
            for i in range(20):
                res[i] += odd_part[i]

            LEN = r - l + 1
            ans = 0
            for bit in range(20):
                if xor_sum >> bit & 1:
                    ans += (LEN - res[bit]) << bit
                else:
                    ans += res[bit] << bit

            print(ans)           
            # res += helper_even.prod(left, right + 1)

            # print('even_part', helper_even.prod(left, right + 1)[0])
            
            # res += helper_odd.prod(left, right + 1)

            # print('odd_part', helper_odd.prod(left, right + 1)[0])

            # res ^= xor_sum

            # print(res)

for testcase in range(1):
    solve(testcase)