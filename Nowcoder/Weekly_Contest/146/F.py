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
def LGMI():
    return list(map(lambda x: int(x) - 1, input().split()))

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
from time import *
from random import *
from math import log, gcd, sqrt, ceil

inf = float('inf')
fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

def solve(testcase):
    n, a, b = MI()
    cards = LII()
    freq = [0] * 13
    for x in cards:
        freq[x - 1] += 1

    ans = 0
    for choice in product(range(3), repeat=13):
        rem = [freq[i] % 3 + choice[i] * 3 for i in range(13)]
        bulk = [freq[i] - rem[i] for i in range(13)]

        if max(rem) > 6:
            continue
        if min(bulk) < 0:
            continue

        s_rem = 0
        for i in range(2, 13):
            res = n
            for j in range(3):
                res = fmin(res, rem[i - j])
            s_rem += res
            for j in range(3):
                rem[i - j] -= res

        s_bulk = 0
        for i in range(2, 13):
            res = n
            for j in range(3):
                res = fmin(res, bulk[i - j])
            s_bulk += res
            for j in range(3):
                bulk[i - j] -= res

        triples = sum(x // 3 for x in bulk)
        ans = fmax(ans, s_rem * b + s_bulk * fmax(a, b) + triples * a)

    print(ans)

for testcase in range(1):
    solve(testcase)