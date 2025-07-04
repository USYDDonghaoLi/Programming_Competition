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

# def TIME(f):

#     def wrap(*args, **kwargs):
#         s = perf_counter()
#         ret = f(*args, **kwargs)
#         e = perf_counter()

#         print(e - s, 'sec')
#         return ret
    
#     return wrap

d = ((-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))

# @TIME
def solve(testcase):
    n, m = MI()
    grid = [list(I()) for _ in range(n)]
    coordinates = []
    for i in range(n):
        for j in range(m):
            if grid[i][j].isdigit():
                grid[i][j] = int(grid[i][j])
            else:
                if grid[i][j] == '*':
                    coordinates.append((i, j))
    
    k = len(coordinates)
    flag = False
    
    def check(state):
        tmp = [[grid[i][j] for j in range(m)] for i in range(n)]
        for bit in range(k):
            if state >> bit & 1:
                x, y = coordinates[bit]
                tmp[x][y] = 'X'
            else:
                x, y = coordinates[bit]
                tmp[x][y] = '.'
        
        for x in range(n):
            for y in range(m):
                if isinstance(tmp[x][y], int):
                    cnt = 0
                    for dx, dy in d:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and tmp[nx][ny] == 'X':
                            cnt += 1
                    if cnt != tmp[x][y]:
                        return False
        return True
    
    for i in range(1 << k):
        if check(i):
            if flag:
                print('Multiple')
                return
            else:
                flag = True
    
    print('Single')
    
    

for testcase in range(II()):
    solve(testcase)