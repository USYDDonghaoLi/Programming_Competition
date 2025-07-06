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

def II():
    return int(input())

def MI():
    return map(int, input().split())

from math import acos, sqrt, pi, sin
from random import *

def intersection(r1, r2, d):
    if d >= r1 + r2:
        return 0.0
    if d <= abs(r1 - r2): 
        return pi * min(r1, r2) ** 2
    
    cos_theta1 = (r1 ** 2 + d ** 2 - r2 ** 2) / (2 * r1 * d)
    cos_theta2 = (r2 ** 2 + d ** 2 - r1 ** 2) / (2 * r2 * d)
    cos_theta1 = min(1.0, max(-1.0, cos_theta1))
    cos_theta2 = min(1.0, max(-1.0, cos_theta2))
    
    theta1 = acos(cos_theta1)
    theta2 = acos(cos_theta2)
    
    area = r1 ** 2 * (theta1 - 0.5 * sin(2 * theta1)) + r2 ** 2 * (theta2 - 0.5 * sin(2 * theta2))
    return area

def circle(r1, r2, d):
    if d >= r1 + r2 or d <= abs(r1 - r2):
        return 0.0
    r_in = (r1 + r2 - d) / 2
    return pi * r_in ** 2

def generate():
    return [randint(1, 1000) for _ in range(6)]

def solve(testcase):
    x1, y1, r1, x2, y2, r2 = generate()
    # x1, y1, r1, x2, y2, r2 = MI()
    d = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    if d == 0:
        print(0)
        return
    print(round(intersection(r1, r2, d) - circle(r1, r2, d)))

for testcase in range(II()):
    solve(testcase)