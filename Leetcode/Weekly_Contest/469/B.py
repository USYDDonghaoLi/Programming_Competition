from typing import *
from math import inf

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

class Solution:
    def splitArray(self, A: List[int]) -> int:
        res = -1
        n = len(A)

        L = [0 for _ in range(n)]
        R = [0 for _ in range(n)]

        flag = True
        for i in range(n):
            if i and A[i] <= A[i - 1]:
                flag = False

            if flag:
                if i:
                    L[i] = L[i - 1] + A[i]
                else:
                    L[i] = A[i]
            else:
                L[i] = -1

        flag = True

        for i in range(n - 1, -1, -1):
            if i != n - 1 and A[i] <= A[i + 1]:
                flag = False

            if flag:
                if i == n - 1:
                    R[i] = A[i]
                else:
                    R[i] = R[i + 1] + A[i]
            else:
                R[i] = -1

        # print('L', L, 'R', R)
        res = inf

        for i in range(n - 1):
            l, r = L[i], R[i + 1]
            if l != -1 and r != -1:
                res = fmin(res, abs(l - r))

        return -1 if res == inf else res