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

#------------------------------FastIO---------------------------------

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
from time import *
from random import *
from math import log, gcd, sqrt, ceil

'''
手写栈防止recursion limit
注意要用yield 不要用return
'''
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

'''
max(***), mp可能为空 -> error
'''

def answer(s):
    print(s, flush = True)

def go(x, y):
    print(x, y, flush = True)

def solve():
    n, l, r = MI()
    if l < r or not (n ^ l) & 1:
        answer('First')
        if (n ^ l) & 1:
            l += 1
        k = n - l >> 1
        go(k + 1, l)
        rx, ry = MI()
        
        while rx:
            if rx > (n >> 1):
                go(rx - (n - k), ry)
                rx, ry = MI()
            else:
                go(rx + (n - k), ry)
                rx, ry = MI()
            
    else:
        #长度为i的sg#
        sg = [0 for _ in range(n + 1)]
        for i in range(l, n + 1):
            mp = defaultdict(int)
            left = i - l
            for j in range(left + 1):
                mp[sg[j] ^ sg[left - j]] += 1
            for j in range(10 ** 9):
                if not mp[j]:
                    sg[i] = j
                    break
        
        # print('sg', sg)
        if sg[-1]:
            answer('First')
            rx, ry = 0, 0

        else:
            answer('Second')
            rx, ry = MI()
        
        used = [1 for _ in range(n + 1)]
        used[0] = 0

        while True:
            for i in range(rx, rx + ry):
                used[i] = 0
            sg_tot = 0
            L, R = 0, 0
            intervals = []
            while R < n + 1:
                while R < n + 1 and not used[R]:
                    R += 1
                L = R
                if R == n + 1:
                    break
                while R < n + 1 and used[R]:
                    R += 1
                sg_tot ^= sg[R - L]
                intervals.append([L, R - 1])
                L = R
            # print('intervals', intervals)
            # print('sgtot', sg_tot)
            # print('l', l)
            
            ansl, ansr = -1, -1
            for L, R in intervals:
                LEN = R - L + 1
                #左端点#
                for j in range(LEN - l + 1):
                    if j + l - 1 > R:
                        break
                    sg_new = sg_tot ^ sg[R - L + 1] ^ sg[j] ^ sg[LEN - l - j]
                    # print(j, sg[j], LEN - l, sg[LEN - l], sg_new)
                    if not sg_new:
                        ansl, ansr = L + j, l
                        break
                if ansl != -1:
                    break
            
            go(ansl, ansr)
            for i in range(ansl, ansl + ansr):
                used[i] = False
            rx, ry = MI()
            if not rx:
                break
        
for _ in range(1):solve()