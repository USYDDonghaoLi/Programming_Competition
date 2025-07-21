class Solution:
    def checkDivisibility(self, n: int) -> bool:
        a, b = 0, 1
        for c in str(n):
            a += int(c)
            b *= int(c)

        return n % (a + b) == 0