'''
Hala Madrid!
https://github.com/USYDDonghaoLi/Programming_Competition
'''

import sys
import os
from io import BytesIO, IOBase
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

def I():
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
def LGMI():
    return list(map(lambda x: int(x) - 1, input().split()))

#------------------------------FastIO---------------------------------

from bisect import *
from heapq import *
from collections import *
from functools import *
from itertools import *
from time import *
from random import *
from math import log, gcd, sqrt, ceil

# from types import GeneratorType
# def bootstrap(f, stack=[]):
#     def wrappedfunc(*args, **kwargs):
#         if stack:
#             return f(*args, **kwargs)
#         else:
#             to = f(*args, **kwargs)
#             while True:
#                 if type(to) is GeneratorType:
#                     stack.append(to)
#                     to = next(to)
#                 else:
#                     stack.pop()
#                     if not stack:
#                         break
#                     to = stack[-1].send(to)
#             return to
#     return wrappedfunc

# seed(19981220)
# RANDOM = getrandbits(64)
 
# class Wrapper(int):
#     def __init__(self, x):
#         int.__init__(x)

#     def __hash__(self):
#         return super(Wrapper, self).__hash__() ^ RANDOM

# def TIME(f):

#     def wrap(*args, **kwargs):
#         s = perf_counter()
#         ret = f(*args, **kwargs)
#         e = perf_counter()

#         print(e - s, 'sec')
#         return ret
    
#     return wrap

inf = float('inf')

fmin = lambda x, y: x if x < y else y
fmax = lambda x, y: x if x > y else y

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

P = Prime(500)

mod = 10 ** 9 + 7

"""
阶乘、组合数与中国剩余定理。

提供三个主要功能：
1. Factorial：模 mod 的阶乘与组合数（模数为质数）
2. Lucas：Lucas 定理（用于计算大数模质数的 C(n, m)）
3. ChineseRemainderTheorem：中国剩余定理
"""

from typing import List, Tuple


class Factorial:
    """
    预计算阶乘与其模逆元，支持快速计算模质数的组合数。
    
    时间复杂度：
    - 预计算：O(n log mod)
    - 单次查询 C(n, m)：O(1)
    
    空间：O(n)
    
    属性：
    - factorial[i] = i! mod p
    - inv_factorial[i] = (i!)^(-1) mod p
    - inv[i] = i^(-1) mod p（数值的模逆）
    """
    
    def __init__(self, n: int, mod: int):
        """
        初始化阶乘和逆元表。
        
        Args:
            n: 预计算的最大值
            mod: 模数（通常是质数）
        """
        self.n = n
        self.mod = mod
        
        # 计算阶乘：fact[i] = i!
        self.factorial = [1] * (n + 1)
        for i in range(1, n + 1):
            self.factorial[i] = self.factorial[i - 1] * i % self.mod
        
        # 计算阶乘的模逆：inv_fact[i] = (i!)^(-1) mod p
        # 使用费马小定理：a^(-1) ≡ a^(p-2) (mod p)
        self.inv_factorial = [1] * (n + 1)
        self.inv_factorial[n] = pow(self.factorial[n], self.mod - 2, self.mod)
        
        # 反向计算逆元
        # inv_fact[i] = inv_fact[i+1] * (i+1)
        for i in range(n - 1, -1, -1):
            self.inv_factorial[i] = self.inv_factorial[i + 1] * (i + 1) % self.mod
        
        # 计算模逆：inv[i] = i^(-1) mod p
        # 使用递推：inv[i] = -(p // i) * inv[p % i] mod p
        self.inv = [0] * (n + 1)
        self.inv[0] = self.inv[1] = 1
        for i in range(2, n + 1):
            self.inv[i] = (self.mod - self.mod // i) * self.inv[self.mod % i] % self.mod
    
    def combination(self, n: int, m: int) -> int:
        """
        计算 C(n, m) mod p。
        
        时间复杂度：O(1)
        
        Args:
            n, m: 参数
            
        Returns:
            C(n, m) mod p = n! / (m! * (n-m)!)
            
        示例:
            >>> fact = Factorial(10, 1000000007)
            >>> fact.combination(5, 2)
            10  # C(5, 2) = 10
        """
        if n < m or n < 0 or m < 0:
            return 0
        
        return (self.factorial[n] * self.inv_factorial[m] % self.mod) * \
               self.inv_factorial[n - m] % self.mod
    
    def permutation(self, n: int, m: int) -> int:
        """
        计算 P(n, m) mod p（排列数）。
        
        时间复杂度：O(1)
        
        Args:
            n, m: 参数
            
        Returns:
            P(n, m) mod p = n! / (n-m)!
        """
        if n < m or n < 0 or m < 0:
            return 0
        
        return self.factorial[n] * self.inv_factorial[n - m] % self.mod
    
    def catalan(self, n: int) -> int:
        """
        计算 Catalan 数 C_n mod p。
        
        时间复杂度：O(1)
        
        Catalan 数定义：C_n = C(2n, n) / (n+1) = C(2n, n) - C(2n, n-1)
        
        Args:
            n: 参数
            
        Returns:
            第 n 个 Catalan 数模 p
            
        应用：括号匹配数、二叉树个数、满二叉树个数等
        """
        if 2 * n >= self.n + 1:
            raise ValueError(f"n 过大，需要预计算 {2 * n} 但只预计算到 {self.n}")
        
        c2n_n = self.combination(2 * n, n)
        c2n_n1 = self.combination(2 * n, n - 1) if n > 0 else 0
        
        return (c2n_n - c2n_n1) % self.mod


class Lucas:
    """
    Lucas 定理：用于计算 C(n, m) mod p，其中 p 是小质数，n 和 m 可以很大。
    
    定理：对于质数 p，C(n, m) ≡ ∏ C(n_i, m_i) (mod p)
    其中 n_i 和 m_i 分别是 n 和 m 在 p 进制下的第 i 位。
    
    时间复杂度：O(p + log_p(n))
    
    适用场景：
    - p 是较小的质数（如 10^9 + 7 不适用，用 Factorial 代替）
    - n 很大（超过 10^5）
    - m 相对较小
    """
    
    def __init__(self, p: int):
        """
        初始化 Lucas 定理。
        
        Args:
            p: 质数（应该是较小的质数，如 10007, 998244353 等）
        """
        self.p = p
        
        # 预计算 1 到 p-1 的阶乘和逆元
        self.factorial = [1] * p
        for i in range(1, p):
            self.factorial[i] = self.factorial[i - 1] * i % p
        
        # 计算 (p-1)! 的逆元
        self.inv_factorial = [1] * p
        self.inv_factorial[p - 1] = pow(self.factorial[p - 1], p - 2, p)
        
        # 反向计算其他逆元
        for i in range(p - 2, -1, -1):
            self.inv_factorial[i] = self.inv_factorial[i + 1] * (i + 1) % p
    
    def combination_small(self, n: int, m: int) -> int:
        """
        计算 n < p 且 m < p 时的 C(n, m) mod p。
        
        Args:
            n, m: 参数
            
        Returns:
            C(n, m) mod p
        """
        if n < m or m < 0:
            return 0
        
        return (self.factorial[n] * self.inv_factorial[m] % self.p) * \
               self.inv_factorial[n - m] % self.p
    
    def lucas(self, n: int, m: int) -> int:
        """
        使用 Lucas 定理计算 C(n, m) mod p。
        
        递归地将 n 和 m 分解为 p 进制，然后计算各位的组合数乘积。
        
        时间复杂度：O(log_p(n) + p)
        
        Args:
            n, m: 参数（可以很大）
            
        Returns:
            C(n, m) mod p
            
        示例:
            >>> luc = Lucas(13)
            >>> luc.lucas(100, 50)
            # 计算 C(100, 50) mod 13
        """
        if m == 0:
            return 1
        
        # Lucas 定理：C(n, m) ≡ C(n_k, m_k) * C(n_{k-1}, m_{k-1}) * ... (mod p)
        # 其中 n_i, m_i 是 n, m 在 p 进制下的第 i 位
        return (self.lucas(n // self.p, m // self.p) * 
                self.combination_small(n % self.p, m % self.p)) % self.p


class ChineseRemainderTheorem:
    """
    中国剩余定理（CRT）与扩展欧几里得算法。
    
    用于解同余方程组：
    - x ≡ b_0 (mod a_0)
    - x ≡ b_1 (mod a_1)
    - ...
    
    时间复杂度：O(k log M)，其中 k 是方程个数，M 是所有模数的乘积
    """
    
    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        扩展欧几里得算法。
        
        找到 x, y 使得 ax + by = gcd(a, b)。
        
        Args:
            a, b: 参数
            
        Returns:
            (x, y, gcd) 其中 ax + by = gcd
        """
        if b == 0:
            return 1, 0, a
        else:
            x, y, gcd_val = ChineseRemainderTheorem.extended_gcd(b, a % b)
            return y, x - (a // b) * y, gcd_val
    
    @staticmethod
    def crt(moduli: List[int], residues: List[int]) -> int:
        """
        使用中国剩余定理求解同余方程组。
        
        要求所有模数两两互质。
        
        Args:
            moduli: 模数列表 [a_0, a_1, ...]
            residues: 余数列表 [b_0, b_1, ...]
            
        Returns:
            满足所有条件的 x（在所有模数乘积范围内唯一）
            
        示例:
            >>> crt([3, 5, 7], [2, 3, 2])
            # 求解：x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)
            # 答案：x = 23（在 3*5*7=105 范围内）
        """
        M = 1
        for m in moduli:
            M *= m
        
        result = 0
        for a, b in zip(moduli, residues):
            M_i = M // a
            x, _, _ = ChineseRemainderTheorem.extended_gcd(M_i, a)
            result += b * M_i * x
            result %= M
        
        return result
    
    @staticmethod
    def crt_non_coprime(moduli: List[int], residues: List[int]) -> Tuple[int, int]:
        """
        扩展 CRT 处理非互质的模数。
        
        （高级功能，如需使用，建议单独处理）
        
        Args:
            moduli: 模数列表（不要求互质）
            residues: 余数列表
            
        Returns:
            (solution, lcm) 其中 solution 是答案，lcm 是所有模数的最小公倍数
        """
        if not moduli:
            return 0, 1
        
        from math import gcd as math_gcd
        
        x, m = residues[0], moduli[0]
        
        for i in range(1, len(moduli)):
            a1, r1 = moduli[i], residues[i]
            g = math_gcd(m, a1)
            
            if (r1 - x) % g != 0:
                return None, None  # 无解
            
            # 求解方程：x + m*k ≡ r1 (mod a1)
            x, m = x, m // g * a1
        
        return x % m, m


    # 同余方程组，A数组是mod数组，B数组是residue数组
    # 可能有无解的情况
    def excrt(self, A, B):
        res, M = 0, 1
        for a, b in zip(A, B):
            rhs = (b - res) % a
            #g, l代表最大公约数，最小公倍数#
            g = gcd(M, a)
            l = M * a // g
            
            if rhs % g:
                return -1, -1
            x, y, q = self.exgcd(M, a)
            res += x * rhs // g * M
            res %= l
            M = l
        return res, M

    def lcm(self, a, b):
        return a * b // gcd(a, b)

    #wx = b(mod a)的同余方程组，记得重写lcm#
    def excrt_with_weight(self, W, A, B):
        res, M = 0, 1
        for w, a, b in zip(W, A, B):
            rhs = (b - w * res) % a
            x, _, g = self.exgcd(w * M % a, a)
            if rhs % g:
                return -1, -1
            res += x * (rhs // g) % (a // g) * M
            M = self.lcm(M, a // gcd(a, w))
            res %= M
        return res, M

class Prime:
    def prime_sieve(self, n):
        """returns a sieve of primes >= 5 and < n"""
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

    def prime_list(self, n):
        """returns a list of primes <= n"""
        res = []
        if n > 1:
            res.append(2)
        if n > 2:
            res.append(3)
        if n > 4:
            sieve = self.prime_sieve(n + 1)
            res.extend(3 * i + 1 | 1 for i in range(1, (n + 1) // 3 + (n % 6 == 1)) if not (sieve[i >> 3] >> (i & 7)) & 1)
        return res
    
    def __init__(self, n) -> None:
        self.primes = self.prime_list(n)
    
    def dissolve(self, num):
        '''prime factor decomposition of num'''
        lst = []
        idx = -1
        for prime in self.primes:
            if prime > num:
                break

            if num % prime == 0:
                lst.append([prime, 0])
                idx += 1
                
            while num % prime == 0:
                lst[idx][1] += 1
                num //= prime
                
        if num != 1:
            lst.append([num, 1])
            
        return lst

class Ex_Lucas:
        
    def __init__(self, p) -> None:
        #TODO: 把CRT, Prime板子也带上
        self.CRT = Crt()
        self.PRIME = Prime(10 ** 5 + 10)

        #分解质因子
        self.p = p
        self.dissolved = self.PRIME.dissolve(p)
        
        self.piset = []
        self.m = []
        self.num = 0
        for pr, pw in self.dissolved:
            self.m.append(pr ** pw)
            self.piset.append(pr)
            self.num += 1
    
    #找循环节#
    def multi(self, n, pi, pk):
        if not n:
            return 1
        ans = 1
        for i in range(2, pk + 1):
            if i % pi:
                ans = ans * i % pk
        ans = pow(ans, n // pk, pk)
        for i in range(2, n % pk + 1):
            if i % pi:
                ans = ans * i % pk
        return ans * self.multi(n // pi, pi, pk) % pk

    def count(self, num, p):
        ret = 0
        while num:
            ret += num // p
            num //= p
        return ret
    
    def inv(self, num, p):
        return self.CRT.exgcd(num, p)[0]
    
    #pi是质因数pr，pk是质因数pr的pw次方#
    def exlucas(self, n, m, pi, pk):
        if m > n:
            return 0
        a = self.multi(n, pi, pk)
        b = self.multi(m, pi, pk)
        c = self.multi(n - m, pi, pk)
        k = self.count(n, pi) - self.count(m, pi) - self.count(n - m, pi)
        return a * self.inv(b, pk) % pk * self.inv(c, pk) % pk * pow(pi, k, pk) % pk
    
    def comb(self, n, m):
        self.r = [-1 for _ in range(self.num)]
        for i in range(self.num):
            self.r[i] = self.exlucas(n, m, self.piset[i], self.m[i])
        return self.CRT.crt(self.m, self.r, self.p)


F = Factorial(200010, mod)


# @TIME
def solve(testcase):
    n = II()
    A = LII()

    mp = defaultdict(int)

    for a in A:
        for d in P.get_all_factors(a):
            mp[d] += 1
    
    B = [-1 for _ in range(n + 1)]
    for d in mp:
        cnt = mp[d]
        B[cnt] = fmax(B[cnt], d)
    
    for i in range(n - 1, -1, -1):
        B[i] = fmax(B[i], B[i + 1])
    
    q = II()
    for _ in range(q):
        k = II()
        val = B[k]
        tot = mp[val]
        print(F.combination(tot, k))


for testcase in range(1):
    solve(testcase)