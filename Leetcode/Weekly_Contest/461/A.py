from typing import List

class Solution:
    def isTrionic(self, nums: List[int]) -> bool:
        n = len(nums)
        A = []
        for i in range(1, n):
            if nums[i] < nums[i - 1]:
                A.append(1)
            elif nums[i] > nums[i - 1]:
                A.append(2)
            else:
                A.append(3)

        B = []
        for a in A:
            if B and a == B[-1]:
                pass
            else:
                B.append(a)

        return B == [2, 1, 2]