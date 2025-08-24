fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

from typing import List

class Solution:
    def maxBalancedShipments(self, A: List[int]) -> int:
        n = len(A)
        
        B = []
        res = [0 for _ in range(n + 1)]

        for i, a in enumerate(A, 1):
            res[i] = res[i - 1]
            while B and A[B[-1] - 1] <= a:
                B.pop()
            if not B:
                pass
            else:
                last = B[-1]
                res[i] = fmax(res[last - 1] + 1, res[i])
            B.append(i)

        return max(res)