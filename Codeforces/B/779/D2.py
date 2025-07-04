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

class Trie:
    N = 18
    def __init__(self) -> None:
        self.left = None
        self.right = None
    
    def insert(self, num):
        root = self
        for i in range(Trie.N - 1, -1 , -1):
            tag = (num >> i) & 1
            if not tag:
                if root.left == None:
                    root.left = Trie()
                root = root.left
            else:
                if root.right == None:
                    root.right = Trie()
                root = root.right
    
    def find(self, num):
        root = self
        for i in range(Trie.N - 1, -1, -1):
            tag = (num >> i) & 1
            if not tag:
                if root.left:
                    root = root.left
                else:
                    return False
            else:
                if root.right:
                    root = root.right
                else:
                    return False
        return True


def solve():
    l, r = MI()
    A = LII()
    print (check(A, l, r))

def check(A, l, r):
    if (r - l) % 2 == 0:
        ans = 0
        for i in range(l, r + 1): ans ^= i
        for x in A: ans ^= x
        return ans
    else:
        A_set = set(A)
        borders = []
        for x in A_set:
            if (x ^ 1) not in A_set:
                borders += [x^l]
 
        if r == l + 1:
            borders = [A[0]^l, A[1]^l]
 
        if len(borders) == 2:
            for cand in borders:
                if set([cand^i for i in range(l, r + 1)]) == A_set: return cand
        else:
            A2 = list(set([x // 2 for x in A]))
            return check(A2, l // 2, (r - 1) // 2) << 1
            

for _ in range(II()):solve()
