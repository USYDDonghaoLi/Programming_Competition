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

def ask(l, r):
    print('?', l, r, flush = True)
    return II()

def answer(ans):
    print('!', ans, flush = True)

def solve():
    n = II()
    lst = [i for i in range(1, (1 << n) + 1)]

    while len(lst) > 1:
        if len(lst) == 2:
            a, b = lst
            ret = ask(a, b)
            if ret == 1:
                answer(a)
                return
            else:
                answer(b)
                return

        temp = []
        idx = 0
        while idx < len(lst):
            #print('lst', lst)
            a, b, c, d = lst[idx], lst[idx + 1], lst[idx + 2], lst[idx + 3]
            ret1 = ask(a, d)
            if ret1 == 1:
                ret2 = ask(a, c)
                if ret2 == 1:
                    temp.append(a)
                else:
                    temp.append(c)
            elif ret1 == 0:
                ret2 = ask(b, c)
                if ret2 == 1:
                    temp.append(b)
                else:
                    temp.append(c)
            else:
                ret2 = ask(b, d)
                if ret2 == 1:
                    temp.append(b)
                else:
                    temp.append(d)
            idx += 4
        if len(temp) == 1:
            answer(temp[0])
            return
        lst = temp

for _ in range(II()):solve()