from typing import *

class Solution:
    def canMakeEqual(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        def check(num):
            A = nums[:]
            cnt = 0
            for i in range(n - 1):
                if A[i] != num:
                    cnt += 1
                    A[i] *= -1
                    A[i + 1] *= -1

            return all(a == num for a in A) and cnt <= k

        return check(1) or check(-1)