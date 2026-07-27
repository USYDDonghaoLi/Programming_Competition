'''
Hala Madrid!
https://github.com/USYDDonghaoLi/Programming_Competition
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

#------------------------------FastIO---------------------------------

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

class TrieNode:

    
    def __init__(self):
        self.children = [None] * 36   
        self.is_end = 0               
        self.cnt = 0                  
    
    def _idx(self, ch: str) -> int:
        if '0' <= ch <= '9':
            return ord(ch) - ord('0')
        return ord(ch) - ord('a') + 10
    
    def insert(self, word: str) -> int:

        node = self
        node.cnt += 1
        for ch in word:
            idx = self._idx(ch)
            if not node.children[idx]:
                node.children[idx] = TrieNode()
            node = node.children[idx]
            node.cnt += 1
        node.is_end += 1
        return node.is_end
    
    def delete(self, word: str) -> None:
        node = self
        for ch in word:
            idx = self._idx(ch)
            if not node.children[idx] or node.children[idx].cnt == 0:
                return
            node = node.children[idx]
        if node.is_end == 0:
            return
        
        node = self
        node.cnt -= 1
        for ch in word:
            idx = self._idx(ch)
            node = node.children[idx]
            node.cnt -= 1
        node.is_end -= 1
    
    def search(self, word: str) -> int:
        node = self
        for ch in word:
            idx = self._idx(ch)
            if not node.children[idx]:
                return 0
            if node.children[idx].cnt == 0:
                return 0
            node = node.children[idx]
        return node.is_end
    
    def starts_with(self, prefix: str) -> bool:
        node = self
        if node.cnt == 0:
            return False
        for ch in prefix:
            idx = self._idx(ch)
            if not node.children[idx]:
                return False
            if node.children[idx].cnt == 0:
                return False
            node = node.children[idx]
        for ch in range(36):
            if node.children[ch] and node.children[ch].cnt > 0:
                return True
        return False


# @TIME
def solve(testcase):
    n = II()
    T = TrieNode()

    for _ in range(n):
        op, s = LI()
        if op == '1':
            print(T.insert(s))
        elif op == '2':
            flag = T.starts_with(s)
            print('YES' if flag else 'NO')
        else:
            T.delete(s)


for testcase in range(1):
    solve(testcase)