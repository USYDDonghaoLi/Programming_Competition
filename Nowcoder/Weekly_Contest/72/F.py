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

def get_eo(L, R):
    if L > R:
        return 0, 0
    tot = R - L + 1
    if L % 2 == 0:
        e = (tot + 1) // 2
        o = tot // 2
    else:
        o = (tot + 1) // 2
        e = tot // 2
    return e, o

class Node:
    __slots__ = ['l', 'r', 'e1', 'o1', 'assign', 'flip']
    def __init__(self):
        self.l = self.r = None
        self.e1 = self.o1 = 0
        self.assign = -1
        self.flip = 0

def apply(node, L, R, ass, flp):
    if ass != -1:
        e, o = get_eo(L, R)
        node.e1 = e if ass else 0
        node.o1 = o if ass else 0
        node.assign = ass
        node.flip = 0
    if flp:
        e, o = get_eo(L, R)
        node.e1 = e - node.e1
        node.o1 = o - node.o1
        if node.assign != -1:
            node.assign ^= 1
        else:
            node.flip ^= 1

def push(node, L, R):
    if node.assign == -1 and node.flip == 0:
        return
    mid = (L + R) // 2
    if node.l is None:
        node.l = Node()
    if node.r is None:
        node.r = Node()
    apply(node.l, L, mid, node.assign, node.flip)
    apply(node.r, mid + 1, R, node.assign, node.flip)
    node.assign = -1
    node.flip = 0

def pull(node):
    node.e1 = (node.l.e1 if node.l else 0) + (node.r.e1 if node.r else 0)
    node.o1 = (node.l.o1 if node.l else 0) + (node.r.o1 if node.r else 0)

def upd_ass(node, L, R, ql, qr, val):
    if R < ql or L > qr:
        return
    if ql <= L and R <= qr:
        apply(node, L, R, val, 0)
        return
    if node.l is None:
        node.l = Node()
    if node.r is None:
        node.r = Node()
    push(node, L, R)
    mid = (L + R) // 2
    upd_ass(node.l, L, mid, ql, qr, val)
    upd_ass(node.r, mid + 1, R, ql, qr, val)
    pull(node)

def upd_flp(node, L, R, ql, qr):
    if R < ql or L > qr:
        return
    if ql <= L and R <= qr:
        apply(node, L, R, -1, 1)
        return
    if node.l is None:
        node.l = Node()
    if node.r is None:
        node.r = Node()
    push(node, L, R)
    mid = (L + R) // 2
    upd_flp(node.l, L, mid, ql, qr)
    upd_flp(node.r, mid + 1, R, ql, qr)
    pull(node)

def qry(node, L, R, ql, qr):
    if node is None or R < ql or L > qr:
        return 0, 0
    if ql <= L and R <= qr:
        return node.e1, node.o1
    if node.assign != -1 or node.flip != 0:
        push(node, L, R)
    mid = (L + R) // 2
    e1, o1 = qry(node.l, L, mid, ql, qr)
    e2, o2 = qry(node.r, mid + 1, R, ql, qr)
    return e1 + e2, o1 + o2

def solve(testcase):
    n, q = MI()
    root = Node()
    for _ in range(q):
        op, l, r = MI()
        if op == 1:
            upd_ass(root, 1, n, l, r, 1)
        elif op == 2:
            upd_flp(root, 1, n, l, r)
        else:
            e1, o1 = qry(root, 1, n, l, r)
            E, O = get_eo(l, r)
            print(min(e1 + O - o1, E - e1 + o1))

for testcase in range(1):
    solve(testcase)