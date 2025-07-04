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

class FenwickTree_min:
    def __init__(self,n):
        self.tree=[float('inf') for _ in range(n)]
        self.nums=[float('inf') for _ in range(n)]
        self.n=n
    
    def lowbit(self,x):
        return x & (-x)
    
    def update(self,idx,val):
        self.nums[idx]=val
        while idx < self.n:
            #print('iidx', idx, 'n', self.n)
 
            if self.tree[idx]<=val:break
            self.tree[idx]=val
        
            gap=1
            while gap<self.lowbit(idx):
                if self.tree[idx-gap]<self.tree[idx]:self.tree[idx]=self.tree[idx-gap]
                gap<<=1
 
            idx+=self.lowbit(idx)
        
 
    def query(self,l,r):
        ans=float('inf')
        while 1:
            if ans>self.nums[r]:ans=self.nums[r]
            if l==r:break
 
            r-=1
            while r-l>self.lowbit(r):
                if self.tree[r]<ans:ans=self.tree[r]
                r-=self.lowbit(r)
        return ans

from bisect import *
def solve():
    n, C = MI()
    helper = [0 for _ in range(C + 1)]
    for _ in range(n):
        c, d, h = MI()
        helper[c] = max(helper[c], d * h)
    
    for c in range(1, C + 1):
        helper[c] = max(helper[c], helper[c - 1])
        for k in range(2, C + 1):
            if c * k > C:
                break
            else:
                helper[c * k] = max(helper[c * k], helper[c] * k)

    res = []
    m = II()
    for _ in range(m):
        d, h = MI()
        idx = bisect_right(helper, d * h)
        if idx == C + 1:
            res.append(-1)
        else:
            res.append(idx)

    print(*res)
solve() 