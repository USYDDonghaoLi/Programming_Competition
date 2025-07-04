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
def solve():
    n = II()
    A = LII()
    B = LII()

    def ops(arr1, arr2):
        n = len(arr1)
        to_ret = 0
        flag1 = flag2 = False
        t = arr1[0]
        idx = -1
        temp = float('inf')
        for i, v in enumerate(arr2):
            if temp > abs(v - t):
                temp = abs(v - t)
                idx = i
        if idx == 0:
            flag1 = True
        if idx == n - 1:
            flag2 = True
        to_ret += temp
        
        t = arr1[-1]
        if flag1:
            idx = -1
            temp = float('inf')
            for i, v in enumerate(arr2):
                if temp > abs(v - t):
                    temp = abs(v - t)
                    idx = i
            if idx == n - 1:
                flag2 = True
            to_ret += temp
        elif flag2:
            idx = -1
            temp = float('inf')
            for i, v in enumerate(arr2):
                if temp > abs(v - t):
                    temp = abs(v - t)
                    idx = i
            if idx == 0:
                flag2 = True
            to_ret += temp
        else:
            idx = -1
            temp = float('inf')
            for i, v in enumerate(arr2):
                if temp > abs(v - t):
                    temp = abs(v - t)
                    idx = i
            if idx == 0:
                flag1 = True
            if idx == n - 1:
                flag2 = True
            to_ret += temp
        
        if not flag1:
            t = arr2[0]
            idx = -1
            temp = float('inf')
            for i, v in enumerate(arr1):
                if temp > abs(v - t):
                    temp = abs(v - t)
                    idx = i
            to_ret += temp
        
        if not flag2:
            t = arr2[-1]
            idx = -1
            temp = float('inf')
            for i, v in enumerate(arr1[1: n - 1]):
                if temp > abs(v - t):
                    temp = abs(v - t)
                    idx = i
            to_ret += temp
        
        return to_ret
    
    to_ret = min(ops(A, B), ops(B, A))
    to_ret = min(to_ret, abs(A[0] - B[0]) + abs(A[-1] - B[-1]))
    to_ret = min(to_ret, abs(A[0] - B[-1]) + abs(B[0] - A[-1]))
    print(to_ret)

for _ in range(II()):solve()