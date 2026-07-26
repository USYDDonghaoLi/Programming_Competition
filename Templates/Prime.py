class Prime:
    """
    素数相关算法库。
    包含：素数筛法、素因数分解、所有因子枚举、原根计算等。
    """
    
    def _prime_sieve(self, n: int) -> bytearray:
        """
        使用轮筛法（wheel factorization）生成素数筛。
        返回筛去 5 到 n 之间的合数的布尔数组。
        时间复杂度：O(n log log n)
        Args:
            n: 上限
        Returns:
            bit 数组，其中 bit=1 表示合数，bit=0 表示素数
        """
        flag = n % 6 == 2
        sieve = bytearray((n // 3 + flag >> 3) + 1)
        for i in range(1, int(n**0.5) // 3 + 1):
            if not (sieve[i >> 3] >> (i & 7)) & 1:
                k = (3 * i + 1) | 1
                for j in range(k * k // 3, n // 3 + flag, 2 * k):
                    sieve[j >> 3] |= 1 << (j & 7)
                for j in range(k * (k - 2 * (i & 1) + 4) // 3, n // 3 + flag, 2 * k):
                    sieve[j >> 3] |= 1 << (j & 7)
        return sieve

    def prime_list(self, n: int) -> list:
        """
        生成不超过 n 的所有素数。
        时间复杂度：O(n log log n)
        Args:
            n: 上限
        Returns:
            素数列表
        """
        result = []
        if n > 1:
            result.append(2)
        if n > 2:
            result.append(3)
        if n > 4:
            sieve = self._prime_sieve(n + 1)
            result.extend(
                3 * i + 1 | 1 
                for i in range(1, (n + 1) // 3 + (n % 6 == 1)) 
                if not (sieve[i >> 3] >> (i & 7)) & 1
            )
        return result
    
    def __init__(self, n: int) -> None:
        """
        初始化素数库。
        Args:
            n: 最大素数上限
        """
        self.primes = self.prime_list(n)
    
    def factorize(self, num: int) -> list:
        """
        对 num 进行素因数分解。
        时间复杂度：O(sqrt(num))
        Args:
            num: 要分解的数
        Returns:
            [[prime1, count1], [prime2, count2], ...] 形式，其中 count >= 1
        """
        factors = []
        for prime in self.primes:
            if prime * prime > num:
                break
            if num % prime == 0:
                count = 0
                while num % prime == 0:
                    count += 1
                    num //= prime
                factors.append([prime, count])
        
        if num != 1:
            factors.append([num, 1])
        
        return factors

    def get_all_factors(self, num: int, sort: bool = False) -> list:
        """
        获取 num 的所有因子（包括 1 和 num 本身）。
        时间复杂度：O(d(num) * log num)，其中 d(num) 是因子个数
        Args:
            num: 数值
            sort: 是否对结果排序
        Returns:
            所有因子的列表
        """
        if num == 1:
            return [1]
        
        factors = [1]
        for prime, exponent in self.factorize(num):
            multiplier = prime
            prev_len = len(factors)
            for _ in range(exponent):
                for i in range(prev_len):
                    factors.append(factors[i] * multiplier)
                multiplier *= prime
        
        if sort:
            factors.sort()
        
        return factors
    
    def primitive_root(self, num: int) -> int:
        """
        计算 num 的原根（前提：num 必须是素数）。
        原根 g 满足：对于所有与 num 互质的 a，存在唯一的 k 使得 g^k ≡ a (mod num)。
        时间复杂度：O(d(num-1) * log num)
        Args:
            num: 素数
        Returns:
            最小的原根
        """
        factors = self.factorize(num - 1)

        g = 1
        while True:
            is_root = True
            for prime, _ in factors:
                if pow(g, (num - 1) // prime, num) == 1:
                    is_root = False
                    break
            if is_root:
                return g
            g += 1

#     def is_prime(self, x:int):
#         if x < 2: return False
#         if x <= self.n: return self.max_div[x] == x
#         for p in self.primes:
#             if p * p > x: break
#             if x % p == 0: return False
#         return True

#     def prime_factorization(self, x:int):
#         if x > self.n:
#             for p in self.primes:
#                 if p * p > x: break
#                 if x <= self.n: break
#                 if x % p == 0:
#                     cnt = 0
#                     while x % p == 0: cnt += 1; x //= p
#                     yield p, cnt
#         while (1 < x and x <= self.n):
#             p, cnt = self.max_div[x], 0
#             while x % p == 0: cnt += 1; x //= p
#             yield p, cnt
#         if x >= self.n and x > 1:
#             yield x, 1

#     def get_factors(self, x:int):
#         factors = [1]
#         for p, b in self.prime_factorization(x):
#             n = len(factors)
#             for j in range(1, b+1):
#                 for d in factors[:n]:
#                     factors.append(d * (p ** j))
#         return factors
