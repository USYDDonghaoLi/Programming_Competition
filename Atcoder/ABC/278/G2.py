import random
import sys
import os
import math
from collections import Counter, defaultdict, deque
from functools import lru_cache, reduce
from itertools import accumulate, combinations, permutations
from heapq import nsmallest, nlargest, heapify, heappop, heappush
from io import BytesIO, IOBase
from copy import deepcopy
import threading
import bisect
BUFSIZE = 4096


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

sys.stdin = IOWrapper(sys.stdin)
sys.stdout = IOWrapper(sys.stdout)
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

n, l, r = MI()
if r > l or not (n ^ l) & 1:
    print('First')
    tmp = l
    if (n - l) % 2 != 0:
        tmp += 1
    print((n - tmp) // 2 + 1, tmp)
    sys.stdout.flush()
    dist = (n - tmp) // 2 + tmp
    while True:
        x, y = MI()
        if x == y == 0:
            exit()
        if x <= (n - tmp) // 2:
            print(x + dist, y)
        else:
            print(x - dist, y)
        sys.stdout.flush()
else:
    @lru_cache(None)
    def sg(num):
        if num < l: return 0
        set_ = set()
        for i in range(num - l + 1):
            set_.add(sg(i) ^ sg(num - l - i))
        mex = 0
        while mex in set_:
            mex += 1
        return mex
    if sg(n):
        print('First')
        for i in range(n - l + 1):
            if sg(i) ^ sg(n-l-i) == 0:
                print(i+1, l)
                if i:
                    intervals = [[1, i], [i + l + 1, n]]
                    lengths = [i, n-l-i]
                    sgs = [sg(i), sg(n-l-i)]
                else:
                    intervals = [[l + 1, n]]
                    lengths = [n-l]
                    sgs = [sg(n-l)]
                break
    else:
        print('Second')
        intervals = [[1, n]]
        lengths = [n]
        sgs = [sg(n)]
    sys.stdout.flush()
    while True:
        x, y = MI()
        if x == y == 0: exit()
        for i, (m, n) in enumerate(intervals):
            assert x + y <= n
            if x <= n:
                interval = []
                length = []
                g = []
                if x - m >= l:
                    interval.append([m, x-1])
                    length.append(x - m)
                    g.append(sg(x-m))
                if n - x - y + 1 >= l:
                    interval.append([x + y, n])
                    length.append(n - x - y + 1)
                    g.append(sg(n-x-y+1))
                intervals[i:i+1] = interval
                lengths[i:i+1] = length
                sgs[i:i+1] = g
                break
        #print('1', intervals, lengths, sgs)
        tot = reduce(lambda x, y: x ^ y, sgs)
        for i, v in enumerate(lengths):
            for j in range(v - l + 1):
                print('info', v, j, v - l - j)
                if tot ^ sg(v) ^ sg(j) ^ sg(v - l - j) == 0:
                    x, y = intervals[i][0] + j, l
                    break
        print(x, y)
        sys.stdout.flush()
        for i, (m, n) in enumerate(intervals):
            if x <= n:
                interval = []
                length = []
                g = []
                if x - m >= l:
                    interval.append([m, x-1])
                    length.append(x - m)
                    g.append(sg(x-m))
                if n - x - y + 1 >= l:
                    interval.append([x + y, n])
                    length.append(n - x - y + 1)
                    g.append(sg(n-x-y+1))
                intervals[i:i+1] = interval
                lengths[i:i+1] = length
                sgs[i:i+1] = g
                break
        #print('2', intervals, lengths, sgs)