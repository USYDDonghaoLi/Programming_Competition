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

import collections
def solve():
    A = list(map(int, input().split()))
    _ = int(input())
    B = list(map(int, input().split()))

    B = set(B)
    
    lst = []
    for ele in B:
        for j in range(6):
            lst.append((ele - A[j], ele))
    
    lst.sort()
    n = len(B)
    helper =  collections.defaultdict(lambda : 0)
    j = -1
    res = float('inf')

    m = len(lst)
    for i in range(m):
        while j + 1 < m and n > 0:
            j += 1
            helper[lst[j][1]] += 1
            if helper[lst[j][1]] == 1:
                n -= 1
        if n > 0:
            break
        
        res = min(res, lst[j][0] - lst[i][0])
        helper[lst[i][1]] -= 1
        if helper[lst[i][1]] == 0:
            n += 1
    
    print(res)
solve()