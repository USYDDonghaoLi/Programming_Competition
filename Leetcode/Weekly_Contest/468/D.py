from typing import *
from heapq import *

min = lambda a, b: b if b < a else a
max = lambda a, b: b if b > a else a

def op(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return min(a[0], b[0]), max(a[1], b[1])

class ST:
    def __init__(self, a: List[int]):
        n = len(a)
        w = n.bit_length()
        st = [[None] * n for _ in range(w)]
        st[0] = [(x, x) for x in a]
        for i in range(1, w):
            for j in range(n - (1 << i) + 1):
                st[i][j] = op(st[i - 1][j], st[i - 1][j + (1 << (i - 1))])
        self.st = st

    def query(self, l: int, r: int) -> int:
        k = (r - l).bit_length() - 1
        mn, mx = op(self.st[k][l], self.st[k][r - (1 << k)])
        return mx - mn

class Solution:
    def maxTotalValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        st = ST(nums)

        h = [(-st.query(i, n), i, n) for i in range(n)]


        ans = 0
        for _ in range(k):
            d, l, r = h[0]
            if d == 0:
                break
            ans -= d
            heapreplace(h, (-st.query(l, r - 1), l, r - 1))
        return ans