
from typing import List

class Solution:
    def xorAfterQueries(self, A: List[int], queries: List[List[int]]) -> int:
        mod = 10 ** 9 + 7

        sz = 2

        n = len(A)

        B = [[1 for _ in range(n + sz * 2)] for _ in range(sz + 1)]

        for l, r, k, v in queries:

            if k <= sz:

                inv = pow(v, mod - 2, mod)

                B[k][l] *= v

                a, b = divmod(l, k)
                c, d = divmod(r, k)

                if d >= b:
                    r = c * k + b
                else:
                    r = (c - 1) * k + b

                B[k][r + k] *= inv

                B[k][l] %= mod
                B[k][r + k] %= mod

            else:
                for i in range(l, r + 1, k):
                    A[i] = A[i] * v % mod

        for i in range(1, sz + 1):
            # if i == 1:
            #     print('debug', B[i][:n + 1])
            for j in range(n):
                if j < i:
                    A[j] = A[j] * B[i][j] % mod
                else:
                    B[i][j] = B[i][j] * B[i][j - i] % mod
                    A[j] = A[j] * B[i][j] % mod
                # if i == 1:
                #     print('debug2', i, j, B[i][j], A[j])

        res = 0
        for a in A:
            res ^= a

        return res