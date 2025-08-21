from typing import List

class Solution:
    def xorAfterQueries(self, A: List[int], queries: List[List[int]]) -> int:
        mod = 10 ** 9 + 7

        for l, r, k, v in queries:
            for i in range(l, r + 1, k):
                A[i] = (A[i] * v) % mod

        res = 0
        for a in A:
            res ^= a

        return res