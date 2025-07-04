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

from collections import *
from heapq import *
def solve():
    n = II()
    P = LII()
    A = LII()

    sp = set(P)
    r = (max(A) - n) // (n - len(sp))
    if r == 0:
        print(*A)
        return
    
    m = r.bit_length()
    #print(r, m)

    st = [[-1 for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        st[i][0] = P[i - 1]
    for j in range(1, m):
        for i in range(1, n + 1):
            st[i][j] = st[st[i][j - 1]][j - 1]
    #print(st)

    froms = defaultdict(list)
    cur = [i for i in range(n + 1)]
    for i in range(m, -1, -1):
        if (r >> i) & 1:
            for j in range(1, n + 1):
                cur[j] = st[cur[j]][i]
    #print('cur', cur)
    for i, v in enumerate(cur):
        if i == 0:
            continue
        heappush(froms[v], i)
    #print('froms', froms)

    #minval -> idx#
    helper_mn =  defaultdict(list)
    pq_values = []
    for v in froms:
        hv = A[v - 1]
        helper_mn[hv] = froms[v]
    #print('min', helper_mn)

    res = [-1 for _ in range(n + 1)]
    S = set()
    for v in helper_mn:
        idx = heappop(helper_mn[v])
        res[idx] = v
        S.add(v)
        if helper_mn[v]:
            heappush(pq_values, v)
    #print('res', res)
    #print('S', S)
    #print('pq', pq_values)

    cur = 1
    pq = []
    while cur <= n:
        while pq_values and pq_values[0] <= cur:
            val = heappop(pq_values)
            for idx in helper_mn[val]:
                heappush(pq, idx)
        #print(cur, pq)

        if cur in S:
            cur += 1
            continue
        else:
            if not pq:
                break
            idx = heappop(pq)
            res[idx] = cur
            S.add(cur)
            cur += 1
            #print('res', res)
            continue
    
    cur = 1
    idx = 1
    while cur <= n:
        if cur not in S:
            while idx <= n:
                if res[idx] > n:
                    res[idx] = cur
                    idx += 1
                    break
                else:
                    idx += 1
            cur += 1
        else:
            cur += 1
    print(*res[1:])
solve()