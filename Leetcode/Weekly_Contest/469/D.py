mod = 10 ** 9 + 7

def construct(r):
    A = [[0 for _ in range(r + 1)] for _ in range(r + 1)]

    for i in range(r + 1):
        for j in range(i):
            A[i][j] = 1

    B = [[0 for _ in range(r + 1)] for _ in range(r + 1)]
    for i in range(r + 1):
        for j in range(i + 1, r + 1):
            B[i][j] = 1

    return A, B

def mul(A, B):
    n, p, m = len(A), len(A[0]), len(B[0])
    res = [[0 for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            for k in range(p):
                res[i][j] = (res[i][j] + A[i][k] * B[k][j]) % mod

    return res

def pw(A, t):
    n = len(A)
    res = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        res[i][i] = 1
        
    while t:
        if t & 1:
            res = mul(res, A)
        A = mul(A, A)
        t >>= 1

    return res
class Solution:
    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        tot = r - l
        if n == 1:
            return tot
        elif n == 2:
            return tot * (tot - 1) // 2
        else:

            mod = 10 ** 9 + 7

            r -= l
            l = 0

            A, B = construct(r)

            # print('A', A, 'B', B)

            AB = mul(A, B)
            BA = mul(B, A)

            # print('AB', AB, 'BA', BA)

            n -= 1
            NA = mul(pw(AB, n >> 1), A) if n & 1 else pw(AB, n >> 1)
            NB = mul(pw(BA, n >> 1), B) if n & 1 else pw(BA, n >> 1)

            # print('NA', NA, 'NB', NB)
            res = 0

            for i in range(r + 1):
                for j in range(r + 1):
                    res = (res + NA[i][j] + NB[i][j]) % mod

            return res