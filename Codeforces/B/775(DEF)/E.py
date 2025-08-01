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

#------------------------------FastIO---------------------------------

MOD = 998244353
facts = [0]
for i in range(1, 200001):
    facts.append(facts[-1] * i % MOD)
invs = [0]
for i in range(1, 200001):
    invs.append(pow(facts[i], MOD - 1, MOD))
def cnm(n, m):
    return facts[n] * invs[m] * invs[m] % MOD 
def inv(n):
    return pow(n, MOD - 1, MOD)

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0 for _ in range(n)]
        self.lst = [0 for _ in range(n)]
    def lowbit(self, x):
        return x & (-x)
    def update(self, pos, x):
        while pos < self.n:
            self.tree[pos] += x
            pos += self.lowbit(pos)
        self.lst[pos] += x
    def query(self, pos):
        to_ret = 0
        while pos:
            to_ret += self.tree[pos]
            pos -= self.lowbit(pos)
        return to_ret
    def query_sum(self, l, r):
        return self.query(r) - self.query(l - 1)

def solve():
    n, m = MI()
    a = LII()
    b = LII()
    flag = 0
    if n < m:
        flag = 1
        b = b[:n]
    if n > m:
        flag = -1

    ft = FenwickTree(200001)
    for num in a:
        ft.update(num, 1)

    du = 1
    for num in range(1, n + 1):
        if ft.lst[num]:
            print(ft.lst[num])
            du *= ft.lst[num]
        du %= MOD
    print(du)

#     to_ret = 0
#     a = n
#     for num in b:
#         if not ft.query_sum(num, num):
#             temp = ft.query_sum(1, num)
#             to_ret += temp * (facts[a - 1] * inv(du))
#             to_ret %= MOD
#             a -= 1
#             break
        
#         else:
#             temp = ft.query_sum(1, num - 1)
#             ft.update(num, -1)
#             hp = ft.query_sum(num, num)
#             if hp:
#                 du *= inv(hp + 1)
#                 du * hp
#             to_ret += temp * (facts[a - 1] * inv(du))
#             to_ret %= MOD
#             a -= 1
    
#     print(to_ret + flag)
solve()
            