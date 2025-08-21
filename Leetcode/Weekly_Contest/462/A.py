from typing import List

class Solution:
    def reverseSubmatrix(self, A: List[List[int]], x: int, y: int, k: int) -> List[List[int]]:
        n, m = len(A), len(A[0])

        B = [[0 for _ in range(m)] for _ in range(n)]

        for i in range(n):
            for j in range(m):
                if x <= i < x + k and y <= j < y + k:
                    B[i][j] = A[x + x + k - 1 - i][j]
                else:
                    B[i][j] = A[i][j]

        return B