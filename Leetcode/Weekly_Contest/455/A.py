from typing import *
from collections import *

primes = []

for i in range(2, 101):
    cnt = 0
    for j in range(1, i + 1):
        cnt += i % j == 0
    if cnt == 2:
        primes.append(i)

S = set(primes)

class Solution:
    def checkPrimeFrequency(self, nums: List[int]) -> bool:
        mp = Counter(nums)
        for k in mp:
            if mp[k] in S:
                return True

        return False