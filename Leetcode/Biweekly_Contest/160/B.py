from typing import *

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Solution:
    def minCost(self, m: int, n: int, A: List[List[int]]) -> int:
        m, n = n, m
        for i in range(n):
            for j in range(m):
                if i == 0 and j == 0:
                    A[i][j] = 1
                elif i == n - 1 and j == m - 1:
                    A[i][j] = (i + 1) * (j + 1)
                else:
                    A[i][j] += (i + 1) * (j + 1)
        
        for i in range(1, n):
            A[i][0] += A[i - 1][0]
        
        for j in range(1, m):
            A[0][j] += A[0][j - 1]
        
        for i in range(1, n):
            for j in range(1, m):
                A[i][j] += fmin(A[i - 1][j], A[i][j - 1])
        
        return A[-1][-1]