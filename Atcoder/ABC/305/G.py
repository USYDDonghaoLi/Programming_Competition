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

# '''
# 手写栈防止recursion limit
# 注意要用yield 不要用return
# 函数结尾要写yield None
# '''
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

# RANDOM = getrandbits(32)
 
# class Wrapper(int):
#     def __init__(self, x):
#         int.__init__(x)
 
#     def __hash__(self):
#         return super(Wrapper, self).__hash__() ^ RANDOM

mod = 998244353

class Matrix:

    def __init__(self, mat, mod) -> None:
        self.n = len(mat)
        self.m = len(mat[0])
        self.Mat = mat
        self.mod = mod
    
    def update(self, i, j, val):
        self.Mat[i][j] = val
    
    def add_ele(self, i, j, val):
        self.Mat[i][j] += val
        self.Mat[i][j] %= self.mod
    
    def get(self, i, j):
        return self.Mat[i][j]
    
    def __mul__(self, other):
        n2 = other.n
        m2 = other.m
        assert self.m == n2

        res = Matrix([[0 for _ in range(m2)] for _ in range(self.n)], self.mod)
        for i in range(self.n):
            for j in range(m2):
                x = 0
                for k in range(self.m):
                    x += self.Mat[i][k] * other.Mat[k][j] % self.mod
                    x %= self.mod
                res.update(i, j, x)
        
        return res

    @staticmethod
    def Quick_mat(matrix, power):
        assert matrix.n == matrix.m
        res = Matrix([[0 for _ in range(matrix.n)] for _ in range(matrix.n)], matrix.mod)
        for i in range(matrix.n):
            res.update(i, i, 1)
        A = Matrix(matrix.Mat, matrix.mod)
        while power:
            if power & 1:
                res *= A
            A *= A
            power >>= 1
        return res

    def __str__(self):
        string = ''
        for i in range(self.n):
            for j in range(self.m):
                string += str(self.Mat[i][j])
                if j != self.m - 1:
                    string += ' '
            if i != self.n - 1:
                string += '\n'
        return string


# @TIME
def solve(testcase):
    n, m = MI()
    words = [I() for _ in range(m)]

    def encode(string):
        ret = 0
        for s in string:
            ret <<= 1
            if s == 'a':
                ret ^= 1
        return ret

    def decode(state, LEN):
        ret = ''
        for k in range(LEN):
            if state >> k & 1:
                ret += 'a'
            else:
                ret += 'b'
        return ret[::-1]
    
    if n <= 6:
        res = 0
        for state in range(1 << n):
            word = decode(state, n)
            for w in words:
                if w in word:
                    break
            else:
                res += 1
        print(res)
        return

    # def check():
    #     res = 0
    #     for state in range(1 << n):
    #         word = decode(state, n)
    #         for w in words:
    #             if w in word:
    #                 break
    #         else:
    #             res += 1
    #     return res
    
    # print(check())

    matrix = Matrix([[0 for _ in range(64)] for _ in range(64)], mod)
    for i in range(64):
        state = i
        word = decode(state, 6)

        if any(w in word for w in words):
            continue

        word1 = word[1:] + 'a'
        for w in words:
            if w in word1:
                break
        else:
            newstate = encode(word1)
            assert decode(newstate,  6) == word1
            # print(word, word1)
            #matrix.update(newstate, state, 1)
            matrix.update(state, newstate, 1)
        
        word2 = word[1:] + 'b'
        for w in words:
            if w in word2:
                break
        else:
            newstate = encode(word2)
            # print(word, word2)
            #matrix.update(newstate, state, 1)
            matrix.update(state, newstate, 1)
    
    # for i in range(64):
    #     for j in range(64):
    #         if matrix.get(i, j):
    #             print(i, j, matrix.get(i, j))

    INIT = Matrix([[0] for _ in range(64)], mod)
    for i in range(64):
        state = i
        word = decode(state, 6)
        for w in words:
            if w in word:
                break
        else:
            INIT.update(i, 0, 1)
    
    final = Matrix.Quick_mat(matrix, n - 6) * INIT
    res = 0
    for i in range(64):
        res += final.Mat[i][0]
        res %= mod

    print(res)

for testcase in range(1):
    solve(testcase)