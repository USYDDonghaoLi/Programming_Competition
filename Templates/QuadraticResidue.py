"""
二次剩余与 Cipolla 算法。

主要功能：找到模质数 p 的二次剩余的平方根。

定义：如果存在 x 使得 x^2 ≡ a (mod p)，则 a 是模 p 的二次剩余。

方法：
- Cipolla 算法：O(log p) 时间复杂度，概率性算法
- 使用 Legendre 符号判断是否存在平方根

适用场景：
- 解二次同余方程：x^2 ≡ a (mod p)
- p 必须是奇质数
"""

import random
from typing import Tuple, Optional


class GaussianInteger:
    """
    高斯整数（Gaussian Integer）：形如 a + bi (mod p) 的复数。
    
    用于 Cipolla 算法中模 p 的扩域计算。
    假设存在形如 i^2 = t (mod p) 的虚数单位 i。
    """
    
    def __init__(self, a: int = 0, b: int = 0, mod: int = None, i_squared: int = None):
        """
        初始化高斯整数。
        
        Args:
            a: 实部
            b: 虚部系数
            mod: 模数（质数）
            i_squared: i^2 模 p 的值
        """
        self.real = a
        self.imag = b
        self.mod = mod
        self.i_squared = i_squared
    
    def __mul__(self, other):
        """
        两个高斯整数的乘法。
        
        (a + bi) * (c + di) = (ac + bdi^2) + (ad + bc)i
        """
        if isinstance(other, GaussianInteger):
            # (a + bi)(c + di) = (ac + bd*i^2) + (ad + bc)i
            real_part = (self.real * other.real + 
                        self.i_squared * self.imag * other.imag) % self.mod
            imag_part = (self.imag * other.real + 
                        self.real * other.imag) % self.mod
            return GaussianInteger(real_part, imag_part, self.mod, self.i_squared)
        else:
            # 与整数相乘
            return GaussianInteger(
                (self.real * other) % self.mod,
                (self.imag * other) % self.mod,
                self.mod,
                self.i_squared
            )
    
    def __eq__(self, other):
        """比较两个高斯整数是否相等。"""
        return self.real == other.real and self.imag == other.imag
    
    def __repr__(self):
        """返回字符串表示。"""
        return f"({self.real} + {self.imag}i)"


def power_mod(base, exponent: int, mod: int):
    """
    快速幂运算：计算 base^exponent mod p。
    
    支持高斯整数和整数。
    
    Args:
        base: 底数（整数或 GaussianInteger）
        exponent: 指数
        mod: 模数
        
    Returns:
        base^exponent mod p
    """
    if isinstance(base, GaussianInteger):
        result = GaussianInteger(1, 0, mod, base.i_squared)
    else:
        result = 1
    
    base_copy = base
    
    while exponent > 0:
        if exponent & 1:
            if isinstance(result, GaussianInteger):
                result = result * base_copy
            else:
                result = (result * base_copy) % mod
        
        if isinstance(base_copy, GaussianInteger):
            base_copy = base_copy * base_copy
        else:
            base_copy = (base_copy * base_copy) % mod
        
        exponent >>= 1
    
    return result


def legendre_symbol(a: int, p: int) -> int:
    """
    计算 Legendre 符号：(a/p)。
    
    定义：
    - (a/p) ≡ a^((p-1)/2) (mod p)
    - (a/p) = 1  如果 a 是模 p 的二次剩余
    - (a/p) = -1 如果 a 不是模 p 的二次剩余
    - (a/p) = 0  如果 a ≡ 0 (mod p)
    
    Args:
        a: 整数
        p: 奇质数
        
    Returns:
        Legendre 符号的值：0, 1 或 p-1（表示 -1）
    """
    return power_mod(a, (p - 1) // 2, p)


def cipolla(a: int, p: int) -> Optional[Tuple[int, int]]:
    """
    Cipolla 算法：求解 x^2 ≡ a (mod p)。
    
    时间复杂度：O(log p)（加上随机部分的期望常数倍）
    
    算法步骤：
    1. 检查 a 是否是二次剩余（Legendre 符号）
    2. 随机找一个 r 使得 r^2 - a 是非剩余
    3. 在高斯整数域中计算 (r + sqrt(r^2 - a))^((p+1)/2)
    4. 取实部得到平方根
    
    Args:
        a: 要开方的数
        p: 奇质数
        
    Returns:
        (x0, x1) 其中 x0 < x1，满足 x0^2 ≡ x1^2 ≡ a (mod p)
        如果 a ≡ 0 (mod p)，返回 (0, 0)
        如果 a 不是二次剩余，返回 None
        
    示例:
        >>> cipolla(2, 7)  # 2^2 = 4, 5^2 = 25 ≡ 4 (mod 7), 但需要验证
        # 实际应该是找 x 使 x^2 ≡ 2 (mod 7)，这里无解
        >>> cipolla(3, 7)  # 3 的平方根
        # 5^2 = 25 ≡ 4 (mod 7), 2^2 = 4 (mod 7)
    """
    a %= p
    
    # 特殊情况：a = 0
    if a == 0:
        return (0, 0)
    
    # 检查 a 是否是二次剩余
    if legendre_symbol(a, p) != 1:
        return None  # a 不是模 p 的二次剩余
    
    # 随机找一个 r 使得 i^2 = r^2 - a 是非二次剩余
    r = 0
    i_squared = 0
    
    max_attempts = 100
    for _ in range(max_attempts):
        r = random.randint(0, p - 1)
        i_squared = (r * r - a) % p
        
        if i_squared != 0 and legendre_symbol(i_squared, p) != 1:
            break
    
    # 在高斯整数域中计算 (r + sqrt(i^2))^((p+1)/2)
    # 注意：sqrt(i^2) = i（虚部为 1）
    gaussian = GaussianInteger(r, 1, p, i_squared)
    result = power_mod(gaussian, (p + 1) // 2, p)
    
    x0 = result.real
    x1 = (p - x0) % p
    
    # 验证结果（调试用）
    assert (x0 * x0) % p == a, f"验证失败：{x0}^2 mod {p} != {a}"
    assert (x1 * x1) % p == a, f"验证失败：{x1}^2 mod {p} != {a}"
    
    # 返回有序的结果
    if x0 > x1:
        x0, x1 = x1, x0
    
    return (x0, x1)


# 以下是使用示例（注释掉以避免自动执行）
# if __name__ == "__main__":
#     # 示例：求解 x^2 ≡ 10 (mod 13)
#     a, p = 10, 13
#     result = cipolla(a, p)
#     if result:
#         x0, x1 = result
#         print(f"x^2 ≡ {a} (mod {p}) 的解：{x0}, {x1}")
#         print(f"验证：{x0}^2 mod {p} = {(x0*x0) % p}")
#         print(f"验证：{x1}^2 mod {p} = {(x1*x1) % p}")
#     else:
#         print(f"{a} 不是模 {p} 的二次剩余")
