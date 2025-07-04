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
#dfs - stack#
#check top!#

class lazy_segtree():
    def update(self,k):self.d[k]=self.op(self.d[2*k],self.d[2*k+1])
    def all_apply(self,k,f):
        self.d[k]=self.mapping(f,self.d[k])
        if (k<self.size):self.lz[k]=self.composition(f,self.lz[k])
    def push(self,k):
        self.all_apply(2*k,self.lz[k])
        self.all_apply(2*k+1,self.lz[k])
        self.lz[k]=self.identity
    #d -> vals lz -> lazy#
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

#update 0, 1, 2, [1, 0], [2, 1], [2, 0]#
def op(x,y):
	ret=[0]*6
	ret[0]=x[0]+y[0]
	ret[1]=x[1]+y[1]
	ret[2]=x[2]+y[2]
	ret[3]=x[3]+y[3]+x[1]*y[0]
	ret[4]=x[4]+y[4]+x[2]*y[0]
	ret[5]=x[5]+y[5]+x[2]*y[1]
	return ret


#0, 1, 2 -> x, y, z : f(0, 1, 2) -> x, y, z#
def mapping(f,x):
    #calculating count of 0, 1, 2 after mapping
	ret=[0]*6
	ret[f[0]]+=x[0]
	ret[f[1]]+=x[1]
	ret[f[2]]+=x[2]

    #cnt calaculates number of pairs[(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]#
	cnt=[[0]*3 for _ in range(3)]
	cnt[f[1]][f[0]]+=x[3]
	cnt[f[2]][f[0]]+=x[4]
	cnt[f[2]][f[1]]+=x[5]
	cnt[f[0]][f[1]]+=x[0]*x[1]-x[3]
	cnt[f[0]][f[2]]+=x[0]*x[2]-x[4]
	cnt[f[1]][f[2]]+=x[1]*x[2]-x[5]

    #update ret as new outcome
	ret[3]=cnt[1][0]
	ret[4]=cnt[2][0]
	ret[5]=cnt[2][1]
	return ret

#calculating function of f * g -> lazynode#
def composition(f,g):
	ret=[0]*3
	ret[0]=f[g[0]]
	ret[1]=f[g[1]]
	ret[2]=f[g[2]]
	return ret

#initial value of values#
e = [0] * 6
#initial value of lazynode#
id = [0,1,2]

def solve():
    n, q = MI()
    V = [[0 for _ in range(6)] for _ in range(n)]
    A = LII()
    for i, a in enumerate(A):
        V[i][a] = 1
    
    segtree = lazy_segtree(V, op, e, mapping, composition, id)

    for _ in range(q):
        t, l, r, *a = MI()
        l -= 1
        if t == 1:
            print(sum(segtree.prod(l, r)[3:]))
        else:
            segtree.apply(l, r, a)

for _ in range(1):solve()