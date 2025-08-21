from itertools import permutations
from bisect import bisect_right

ODD_MASK = 0x155
D = 9

special_numbers = []
for mask in range(1, 1 << D):
    t = mask & ODD_MASK
    if t & (t - 1):  # 至少有两个奇数
        continue

    # 构造排列 perm
    perm = []
    size = odd = 0
    for x in range(1, D + 1):
        if mask >> (x - 1) & 1:
            size += x
            perm.extend([x] * (x // 2))
            if x % 2:
                odd = x
    if size > 16:  # 回文串太长了
        continue

    # 枚举 perm 的所有排列 p，生成对应的回文数
    for p in permutations(perm):
        pal = 0
        for v in p:
            pal = pal * 10 + v
        v = pal
        if odd:
            pal = pal * 10 + odd
        # 反转 pal 的左半，拼在 pal 后面
        while v:
            v, d = divmod(v, 10)
            pal = pal * 10 + d
        special_numbers.append(pal)
special_numbers = sorted(set(special_numbers))

class Solution:
    def specialPalindrome(self, n: int) -> int:
        i = bisect_right(special_numbers, n)
        return special_numbers[i]