"""
Pollard's Rho 算法：快速质因数分解。

用于分解较大的整数（10^18 范围）。
结合 Miller-Rabin 素性检验和 Pollard's Rho 因数分解。

时间复杂度：
- 平均：O(n^(1/4) * log n)
- 最坏：O(n^(1/2))

应用：
- 分解极大整数
- 检验素数
- 求欧拉函数等数论应用
"""

from math import gcd as math_gcd
from typing import Dict, List


def extended_gcd(a: int, b: int) -> tuple:
    """扩展欧几里得算法。"""
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y


def gcd(a: int, b: int) -> int:
    """计算最大公约数。"""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """计算最小公倍数。"""
    return a // gcd(a, b) * b


def power_mod(base: int, exp: int, mod: int) -> int:
    """快速幂：计算 base^exp mod mod。"""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


def is_prime_miller_rabin(n: int) -> bool:
    """
    Miller-Rabin 素性检验。
    
    确定性检验范围：
    - n < 2^32：使用 [2, 7, 61] 三个证人
    - n < 2^48：使用 7 个证人
    - n >= 2^48：使用 12 个证人
    
    Args:
        n: 待检验的整数
        
    Returns:
        True 如果 n 是质数，False 如果 n 是合数
        
    时间复杂度：O(k log n)，其中 k 是证人个数
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n & 1 == 0:
        return False
    
    # 选择证人
    if n < (1 << 32):
        witnesses = [2, 7, 61]
    elif n < (1 << 48):
        witnesses = [2, 3, 5, 7, 11, 13, 17]
    else:
        witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    
    # 将 n-1 写成 d * 2^r 的形式
    d = n - 1
    r = 0
    while d & 1 == 0:
        d >>= 1
        r += 1
    
    # 检验每个证人
    for a in witnesses:
        if a >= n:
            continue
        
        x = power_mod(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        # 重复 r-1 次
        composite = True
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                composite = False
                break
        
        if composite:
            return False
    
    return True


def pollard_rho_find_factor(n: int) -> int:
    """
    Pollard's Rho 算法：找 n 的一个非平凡因子。
    
    基于生日悖论和伪随机序列。
    
    Args:
        n: 待因数分解的整数（假设 n 是合数）
        
    Returns:
        n 的一个因子（可能不是质因子）
        
    时间复杂度：平均 O(n^(1/4))
    """
    if n & 1 == 0:
        return 2
    
    # 尝试不同的随机序列
    x = 2
    y = 2
    c = 1
    d = 1
    
    # f(x) = (x^2 + c) mod n
    f = lambda x: (x * x + c) % n
    
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
        
        if d == n:
            # 失败，尝试下一个 c
            return pollard_rho_find_factor_with_c(n, c + 1)
    
    if d != n:
        return d
    
    return pollard_rho_find_factor_with_c(n, c + 1)


def pollard_rho_find_factor_with_c(n: int, c: int) -> int:
    """
    Pollard's Rho 算法的变体：使用指定的 c 值。
    
    Args:
        n: 待因数分解的整数
        c: 随机序列的参数
        
    Returns:
        n 的一个非平凡因子
    """
    if n & 1 == 0:
        return 2
    
    m = max(1, 1 << (n.bit_length() // 8))
    
    for attempt in range(1, 100):
        f = lambda x: (x * x + c) % n
        
        y = 2
        r = 1
        q = 1
        g = 1
        
        x = y
        
        while g == 1:
            # 快速前进 y
            x = y
            for _ in range(r):
                y = f(y)
            
            # 计算 gcd
            k = 0
            while k < r and g == 1:
                ys = y
                # 计算 m 次迭代
                for _ in range(min(m, r - k)):
                    y = f(y)
                    q = q * abs(x - y) % n
                
                g = gcd(q, n)
                k += m
            
            r <<= 1
        
        if g == n:
            # 回溯找实际因子
            g = 1
            while g == 1:
                ys = f(ys)
                g = gcd(abs(x - ys), n)
        
        if g != n and g != 1:
            return g
    
    return n


def factorize(n: int) -> Dict[int, int]:
    """
    完整的质因数分解。
    
    Args:
        n: 待分解的整数
        
    Returns:
        字典 {质因子: 指数}
        
    示例:
        >>> factorize(60)
        {2: 2, 3: 1, 5: 1}  # 60 = 2^2 * 3 * 5
        
        >>> factorize(1000000007)
        {1000000007: 1}  # 是质数
    """
    factors = {}
    
    # 先分解小质因子
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    for p in small_primes:
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
    
    # 对于更大的因子，使用 Pollard's Rho + 试除
    if n == 1:
        return factors
    
    stack = [n]
    
    while stack:
        current = stack.pop()
        
        if current == 1:
            continue
        
        # 检查是否是质数
        if is_prime_miller_rabin(current):
            factors[current] = factors.get(current, 0) + 1
            continue
        
        # 不是质数，需要分解
        # 如果足够小，继续试除
        if current < 10000:
            i = 2
            while i * i <= current:
                while current % i == 0:
                    factors[i] = factors.get(i, 0) + 1
                    current //= i
                i += 1 if i == 2 else 2
            
            if current > 1:
                factors[current] = factors.get(current, 0) + 1
        else:
            # 使用 Pollard's Rho
            divisor = pollard_rho_find_factor(current)
            
            if divisor == current:
                # 仍然找不到因子，作为质因子处理
                factors[current] = factors.get(current, 0) + 1
            else:
                # 递归分解
                stack.append(current // divisor)
                stack.append(divisor)
    
    return factors


def get_all_factors(n: int) -> List[int]:
    """
    获取 n 的所有因子。
    
    Args:
        n: 整数
        
    Returns:
        n 的所有因子列表（升序）
        
    示例:
        >>> get_all_factors(12)
        [1, 2, 3, 4, 6, 12]
    """
    if n == 1:
        return [1]
    
    prime_factors = factorize(n)
    
    # 生成所有因子
    factors = [1]
    
    for prime, exp in prime_factors.items():
        new_factors = []
        p_power = 1
        for _ in range(exp):
            p_power *= prime
            for f in factors:
                new_factors.append(f * p_power)
        factors.extend(new_factors)
    
    return sorted(factors)


def euler_phi(n: int) -> int:
    """
    计算欧拉函数 φ(n)。
    
    φ(n) = n * ∏(1 - 1/p)，其中 p 是 n 的所有不同质因子。
    
    Args:
        n: 整数
        
    Returns:
        φ(n) 的值
        
    示例:
        >>> euler_phi(12)  # φ(12) = 12 * (1 - 1/2) * (1 - 1/3) = 4
        4
    """
    if n == 1:
        return 1
    
    prime_factors = factorize(n)
    result = n
    
    for prime in prime_factors:
        result = result // prime * (prime - 1)
    
    return result


def mobius(n: int) -> int:
    """
    计算莫比乌斯函数 μ(n)。
    
    定义：
    - μ(1) = 1
    - 如果 n 包含平方因子，μ(n) = 0
    - 如果 n 是 k 个不同质数的乘积，μ(n) = (-1)^k
    
    Args:
        n: 整数
        
    Returns:
        莫比乌斯函数值
    """
    if n == 1:
        return 1
    
    prime_factors = factorize(n)
    
    # 检查是否有重复质因子
    for exp in prime_factors.values():
        if exp > 1:
            return 0
    
    # 计算 (-1)^k，其中 k 是不同质因子个数
    return (-1) ** len(prime_factors)

    return x & 0x7f