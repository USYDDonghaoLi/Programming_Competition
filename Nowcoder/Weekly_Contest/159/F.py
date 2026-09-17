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

mod = 10 ** 9 + 7

class FenwickTree:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def _lowbit(self, x: int) -> int:
        return x & (-x)

    def update(self, pos: int, delta: int) -> None:
        delta %= mod
        while pos <= self.n:
            self.tree[pos] = (self.tree[pos] + delta) % mod
            pos += self._lowbit(pos)

    def query(self, pos: int) -> int:
        result = 0
        while pos > 0:
            result += self.tree[pos]
            pos -= self._lowbit(pos)
        return result % mod

    def range_add(self, left: int, right: int, delta: int) -> None:
        # 1-indexed inclusive
        if left > right:
            return
        self.update(left, delta)
        if right + 1 <= self.n:
            self.update(right + 1, -delta)

    def point_query(self, pos: int) -> int:
        return self.query(pos)


def solve():
    n, q = MI()
    s = I()
    A = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = GMI()
        A[u].append(v)
        A[v].append(u)

    DEP = [0] * n
    IN = [0] * n
    OUT = [0] * n
    t = 0

    @bootstrap
    def dfs(u, fa):
        nonlocal t
        IN[u] = t
        for v in A[u]:
            if v != fa:
                DEP[v] = DEP[u] + 1
                t += 1
                yield dfs(v, u)
        OUT[u] = t
        yield

    dfs(0, -1)

    pw = [1] * n
    for i in range(1, n):
        pw[i] = (pw[i - 1] << 1) % mod

    # 欧拉序 0..n-1 -> BIT 的 1..n；开 n+1 是为了差分的 right+1
    bit = FenwickTree(n + 1)
    cur = [1 if ch == '1' else 0 for ch in s]
    for i in range(n):
        if cur[i]:
            bit.range_add(IN[i] + 1, OUT[i] + 1, pw[DEP[i]])

    out = []
    for _ in range(q):
        op, x = LI()
        x = int(x) - 1
        if op == 'Q':
            out.append(str(bit.point_query(IN[x] + 1)))
        else:
            cur[x] ^= 1
            delta = pw[DEP[x]] if cur[x] else -pw[DEP[x]]
            bit.range_add(IN[x] + 1, OUT[x] + 1, delta)
    print('\n'.join(out))


solve()