fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

from typing import List
inf = float('inf')

class Solution:
    def maxSumTrionic(self, A: List[int]) -> int:
        res = -inf
        n = len(A)
        
        B = [(0, 0)]

        l, r = 0, 1
        while r < n:
            if A[r] >= A[r - 1]:
                l = r
                r += 1
            else:
                while r < n and A[r] < A[r - 1]:
                    r += 1
                B.append((l, r - 1))
                l = r - 1

        B.append((n - 1, n - 1))

        # print('B', B)

        m = len(B)

        for i in range(1, m - 1):
            l, r = B[i]
            cur = 0
            for j in range(l, r + 1):
                cur += A[j]

            ls = 0
            lm = -inf
            cl = l - 1
            lastr = B[i - 1][1]

            while cl >= lastr:
                if A[cl] >= A[cl + 1]:
                    break
                else:
                    ls += A[cl]
                    lm = fmax(lm, ls)
                    cl -= 1

            rs = 0
            rm = -inf
            cr = r + 1
            lastl = B[i + 1][0]

            while cr <= lastl:
                if A[cr] <= A[cr - 1]:
                    break
                else:
                    rs += A[cr]
                    rm = fmax(rm, rs)
                    cr += 1

            # print(l, r, cur, cl, cr, lm, rm)
            res = fmax(res, cur + lm + rm)

        return res