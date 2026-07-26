"""
莫比乌斯反演（Möbius Inversion）。

用于解决涉及最大公约数（GCD）的计数问题。
通常用于求解形如 "满足 gcd(i, j) = 1 的对数" 的问题。

主要结论：
1. 莫比乌斯函数定义：
   - μ(1) = 1
   - 如果 n 包含平方因子，μ(n) = 0
   - 如果 n 是 k 个不同质数的乘积，μ(n) = (-1)^k

2. 莫比乌斯反演定理：
   如果 g(n) = Σ f(d)（d | n）
   则 f(n) = Σ μ(d) * g(n/d)（d | n）

时间复杂度：
- 预计算 μ (1 到 n)：O(n log log n)
- 单次查询：O(n)（取决于具体应用）
"""


def sieve_mobius(n: int) -> list:
    """
    使用线性筛计算 1 到 n 的莫比乌斯函数值。
    
    时间复杂度：O(n)
    
    Args:
        n: 上限
        
    Returns:
        mu[i] = μ(i)，其中 i ∈ [1, n]
        
    示例:
        >>> mu = sieve_mobius(10)
        >>> mu[1]  # μ(1) = 1
        1
        >>> mu[2]  # μ(2) = -1（一个质数）
        -1
        >>> mu[6]  # μ(6) = μ(2*3) = 1（两个不同质数）
        1
        >>> mu[4]  # μ(4) = 0（包含 2^2）
        0
    """
    mu = [0] * (n + 1)
    is_prime = [True] * (n + 1)
    primes = []
    
    mu[1] = 1
    
    for i in range(2, n + 1):
        # 如果 i 是质数
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1  # 质数的莫比乌斯值为 -1
        
        # 线性筛的核心：用最小质因子标记合数
        for p in primes:
            if i * p > n:
                break
            
            is_prime[i * p] = False
            
            if i % p == 0:
                # p 是 i 的最小质因子
                # i*p 包含 p^2，所以 μ(i*p) = 0
                mu[i * p] = 0
                break
            else:
                # p 不是 i 的因子
                # μ(i*p) = -μ(i)（多一个质因子）
                mu[i * p] = -mu[i]
    
    return mu


def sieve_mobius_and_primes(n: int) -> tuple:
    """
    同时计算莫比乌斯函数和质数列表。
    
    时间复杂度：O(n)
    
    Args:
        n: 上限
        
    Returns:
        (mu, primes) 其中：
        - mu[i] = μ(i)
        - primes 是 1 到 n 之间的所有质数列表
    """
    mu = [0] * (n + 1)
    is_prime = [True] * (n + 1)
    primes = []
    
    mu[1] = 1
    
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        
        for p in primes:
            if i * p > n:
                break
            
            is_prime[i * p] = False
            
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    
    return mu, primes


def count_coprime_pairs(n: int) -> int:
    """
    计算 1 到 n 中互质的有序对 (i, j) 的个数，其中 i ≤ j。
    
    使用莫比乌斯反演。
    
    时间复杂度：O(n log n)
    
    Args:
        n: 上限
        
    Returns:
        满足 gcd(i, j) = 1 且 i ≤ j 的对数
        
    示例:
        >>> count_coprime_pairs(5)  # (1,1), (1,2), (1,3), (1,4), (1,5), (2,3), (2,5), (3,4), (3,5), (4,5)
        10
    """
    mu = sieve_mobius(n)
    count = 0
    
    # 使用莫比乌斯反演计数
    for d in range(1, n + 1):
        # 计算有多少对 (i, j) 使得 gcd(i, j) = d
        # 即 i = d*a, j = d*b，其中 gcd(a, b) = 1，1 ≤ a ≤ b ≤ n/d
        pairs_with_gcd_d = 0
        
        for a in range(1, n // d + 1):
            for b in range(a, n // d + 1):
                # 检查 gcd(a, b) 是否等于 1
                from math import gcd
                if gcd(a, b) == 1:
                    pairs_with_gcd_d += 1
        
        count += mu[d] * pairs_with_gcd_d
    
    return count


def invert_with_mobius(g: list) -> list:
    """
    给定 g，使用莫比乌斯反演求 f。
    
    假设 g[n] = Σ f[d]（d | n）
    则 f[n] = Σ μ(d) * g[n/d]（d | n）
    
    Args:
        g: 长度为 n+1 的数组，其中 g[i] = Σ f[d]（d | i）
        
    Returns:
        f: 长度为 n+1 的数组
        
    示例:
        假设 f = [0, 1, 2, 3, 4, 5, ...]（某个函数）
        g[i] = Σ f[d]（d | i）
        则 invert_with_mobius(g) 会恢复出 f
    """
    n = len(g) - 1
    mu = sieve_mobius(n)
    f = [0] * (n + 1)
    
    for i in range(1, n + 1):
        for d in range(1, i + 1):
            if i % d == 0:  # d | i
                f[i] += mu[d] * g[i // d]
    
    return f


def mobius_transform(f: list) -> list:
    """
    Dirichlet 卷积的快速计算。
    
    给定 f，计算 g[n] = Σ f[d]（d | n）。
    
    Args:
        f: 长度为 n+1 的数组
        
    Returns:
        g: 长度为 n+1 的数组
    """
    n = len(f) - 1
    g = [0] * (n + 1)
    
    for i in range(1, n + 1):
        for d in range(1, n + 1):
            if i * d <= n:
                g[i * d] += f[i]
    
    return g


# 示例：欧拉函数与莫比乌斯函数的关系
def compute_euler_totient(n: int) -> list:
    """
    使用莫比乌斯函数计算欧拉函数 φ(n)。
    
    φ(n) = n * Π (1 - 1/p)（p 是 n 的所有质因子）
    
    或者：φ(n) = Σ μ(d) * (n / d)（d | n）
    
    Args:
        n: 上限
        
    Returns:
        phi[i] = φ(i)
    """
    mu = sieve_mobius(n)
    phi = [0] * (n + 1)
    
    for i in range(1, n + 1):
        for d in range(1, i + 1):
            if i % d == 0:
                phi[i] += mu[d] * (i // d)
    
    return phi
