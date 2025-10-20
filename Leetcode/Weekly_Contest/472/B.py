from typing import *

class Solution:
    def longestBalanced(self, A: List[int]) -> int:
        res = 0
        n = len(A)

        for i in range(n):
            e, o = set(), set()
            for j in range(i, n):
                if A[j] & 1:
                    e.add(A[j])
                else:
                    o.add(A[j])

                if len(e) == len(o):
                    res = max(res, j - i + 1)

        return res