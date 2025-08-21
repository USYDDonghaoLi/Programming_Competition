class Solution:
    def minSensors(self, n: int, m: int, k: int) -> int:
        k = k * 2 + 1
        return ((n + k - 1) // k) * ((m + k - 1) // k)