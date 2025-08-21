from typing import List

class Solution:
    def sortPermutation(self, nums: List[int]) -> int:
        A = []
        for i, v in enumerate(nums):
            if i != v:
                A.append(v)

        if not A:
            return 0
        else:
            res = A[0]
            for i in range(1, len(A)):
                res &= A[i]
            return res