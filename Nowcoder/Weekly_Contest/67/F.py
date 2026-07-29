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
#------------------------------FastIO---------------------------------
from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
from time import *
from random import *
from math import log, gcd, sqrt, ceil
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

inf = float('inf')
fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class SparseTable:
    def __init__(self, values: list, operation, identity):
        self.n = len(values)
        self.operation = operation
        self.identity = identity
        self.values = values
       
        self.log2 = [0] * (self.n + 1)
        self.log2[1] = 0
        for i in range(2, self.n + 1):
            self.log2[i] = self.log2[i >> 1] + 1
       
        self.max_power = self.log2[self.n] if self.n > 0 else 0
       
        self.info = [[self.identity] * (self.max_power + 1) for _ in range(self.n)]
       
        for i in range(self.n):
            self.info[i][0] = self.values[i]
       
        for j in range(1, self.max_power + 1):
            for i in range(self.n):
                right_start = i + (1 << (j - 1))
                if right_start < self.n:
                    self.info[i][j] = self.operation(
                        self.info[i][j - 1],
                        self.info[right_start][j - 1]
                    )
   
    def query(self, left: int, right: int):
        if left > right:
            return self.identity
        length = right - left + 1
        k = self.log2[length]
        left_result = self.info[left][k]
        right_start = right - (1 << k) + 1
        right_result = self.info[right_start][k]
        return self.operation(left_result, right_result)
   
    def range_max(self, left: int, right: int) -> int:
        return self.query(left, right)

def solve(testcase):
    n = II()
    A = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v, w = MI()
        u -= 1
        v -= 1
        A[u].append((v, w))
        A[v].append((u, w))
    
    IN = [0] * n
    OUT = [0] * n
    VAL = [0] * n
    DEP = [0] * n

    nodes = defaultdict(list)

    ins = defaultdict(list)
    
    dfn = -1
    
    @bootstrap
    def dfs(u, fa, d=0):
        nonlocal dfn
        dfn += 1
        IN[u] = dfn
        nodes[d].append(u)
        ins[d].append(dfn)
        DEP[u] = d
        for v, w in A[u]:
            if v == fa:
                continue
            VAL[v] = VAL[u] + w
            yield dfs(v, u, d + 1)
        OUT[u] = dfn
        yield
    
    dfs(0, -1)
    

    mp2 = {}
    for dep in nodes:
        vals = [VAL[u] for u in nodes[dep]]
        mp2[dep] = SparseTable(vals, fmax, -inf)
    
    q = II()
    for _ in range(q):
        u, k = MI()
        u -= 1
        nd = DEP[u] + k
        
        if nd not in ins:
            print(-1)
            continue
        
        L, R = IN[u], OUT[u]
        il = bisect_left(ins[nd], L)
        ir = bisect_right(ins[nd], R)
        
        if il >= ir:
            print(-1)
        else:
            print(mp2[nd].range_max(il, ir - 1) - VAL[u])

for testcase in range(1):
    solve(testcase)