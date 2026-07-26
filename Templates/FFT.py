"""
数论变换（NTT - Number Theoretic Transform）

在模某素数的有限域下进行多项式乘法（卷积），时间复杂度 O(n log n)。

使用素数的原始根替代 FFT 中的复数单位根，避免浮点误差。

应用：多项式乘法、大整数乘法、卷积计算。

复杂度：O(n log n)，其中 n = |A| + |B| - 1 向上取 2 的幂
"""

from typing import List


class NTT:
    """数论变换，用于模素数下的快速多项式乘法。"""
    
    MOD = 998244353  # 2^23 * 119 + 1
    
    def __init__(self, mod: int = 998244353):
        """初始化 NTT。"""
        self.MOD = mod
        if mod == 998244353:
            self.g = 3  # primitive root
        elif mod == 469762049:
            self.g = 3
        elif mod == 167772161:
            self.g = 3
        else:
            # Find primitive root for arbitrary prime
            self.g = self._find_primitive_root()
    
    def _find_primitive_root(self) -> int:
        """查找模数的原始根。"""
        # 分解 mod-1 的质因子
        divs = []
        x = self.MOD - 1
        d = 2
        while d * d <= x:
            if x % d == 0:
                divs.append(d)
                while x % d == 0:
                    x //= d
            d += 1
        if x > 1:
            divs.append(x)
        
        # 试验
        for g in range(2, self.MOD):
            ok = True
            for d in divs:
                if pow(g, (self.MOD - 1) // d, self.MOD) == 1:
                    ok = False
                    break
            if ok:
                return g
        return 2
    
    def ntt(self, a: List[int], inverse: bool = False) -> None:
        """
        原位 NTT 变换。
        
        Args:
            a: 多项式系数（长度必须为 2 的幂，原位修改）
            inverse: 是否为逆变换
        """
        n = len(a)
        if n == 1:
            return
        
        # 比特反转排列
        i = 0
        for j in range(1, n):
            k = n >> 1
            while i & k:
                i ^= k
                k >>= 1
            i ^= k
            if i > j:
                a[i], a[j] = a[j], a[i]
        
        # Cooley-Tukey NTT
        h = 1
        while h < n:
            # 计算单位根
            if inverse:
                w = pow(self.g, (self.MOD - 1) - (self.MOD - 1) // (h << 1), self.MOD)
            else:
                w = pow(self.g, (self.MOD - 1) // (h << 1), self.MOD)
            
            for i in range(0, n, h << 1):
                wn = 1
                for j in range(h):
                    u = a[i + j]
                    v = a[i + j + h] * wn % self.MOD
                    a[i + j] = (u + v) % self.MOD
                    a[i + j + h] = (u - v + self.MOD) % self.MOD
                    wn = wn * w % self.MOD
            
            h <<= 1
        
        if inverse:
            inv_n = pow(n, self.MOD - 2, self.MOD)
            for i in range(n):
                a[i] = a[i] * inv_n % self.MOD
    
    def convolve(self, a: List[int], b: List[int]) -> List[int]:
        """
        多项式卷积。
        
        Args:
            a, b: 多项式系数
            
        Returns:
            卷积结果
        """
        result_len = len(a) + len(b) - 1
        n = 1
        while n < result_len:
            n <<= 1
        
        a = a + [0] * (n - len(a))
        b = b + [0] * (n - len(b))
        
        self.ntt(a)
        self.ntt(b)
        
        for i in range(n):
            a[i] = a[i] * b[i] % self.MOD
        
        self.ntt(a, inverse=True)
        
        return a[:result_len]


class FFT(NTT):
    """FFT 别名。"""
    pass


def test_basic():
    """测试：(1 + 2x)(1 + 3x) = 1 + 5x + 6x^2"""
    ntt = NTT()
    result = ntt.convolve([1, 2], [1, 3])
    assert result == [1, 5, 6], f"Expected [1, 5, 6], got {result}"
    print("✓ test_basic passed")


def test_square():
    """测试：(1 + x)^2 = 1 + 2x + x^2"""
    ntt = NTT()
    result = ntt.convolve([1, 1], [1, 1])
    assert result == [1, 2, 1], f"Expected [1, 2, 1], got {result}"
    print("✓ test_square passed")


def test_larger():
    """测试：(1 + x + x^2)(1 + 2x)"""
    ntt = NTT()
    result = ntt.convolve([1, 1, 1], [1, 2])
    assert result == [1, 3, 3, 2], f"Expected [1, 3, 3, 2], got {result}"
    print("✓ test_larger passed")


if __name__ == "__main__":
    test_basic()
    test_square()
    test_larger()
    print("\n所有 NTT 测试通过！✓")
