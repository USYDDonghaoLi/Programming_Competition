"""
Baby-Step Giant-Step 算法

求解离散对数问题：a^x ≡ b (mod m)

原理：
- Baby Step: 预计算 a^j mod m 的哈希表
- Giant Step: 尝试 (a^t)^i mod m 并查询哈希表
- t ≈ √m

复杂度：O(√m) 时间，O(√m) 空间

应用：
- 求离散对数
- 某些加密系统中的安全参数
- 循环群的阶数问题
"""

    return input()
def II():
    return int(input())
def MI():
    return map(int, input().split())
def LI():
    return list(input().split())
def LII():
    return list(map(int, input().split()))
def GMI():
    return map(lambda x: int(x) - 1, input().split())

#------------------------------FastIO---------------------------------

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
from time import *
from random import *
from math import gcd
#dfs - stack#
#check top!#

class BSGS:
    #solving problem like a ** x = b (mod m)#
    
    def solution(self, a, b, m, k = 1):
        d = dict()
        cur = 1
        t = int(m ** .5) + 1
        for B in range(1, t + 1):
            cur *= a
            cur %= m
            d[b * cur % m] = B
        
        now = cur * k % m
        for A in range(1, t + 1):
            if now in d:
                return A * t - d[now]
            now *= cur
            now %= m
        
        return float('-inf')
    
    def exBSGS(self, a, b, m, k = 1):
        a %= m; A = a
        b %= m; B = b
        M = m

        cur = 1 % m
        for i in range(10000):
            if cur == B:
                return i
            cur *= A
            cur %= M
            d = gcd(a, m)
            if b % d:
                return float('-inf')
            if d == 1:
                return self.solution(a, b, m, k * a % m) + i + 1
            k *= a // d; k %= m
            b //= d
            m //= d

def solve():
    a, b, m = MI()
    bsgs = BSGS()
    print(bsgs.exBSGS(a, b, m, k = 1))

for _ in range(1):solve()


