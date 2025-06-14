from typing import *

F = [1 for _ in range(100010)]
mod = 10 ** 9 + 7
for i in range(2, 100010):
    F[i] = F[i - 1] * i % mod

class Solution:
    def countPermutations(self, A: List[int]) -> int:
        n = len(A)
        for i in range(1, n):
            if A[i] <= A[0]:
                return 0

        return F[n - 1]