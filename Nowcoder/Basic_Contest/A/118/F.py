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

mod = 10 ** 9 + 7

# class Matrix:
#     def __init__(self, n, m):
#         self.n = n
#         self.m = m
#         self.mat = [[0] * self.m for _ in range(self.n)]
#         self.mod = mod
    
#     def build(self, mat):
#         '''
#         initialize matrix
#         '''
#         assert len(mat) == self.n and len(mat[0]) == self.m, "Matrix dimensions must agree"
#         for i in range(self.n):
#             for j in range(self.m):
#                 self.mat[i][j] = mat[i][j]
#         return self
    
#     def setMod(self, mod):
#         '''
#         update mod
#         '''
#         self.mod = mod
    
#     def __getitem__(self, index):
#         row, col = index
#         return self.mat[row][col]

#     def __setitem__(self, index, value):
#         row, col = index
#         self.mat[row][col] = value
    
#     def __iter__(self):
#         self.current_col = 0
#         self.current_row = 0
#         return self
    
#     def __next__(self):
#         if self.current_row >= self.n:
#             raise StopIteration
#         value = self.mat[self.current_row][self.current_col]
#         self.current_col += 1
#         if self.current_col == self.m:
#             self.current_row += 1
#             self.current_col = 0
#         return value

#     def build_identity(self, lim):
#         '''
#         initialize matrix as I
#         '''
#         for i in range(lim + 1):
#             self.mat[i][i] = 1
#         return self

#     def __mul__(self, other):
#         assert self.m == other.n, "Matrix dimensions must agree"
#         result = Matrix(self.n, other.m)
        
#         if self.mod:
#             for i in range(self.n):
#                 for j in range(other.m):
#                     for k in range(self.m):
#                         result.mat[i][j] += self.mat[i][k] * other.mat[k][j] % self.mod
#                         result.mat[i][j] %= self.mod
#         else:
#             for i in range(self.n):
#                 for j in range(other.m):
#                     for k in range(self.m):
#                         result.mat[i][j] += self.mat[i][k] * other.mat[k][j]
                        
#         return result

#     def __add__(self, other):
#         assert self.n == other.n and self.m == other.m, "Matrix dimensions must agree"
#         result = Matrix(self.n, self.m)
        
#         if self.mod:
#             for i in range(self.n):
#                 for j in range(self.m):
#                     result.mat[i][j] = (self.mat[i][j] + other.mat[i][j]) % self.mod
#         else:
#             for i in range(self.n):
#                 for j in range(self.m):
#                     result.mat[i][j] = self.mat[i][j] + other.mat[i][j]
                    
#         return result

#     def __sub__(self, other):
#         assert self.n == other.n and self.m == other.m, "Matrix dimensions must agree"
#         result = Matrix(self.n, self.m)
        
#         if self.mod:
#             for i in range(self.n):
#                 for j in range(self.m):
#                     result.mat[i][j] = (self.mat[i][j] - other.mat[i][j]) % self.mod
#         else:
#             for i in range(self.n):
#                 for j in range(self.m):
#                     result.mat[i][j] = self.mat[i][j] - other.mat[i][j]
                    
#         return result

#     def qpow_matrix(self, b):
#         res = Matrix(self.n, self.n)
#         res.build_identity(self.n - 1)
#         a = self
#         while b:
#             if b & 1:
#                 res = res * a
#             a = a * a
#             b >>= 1
#         return res

#     @staticmethod
#     def gauss(n, a):
#         '''
#         find solution of linear equations (float number)
#         '''
#         eps = 1e-8
#         c, r = 0, 0
#         for c in range(n):
#             cur = r
#             for j in range(r + 1, n):
#                 if abs(a[j][c]) > abs(a[cur][c]):
#                     cur = j
#             if abs(a[cur][c]) < eps:
#                 continue
#             a[r], a[cur] = a[cur], a[r]
#             for i in range(n, c - 1, -1):
#                 a[r][i] /= a[r][c]
#             for i in range(r + 1, n):
#                 if abs(a[i][c]) > eps:
#                     for j in range(n, c - 1, -1):
#                         a[i][j] -= a[r][j] * a[i][c]
#             r += 1
#         if r < n:
#             for i in range(r, n):
#                 if abs(a[i][n]) > eps:
#                     '''
#                     No Solution
#                     '''
#                     return 2
#             '''
#             Infinite solution
#             '''
#             return 1
        
#         for i in range(n - 1, -1, -1):
#             for j in range(i + 1, n):
#                 a[i][n] -= a[i][j] * a[j][n]
        
#         '''
#         Single solution    
#         '''
#         return [a[i][-1] for i in range(n)]

#     def gauss_jordan(self, n):
#         '''
#         find solution of linear equtaion (with mod)
#         '''
#         for i in range(n):
#             r = i
#             for j in range(i + 1, n):
#                 if self.mat[j][i] > self.mat[r][i]:
#                     r = j
#             if r != i:
#                 self.mat[i], self.mat[r] = self.mat[r], self.mat[i]
#             if not self.mat[i][i]:
#                 return False
#             inv = pow(self.mat[i][i], self.mod - 2, self.mod)
#             for k in range(n):
#                 if k == i:
#                     continue
#                 p = self.mat[k][i] * inv % self.mod
#                 '''
#                 因为求逆，取两倍
#                 '''
#                 for j in range(i, 2 * n):
#                     self.mat[k][j] = (self.mat[k][j] - p * self.mat[i][j] % self.mod ) % self.mod
#             for j in range(i, 2 * n):
#                 self.mat[i][j] = self.mat[i][j] * inv % self.mod
#         return True

#     def get_inv_matrix(self, n):
#         '''
#         get inverse matrix of current matrix
#         '''
#         extended_matrix = [row[:] + [1 if i == j else 0 for j in range(self.n)] for i, row in enumerate(self.mat)]
#         aug_matrix = Matrix(n, 2 * n)
#         aug_matrix.mat = extended_matrix
#         if aug_matrix.gauss_jordan(n):
#             inv_mat = Matrix(n, n)
#             for i in range(n):
#                 for j in range(n):
#                     inv_mat.mat[i][j] = aug_matrix.mat[i][j + n]
#             return inv_mat
#         else:
#             raise ValueError("Matrix is singular and cannot be inverted")
    
#     def determinant(self):
#         '''
#         calculate the determinant of the matrix
#         Caution: self.mod must be prime
#         '''
#         assert self.n == self.m, "Matrix must be square"
#         n = self.n
#         mat_copy = [row[:] for row in self.mat]
#         det = 1
#         for i in range(n):
#             pivot = i
#             for j in range(i + 1, n):
#                 if abs(mat_copy[j][i]) > abs(mat_copy[pivot][i]):
#                     pivot = j
#             if i != pivot:
#                 mat_copy[i], mat_copy[pivot] = mat_copy[pivot], mat_copy[i]
#                 det = -det
#             if mat_copy[i][i] == 0:
#                 return 0
#             det = det * mat_copy[i][i] % self.mod
#             inv = pow(mat_copy[i][i], self.mod - 2, self.mod)
#             assert inv * mat_copy[i][i] % self.mod == 1
#             for j in range(i + 1, n):
#                 factor = mat_copy[j][i] * inv % self.mod
#                 for k in range(i, n):
#                     mat_copy[j][k] = (mat_copy[j][k] - factor * mat_copy[i][k] % self.mod) % self.mod
#         return det % self.mod

#     def Determinant(self):
#         '''
#         calculate the determinant of the matrix for any mod
#         '''
#         res = 1
#         for c in range(self.n):
#             for r in range(c + 1, self.n):
#                 while self.mat[r][c]:
#                     self.mat[r], self.mat[c] = self.mat[c], self.mat[r]
#                     res *= -1
#                     if not self.mat[r][c]:
#                         break
#                     if self.mat[r][c] >= self.mat[c][c]:
#                         div = self.mat[r][c] // self.mat[c][c]
#                         for k in range(c, self.n):
#                             self.mat[r][k] = (self.mat[r][k] - div * self.mat[c][k]) % self.mod
#                     if not self.mat[r][c]:
#                         break
        
#         for i in range(self.n):
#             res = res * self.mat[i][i] % self.mod
        
#         return res
#         # res, w = 1, 1
        
#         # for i in range(self.n):
#         #     for j in range(i + 1, self.n):
#         #         while self.mat[i][i]:
#         #             div = self.mat[j][i] // self.mat[i][i]
#         #             for k in range(i, self.n):
#         #                 self.mat[j][k] -= div * self.mat[i][k] % self.mod
#         #                 self.mat[j][k] %= self.mod
#         #             self.mat[i], self.mat[j] = self.mat[j], self.mat[i]
#         #             w = -w
#         #         self.mat[i], self.mat[j] = self.mat[j], self.mat[i]
#         #         w = -w

#         # for i in range(self.n):
#         #     res = self.mat[i][i] * res % self.mod
        
#         # return w * res % self.mod

#     def __str__(self):
#         res = []
#         for i in range(self.n):
#             res.append(" ".join(map(str, self.mat[i])))
#         return "\n".join(res)

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

ZERO = [
    [2, 0, 0],
    [0, 1, 0],
    [1, 0, 1]
]

ONE = [
    [1, 1, 0],
    [0, 2, 0],
    [0, 1, 1]
]

# ZERO = Matrix(3, 3)
# ZERO.build(
#     [
#         [2, 0, 0],
#         [0, 1, 0],
#         [1, 0, 1]
#     ]
# )

# ONE = Matrix(3, 3)
# ONE.build(
#     [
#         [1, 1, 0],
#         [0, 2, 0],
#         [0, 1, 1]
#     ]
# )

def matrix_multiply(A, B):
    n, p, m = len(A), len(A[0]), len(B[0])

    res = [[0 for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            for k in range(p):
                res[i][j] += A[i][k] * B[k][j]
            res[i][j] %= mod
    
    return res

# @TIME
def solve(testcase):
    n = II()
    s = I()

    # res = Matrix(1, 3)
    # res.build(
    #     [
    #         [0, 0, 1]
    #     ]
    # )

    res = [
        [0, 0, 1]
    ]

    routine = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

    # routine = Matrix(3, 3)
    # routine.build_identity(2)
    # print(routine)

    for c in s:
        if c == '0':
            routine = matrix_multiply(routine, ZERO)
        else:
            routine = matrix_multiply(routine, ONE)
    
    pw = [
        [routine[i][j] for j in range(3)] for i in range(3)
    ]

    n -= 1

    while n:
        if n & 1:
            routine = matrix_multiply(routine, pw)
        pw = matrix_multiply(pw, pw)
        n >>= 1
    
    # print(routine)
    res = matrix_multiply(res, routine)
    print((res[0][0] + res[0][1]) % mod)

    # print((res[(0, 0)] + res[(0, 1)]) % mod)

for testcase in range(II()):
    solve(testcase)