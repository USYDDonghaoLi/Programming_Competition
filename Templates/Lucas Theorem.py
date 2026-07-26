"""
Lucas 定理

计算 C(n, m) mod p，其中 p 是质数。

定理：C(n, m) ≡ ∏ C(n_i, m_i) (mod p)
其中 n = Σ n_i * p^i，m = Σ m_i * p^i（p 进制表示）

复杂度：O(log_p(n) * p) 预处理阶乘，O(log_p(n)) 查询

应用：
- 计算大组合数的模值
- 概率论组合计数
- 数论竞赛问题
"""

#when n>p
from functools import lru_cache
MOD=131
@lru_cache(None)
def factorial(n):
    return 1 if n==0 else n*factorial(n-1)
@lru_cache(None)
def inv(n):
    return pow(factorial(n),MOD-2,MOD)
def binom(n,m):
    return factorial(n)*inv(m)*inv(n-m)%MOD if n>=m else 0
def lucas(n,m):
    return binom(n%MOD,m%MOD)*binom(n//MOD,m//MOD) if n>MOD and m>MOD else binom(n,m)