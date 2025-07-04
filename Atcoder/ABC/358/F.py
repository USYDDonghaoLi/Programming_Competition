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

# @TIME
def solve(testcase):
    n, m, k = MI()
    if k < n:
        print('No')
        return
    
    need = k - n
    
    if need & 1:
        print('No')
        return
    
    grid = [[' ' for _ in range(2 * m + 1)] for _ in range(2 * n + 1)]
    
    for i in range(2 * n + 1):
        for j in range(2 * m + 1):
            if i == 0 or i == 2 * n or j == 0 or j == 2 * m:
                if i == 0 and j == 2 * m - 1:
                    grid[i][j] = 'S'
                elif i == 2 * n and j == 2 * m - 1:
                    grid[i][j] = 'G'
                else:
                    grid[i][j] = '+'
            else:
                if i + j & 1:
                    grid[i][j] = '.'
                else:
                    if i & 1:
                        grid[i][j] = 'o'
                    else:
                        grid[i][j] = '+'
    
    if n & 1:
        if need <= (n // 2) * 2 * (m - 1):
            for i in range(1, n, 2):
                M = 2 * (m - 1)
                # print(need, M)
                # print('M', M)
                if need >= M:
                    need -= M
                    '''
                    2 * (i + 1), 2 * (i + 2)
                    '''
                    for j in range(3, 2 * m + 1, 2):
                        grid[2 * (i)][j] = '-'
                    for j in range(1, 2 * m - 1, 2):
                        if 2 * (i + 1) != 2 * n:
                            grid[2 * (i + 1)][j] = '-'
                    if need == 0:
                        for ii in range(2 * i + 3, 2 * n + 1):
                            # print(ii, ''.join(grid[ii]))
                            if ii & 1:
                                try:
                                    if m != 1:
                                        grid[ii][-3] = '|'
                                except:
                                    continue
                        
                else:
                    assert need % 2 == 0
                    need //= 2
                    for j in range(2 * m - 1, 2 * m - 2 * need, -2):
                        grid[2 * i][j] = '-'
                    grid[2 * i - 1][2 * m - 2 * need - 2] = '|'
                    grid[2 * i + 1][2 * m - 2 * need - 2] = '|'
                    for j in range(2 * m - 2 * need - 1, 2 * m - 1, 2):
                        if 2 * i + 2 != 2 * n:
                            grid[2 * i + 2][j] = '-'
                    for ii in range(2 * i + 3, 2 * n + 1):
                        # print(ii, ''.join(grid[ii]))
                        if ii & 1:
                            try:
                                grid[ii][-3] = '|'
                            except:
                                continue
                    need = 0
                    break
            
            # print('need', need)
            if not need:
                print('Yes')
                
                # for i in range(2 * n + 1):
                #     for j in range(2 * m + 1):
                #         if i == 0 or i == 2 * n or j == 0 or j == 2 * m:
                #             if i == 0 and j == 2 * m - 1:
                #                 grid[i][j] = 'S'
                #             elif i == 2 * n and j == 2 * m - 1:
                #                 grid[i][j] = 'G'
                #             else:
                #                 grid[i][j] = '+'
            
                for i in range(2 * n + 1):
                    print(''.join(grid[i]))
            else:
                print('No')
            
        else:
            print('wtf2')
            for i in range(1, n - 2, 2):
                M = 2 * (m - 1)
                # print(need, M)
                # print('M', M)
                if need >= M:
                    need -= M
                    '''
                    2 * (i + 1), 2 * (i + 2)
                    '''
                    for j in range(3, 2 * m + 1, 2):
                        grid[2 * i][j] = '-'
                    for j in range(1, 2 * m - 1, 2):
                        if 2 * (i + 1) != 2 * n:
                            grid[2 * (i + 1)][j] = '-'
                    if need == 0:
                        for ii in range(2 * i + 3, 2 * n + 1):
                            # print(ii, ''.join(grid[ii]))
                            if ii & 1:
                                try:
                                    if m != 1:
                                        grid[ii][-3] = '|'
                                except:
                                    continue
                        
                else:
                    assert need % 2 == 0
                    need //= 2
                    for j in range(2 * m - 1, 2 * m - 2 * need, -2):
                        grid[2 * i][j] = '-'
                    grid[2 * i - 1][2 * m - 2 * need - 2] = '|'
                    grid[2 * i + 1][2 * m - 2 * need - 2] = '|'
                    for j in range(2 * m - 2 * need - 1, 2 * m - 1, 2):
                        if 2 * i + 2 != 2 * n:
                            grid[2 * i + 2][j] = '-'
                    for ii in range(2 * i + 3, 2 * n + 1):
                        # print(ii, ''.join(grid[ii]))
                        if ii & 1:
                            try:
                                grid[ii][-3] = '|'
                            except:
                                continue
                    need = 0
                    break
            
            need += 3
            print('wtf3', need)
            # print('need', need)
            flag = False
            for lshift in range(1, m):
                if not lshift & 1:
                    tot = 3 * (lshift + 1)
                    if tot == need:
                        # print(lshift, 'ls 1')
                        for j in range(2 * m - 1, 1, -2):
                            grid[-5][j] = '-'
                        for j in range(2, 2 * m, 2):
                            if j % 4 == 2:
                                grid[-4][j] = '|'
                            elif j % 4 == 0:
                                grid[-2][j] = '|'
                        flag = True
                        break
                    elif tot == need + 2:
                        # print('lshift -2', lshift)
                        for j in range(2 * m - 1, 1, -2):
                            grid[-5][j] = '-'
                        for j in range(2, 2 * m - 2, 2):
                            if j % 4 == 2:
                                grid[-4][j] = '|'
                            elif j % 4 == 0:
                                grid[-2][j] = '|'
                        grid[-3][-4] = '-'
                        grid[-3][-2] = '-'
                        flag = True
                        
                        break
                else:
                    tot = 3 * (lshift + 1) - 1
                    if tot == need:
                        # print(lshift, 'ls not 1')
                        for j in range(2 * m - 1, 1, -2):
                            grid[-5][j] = '-'
                        for j in range(2, 2 * m, 2):
                            if j % 4 == 2:
                                grid[-4][j] = '|'
                            elif j % 4 == 0:
                                grid[-2][j] = '|'
                        grid[-3][-2] = '-'
                        flag = True
                        break
            
            fo = open("C:/Users/Admin/Desktop/Ldh/ALGORITHM/Atcoder/ABC/358/Fout.txt", "w")
            
            if flag:
                print('Yes')
                for i in range(2 * n + 1):
                    print(''.join(grid[i]))
                    fo.write(''.join(grid[i]) + '\n')
            else:
                print('No')   
        
    else:
    
        for i in range(1, n, 2):
            M = 2 * (m - 1)
            # print(need, M)
            # print('M', M)
            if need >= M:
                need -= M
                '''
                2 * (i + 1), 2 * (i + 2)
                '''
                for j in range(3, 2 * m + 1, 2):
                    grid[2 * (i)][j] = '-'
                for j in range(1, 2 * m - 1, 2):
                    if 2 * (i + 1) != 2 * n:
                        grid[2 * (i + 1)][j] = '-'
                if need == 0:
                    for ii in range(2 * i + 3, 2 * n + 1):
                        # print(ii, ''.join(grid[ii]))
                        if ii & 1:
                            try:
                                if m != 1:
                                    grid[ii][-3] = '|'
                            except:
                                continue
                    
            else:
                assert need % 2 == 0
                need //= 2
                for j in range(2 * m - 1, 2 * m - 2 * need, -2):
                    grid[2 * i][j] = '-'
                grid[2 * i - 1][2 * m - 2 * need - 2] = '|'
                grid[2 * i + 1][2 * m - 2 * need - 2] = '|'
                for j in range(2 * m - 2 * need - 1, 2 * m - 1, 2):
                    if 2 * i + 2 != 2 * n:
                        grid[2 * i + 2][j] = '-'
                for ii in range(2 * i + 3, 2 * n + 1):
                    # print(ii, ''.join(grid[ii]))
                    if ii & 1:
                        try:
                            grid[ii][-3] = '|'
                        except:
                            continue
                need = 0
                break
    
        # print('need', need)
        if not need:
            print('Yes')
            
            # for i in range(2 * n + 1):
            #     for j in range(2 * m + 1):
            #         if i == 0 or i == 2 * n or j == 0 or j == 2 * m:
            #             if i == 0 and j == 2 * m - 1:
            #                 grid[i][j] = 'S'
            #             elif i == 2 * n and j == 2 * m - 1:
            #                 grid[i][j] = 'G'
            #             else:
            #                 grid[i][j] = '+'
            
            for i in range(2 * n + 1):
                print(''.join(grid[i]))
        else:
            print('No')

for testcase in range(1):
    solve(testcase)