fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

from typing import List

class Solution:
    def maxProfit(self, A: List[int], B: List[int], k: int) -> int:

        n = len(A)

        pa = [0]
        pab = [0]

        for a, b in zip(A, B):
            pa.append(pa[-1] + a)
            pab.append(pab[-1] + a * b)

        res = pab[-1]

        # print('pa', pa)
        # print('pab', pab)

        kk = k >> 1
        for i in range(k, n + 1):
            cur = pab[-1] - pab[i]
            one = pa[i] - pa[i - kk]
            cur2 = pab[i - k]

            # print('info', cur, one, cur2)

            res = fmax(res, cur + one + cur2)

        return res