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

# from types import GeneratorType
# def bootstrap(f, stack=[]):
#     def wrappedfunc(*args, **kwargs):
#         if stack:
#             return f(*args, **kwargs)
#         else:
#             to = f(*args, **kwargs)
#             while True:
#                 if type(to) is GeneratorType:
#                     stack.append(to)
#                     to = next(to)
#                 else:
#                     stack.pop()
#                     if not stack:
#                         break
#                     to = stack[-1].send(to)
#             return to
#     return wrappedfunc

# seed(19981220)
# RANDOM = getrandbits(64)
 
# class Wrapper(int):
#     def __init__(self, x):
#         int.__init__(x)

#     def __hash__(self):
#         return super(Wrapper, self).__hash__() ^ RANDOM

# def TIME(f):

#     def wrap(*args, **kwargs):
#         s = perf_counter()
#         ret = f(*args, **kwargs)
#         e = perf_counter()

#         print(e - s, 'sec')
#         return ret
    
#     return wrap

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class ACAM:
    
    '''
    给定一个文本串，看每个模式串出现了几次
    这里默认字符串都是小写的
    '''
    
    def __init__(self, n) -> None:
        '''
        n: 模式字符串总长度
        '''
        self.n = n
        self.nxt = [[0 for _ in range(self.n)] for _ in range(26)]
        self.fail = [0 for _ in range(self.n)]
        self.cnt =[0 for _ in range(self.n)]
        self.a = [0 for _ in range(self.n)]
        self.id = [0 for _ in range(self.n)]
        
        self.root = 0
        self.idx = 0
        self.timer = 0
    
    def clear(self):
        for i in range(26):
            self.nxt[i][0] = 0
        self.root = 0
        self.idx = 0
    
    def newnode(self):
        self.idx += 1
        for i in range(26):
            self.nxt[i][self.idx] = 0
        return self.idx

    def insert_char(self, pre, ch):
        if not self.nxt[ch][pre]:
            self.nxt[ch][pre] = self.newnode()
        return self.nxt[ch][pre]

    def insert_string(self, s, u):
        '''
        s: 插入的模式串
        u: 第几个模式串
        '''
        now = self.root
        for c in s:
            now = self.insert_char(now, ord(c) - 97)
        self.id[u] = now
        return self.id[u]

    def build(self):
        self.fail[self.root] = self.root
        q = deque()
        for i in range(26):
            if self.nxt[i][0]:
                q.append(self.nxt[i][0])
        
        while q:
            h = q.popleft()
            self.a[self.timer] = h
            self.timer += 1
            
            for i in range(26):
                if not self.nxt[i][h]:
                    self.nxt[i][h] = self.nxt[i][self.fail[h]]
                else:
                    tmp = self.nxt[i][h]
                    self.fail[tmp] = self.nxt[i][self.fail[h]]
                    q.append(tmp)
    
    def solve(self, s, m):
        '''
        s: 匹配的文本串
        m: 一共有多少个模式串
        '''
        now = self.root
        for c in s:
            now = self.nxt[ord(c) - 97][now]
            self.cnt[now] += 1
        
        for i in range(self.timer, -1, -1):
            self.cnt[self.fail[self.a[i]]] += self.cnt[self.a[i]]
        
        return [self.cnt[self.id[i]] for i in range(m)]

# @TIME
def solve(testcase):
    n = II()
    ac = ACAM(200010)
    
    for i in range(n):
        ac.insert_string(I(), i)
    
    ac.build()
    s = I()
    
    res = ac.solve(s, n)
    
    print('\n'.join(map(str, res)))

for testcase in range(1):
    solve(testcase)