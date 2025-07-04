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

# def TIME(f):

#     def wrap(*args, **kwargs):
#         s = perf_counter()
#         ret = f(*args, **kwargs)
#         e = perf_counter()

#         print(e - s, 'sec')
#         return ret
    
#     return wrap
class LazySegmentTree():
    __slots__ = ['n', 'log', 'size', 'd', 'lz', 'e', 'op', 'mapping', 'composition', 'identity']
    def _update(self, k):self.d[k]=self.op(self.d[2 * k], self.d[2 * k + 1])
    def _all_apply(self, k, f):
        self.d[k]=self.mapping(f,self.d[k])
        if (k<self.size):self.lz[k]=self.composition(f,self.lz[k])
    def _push(self, k):
        self._all_apply(2 * k, self.lz[k])
        self._all_apply(2 * k + 1, self.lz[k])
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
        for i in range(self.size-1,0,-1):self._update(i)
    def set(self,p,x):
        assert 0<=p and p<self.n
        p+=self.size
        for i in range(self.log,0,-1):self._push(p >> i)
        self.d[p]=x
        for i in range(1,self.log+1):self._update(p >> i)
    def get(self,p):
        assert 0<=p and p<self.n
        p+=self.size
        for i in range(self.log,0,-1):self._push(p >> i)
        return self.d[p]
    def prod(self,l,r):
        assert 0<=l and l<=r and r<=self.n
        if l==r:return self.e
        l+=self.size
        r+=self.size
        for i in range(self.log,0,-1):
            if (((l>>i)<<i)!=l):self._push(l >> i)
            if (((r>>i)<<i)!=r):self._push(r >> i)
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
        for i in range(self.log,0,-1):self._push(p >> i)
        self.d[p]=self.mapping(f,self.d[p])
        for i in range(1,self.log+1):self._update(p >> i)
    def apply(self,l,r,f):
        assert 0<=l and l<=r and r<=self.n
        if l==r:return
        l+=self.size
        r+=self.size
        for i in range(self.log,0,-1):
            if (((l>>i)<<i)!=l):self._push(l >> i)
            if (((r>>i)<<i)!=r):self._push((r - 1) >> i)
        l2,r2=l,r
        while(l<r):
            if (l&1):
                self._all_apply(l, f)
                l+=1
            if (r&1):
                r-=1
                self._all_apply(r, f)
            l>>=1
            r>>=1
        l,r=l2,r2
        for i in range(1,self.log+1):
            if (((l>>i)<<i)!=l):self._update(l >> i)
            if (((r>>i)<<i)!=r):self._update((r - 1) >> i)
    def max_right(self,l,g):
        assert 0<=l and l<=self.n
        assert g(self.e)
        if l==self.n:return self.n
        l+=self.size
        for i in range(self.log,0,-1):self._push(l >> i)
        sm=self.e
        while(1):
            while(i%2==0):l>>=1
            if not(g(self.op(sm,self.d[l]))):
                while(l<self.size):
                    self._push(l)
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
        for i in range(self.log,0,-1):self._push((r - 1) >> i)
        sm=self.e
        while(1):
            r-=1
            while(r>1 and (r%2)):r>>=1
            if not(g(self.op(self.d[r],sm))):
                while(r<self.size):
                    self._push(r)
                    r=(2*r+1)
                    if g(self.op(self.d[r],sm)):
                        sm=self.op(self.d[r],sm)
                        r-=1
                return r+1-self.size
            sm=self.op(self.d[r],sm)
            if (r&-r)==r:break
        return 0

mod = 998244353

def __add__(a, b):
    return (a + b) % mod

def __mul__(a, b):
    return a * b % mod

def OP(A, B):
    # print('OP', A, B)
    res = [[(A[i][j] + B[i][j]) % mod for j in range(3)] for i in range(3)]
    return res

def MAP(B, A):
    res = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                # if i == 1 and j == 1:
                #     print(i, j, A[i][k], B[k][j])
                res[i][j] += A[i][k] * B[k][j] % mod
                res[i][j] %= mod
    return res

def COMP(A, B):
    res = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                # if i == 1 and j == 1:
                #     print(i, j, A[i][k], B[k][j])
                res[i][j] += A[i][k] * B[k][j] % mod
                res[i][j] %= mod
    return res

@lru_cache(None)
def GETSWAP(a, b):
    res = [[0 for _ in range(3)] for _ in range(3)]
    res[a][b] = res[b][a] = 1
    res[3 - a - b][3 - a - b] = 1
    return res

@lru_cache(None)
def GETTOT(a, b):
    res = [[0 for _ in range(3)] for _ in range(3)]
    res[a][b] = 1
    res[b][b] = 1
    res[3 - a - b][3 - a - b] = 1
    return res

@lru_cache(None)
def GETMUL(a):
    res = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        if i == a:
            res[i][i] = 2
        else:
            res[i][i] = 1
    return res

@lru_cache(None)
def GetE(val):
    res = [[0 for _ in range(3)] for _ in range(3)]
    res[val][val] = 1
    return res

ID = [[0 for _ in range(3)] for _ in range(3)]
for i in range(3):
    ID[i][i] = 1

# print(MAP(GetE(0), GETTOT(0, 1)))

# @TIME
def solve(testcase):
    n, m = MI()
    nums = LII()
    sg = LazySegmentTree([GetE(num - 1) for num in nums], OP, [[0 for _ in range(3)] for _ in range(3)], MAP, COMP, ID)
    # for i in range(n):
    #     print(sg.get(i))
    
    for _ in range(m):
        ops = LII()
        if ops[2] == 1:
            l, r, op, a, b = ops
            a -= 1
            b -= 1
            l -= 1
            r -= 1 
            sg.apply(l, r + 1, GETSWAP(a, b))
        elif ops[2] == 2:
            # print('ops', ops)
            l, r, op, a, b = ops
            # print('2222', l, r, a, b)
            a -= 1
            b -= 1
            l -= 1
            r -= 1
            # print('lr', l, r)
            sg.apply(l, r + 1, GETTOT(a, b))
            # for i in range(n):
            #     print(sg.get(i))
        else:
            l, r, op, a = ops
            l -= 1
            r -= 1
            a -= 1
            sg.apply(l, r + 1, GETMUL(a))
        
        # print('-------------------')
        # for i in range(n):
        #     print(sg.get(i))
        res = [0 for _ in range(3)]
        tmp = sg.all_prod()
        for i in range(3):
            for j in range(3):
                res[j] += tmp[i][j]
                res[j] %= mod
        
        print(*res)

for testcase in range(1):
    solve(testcase)