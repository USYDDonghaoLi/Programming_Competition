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
函数结尾要写yield None
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

mod = 10 ** 9 + 7

def solve(testcase):
    N = II()
    S = ' ' + I()

    '''
    insertion dp
    f[i][j]表示前i个数字为1-i的全排列，并且第i个数字是j且满足大小关系的方案数
    sum[i][j]表示第i个位置放置1-j的方案数之和

    当s[i]为<，且第i+1个位置为数字j时，我们需要找前一个数字小于j，且满足前面字符串关系的方案数
    （给前面的大于j的数都+1即可）
    f[i + 1][j] = \sum_{k = i} ^ {k = j - 1} f[i][k]
    当s[i]为>，且第i+1个位置为数字j时，我们需要找前一个数字小于j小于等于i+1，且满足前面字符串关系的方案数
    f[i + 1][j] = \sum_{k = j} ^ {k = i + 1} f[i][k]
    '''
    f = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
    s = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
    f[1][1] = 1
    for j in range(1, N + 1):
        s[1][j] = 1
    for i in range(1, N):
        for j in range(1, i + 2):
            if S[i] == '<':
                f[i + 1][j] += s[i][j - 1]
                f[i + 1][j] %= mod
            else:
                f[i + 1][j] += s[i][i + 1] - s[i][j - 1]
                f[i + 1][j] %= mod
        for j in range(1, N + 1):
            s[i + 1][j] = s[i + 1][j - 1] + f[i + 1][j]
            s[i + 1][j] %= mod
    
    res = 0
    for j in range(1, N + 1):
        res += f[N][j]
        res %= mod
    
    print(res)


for testcase in range(1):
    solve(testcase)