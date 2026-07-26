"""
位集合（Bitset）数据结构。

用于高效存储和操作大量布尔值。相比列表节省 63 倍空间。

支持的操作：
- 单个元素访问和修改
- 位逻辑操作：AND, OR, XOR, NOT
- 移位操作：左移、右移
- 统计操作：计数、查找

时间复杂度：
- 单个位的读写：O(1)
- 逻辑操作（两个 n 位的位集）：O(n/64)
- 计数：O(n/64)

空间：O(n/64) 字节
"""

from typing import Optional, List


def popcount(n: int) -> int:
    """
    计算整数 n 的二进制表示中 1 的个数。
    
    使用分治法快速计算。
    时间复杂度：O(1)
    
    Args:
        n: 非负整数
        
    Returns:
        n 的二进制表示中 1 的个数
    """
    n -= ((n >> 1) & 0x5555555555555555)
    n = (n & 0x3333333333333333) + ((n >> 2) & 0x3333333333333333)
    n = (n + (n >> 4)) & 0x0f0f0f0f0f0f0f0f
    n += ((n >> 8) & 0x00ff00ff00ff00ff)
    n += ((n >> 16) & 0x0000ffff0000ffff)
    n += ((n >> 32) & 0x00000000ffffffff)
    return n & 0x7f


class Bitset:
    """
    高效的位集合数据结构。
    
    使用 64 位整数数组存储位信息，内存效率是列表的 63 倍。
    
    属性：
    - n: 位集合的大小（位数）
    - m: 内部数组大小（每个整数 64 位，但我们用 63 位避免符号位问题）
    - data: 存储位数据的内部数组
    
    示例:
        >>> bs = Bitset(10)
        >>> bs[3] = 1
        >>> bs[7] = 1
        >>> bs.count()  # 有 2 个 1
        2
        >>> (bs >> 2).count()  # 右移 2 位后有 2 个 1
        2
    """
    
    # 每个整数的有效位数（使用 63 位避免符号位问题）
    BITS_PER_WORD = 63
    
    def __init__(self, n: int):
        """
        初始化大小为 n 的位集合，所有位初始为 0。
        
        Args:
            n: 位集合的大小
        """
        self.n = n
        self.m = (n + self.BITS_PER_WORD - 1) // self.BITS_PER_WORD
        self.data = [0] * self.m
    
    def __len__(self) -> int:
        """返回位集合的大小。"""
        return self.n
    
    @property
    def size(self) -> int:
        """返回位集合的大小。"""
        return self.n
    
    def __str__(self) -> str:
        """
        返回位集合的字符串表示（二进制）。
        
        从高位到低位显示。
        """
        bits = []
        for word in self.data:
            # 将每个 64 位整数转换为二进制字符串（63 位）
            bits.append(bin(word)[2:].zfill(self.BITS_PER_WORD)[::-1])
        
        # 拼接并截取到实际大小
        full_bits = "".join(bits)[:self.n]
        return full_bits[::-1]
    
    def __repr__(self) -> str:
        """返回位集合的代码表示。"""
        return f"Bitset({self.n}, {self.count()} ones)"
    
    def __getitem__(self, index: int) -> int:
        """
        获取指定位置的值。
        
        Args:
            index: 位置（0 到 n-1）
            
        Returns:
            该位的值（0 或 1）
        """
        if index < 0 or index >= self.n:
            raise IndexError(f"Bitset index out of range: {index}")
        
        word_idx = index // self.BITS_PER_WORD
        bit_idx = index % self.BITS_PER_WORD
        return (self.data[word_idx] >> bit_idx) & 1
    
    def __setitem__(self, index: int, value: int) -> None:
        """
        设置指定位置的值。
        
        Args:
            index: 位置（0 到 n-1）
            value: 新值（0 或 1）
        """
        if index < 0 or index >= self.n:
            raise IndexError(f"Bitset index out of range: {index}")
        
        word_idx = index // self.BITS_PER_WORD
        bit_idx = index % self.BITS_PER_WORD
        
        if value:
            # 设置第 bit_idx 位为 1
            self.data[word_idx] |= (1 << bit_idx)
        else:
            # 设置第 bit_idx 位为 0
            self.data[word_idx] &= ~(1 << bit_idx)
    
    def flip(self, index: int) -> None:
        """
        翻转指定位置的值（0→1, 1→0）。
        
        Args:
            index: 位置（0 到 n-1）
        """
        if index < 0 or index >= self.n:
            raise IndexError(f"Bitset index out of range: {index}")
        
        word_idx = index // self.BITS_PER_WORD
        bit_idx = index % self.BITS_PER_WORD
        self.data[word_idx] ^= (1 << bit_idx)
    
    def count(self) -> int:
        """
        计算位集合中 1 的个数。
        
        时间复杂度：O(m)，其中 m = n / 63
        
        Returns:
            1 的个数
        """
        total = 0
        for word in self.data:
            total += popcount(word)
        return total
    
    def __bool__(self) -> bool:
        """检查是否至少有一个 1。"""
        return any(word != 0 for word in self.data)
    
    def any(self) -> bool:
        """检查是否至少有一个 1。"""
        return any(word != 0 for word in self.data)
    
    def all(self) -> bool:
        """检查是否所有位都是 1。"""
        for i, word in enumerate(self.data):
            if i == self.m - 1:
                # 最后一个字，可能有多余位
                bits_in_last = self.n % self.BITS_PER_WORD
                if bits_in_last == 0:
                    bits_in_last = self.BITS_PER_WORD
                expected = (1 << bits_in_last) - 1
                if word != expected:
                    return False
            else:
                # 前面的字应该全是 1
                if word != (1 << self.BITS_PER_WORD) - 1:
                    return False
        return True
    
    def reset(self) -> None:
        """将所有位重置为 0。"""
        for i in range(self.m):
            self.data[i] = 0
    
    def set_all(self) -> None:
        """将所有位设置为 1。"""
        for i in range(self.m):
            self.data[i] = (1 << self.BITS_PER_WORD) - 1
        
        # 清除最后一个字的多余位
        if self.n % self.BITS_PER_WORD != 0:
            mask = (1 << (self.n % self.BITS_PER_WORD)) - 1
            self.data[-1] &= mask
    
    def resize(self, new_size: int) -> None:
        """
        调整位集合的大小。
        
        Args:
            new_size: 新的大小
        """
        new_m = (new_size + self.BITS_PER_WORD - 1) // self.BITS_PER_WORD
        
        if new_m > self.m:
            # 扩大
            self.data.extend([0] * (new_m - self.m))
        elif new_m < self.m:
            # 缩小
            self.data = self.data[:new_m]
            # 清除最后一个字的多余位
            if new_size % self.BITS_PER_WORD != 0:
                mask = (1 << (new_size % self.BITS_PER_WORD)) - 1
                self.data[-1] &= mask
        
        self.n = new_size
        self.m = new_m
    
    def find_first(self) -> Optional[int]:
        """
        找到第一个 1 的位置。
        
        Returns:
            第一个 1 的位置，如果没有 1 则返回 None
        """
        for word_idx, word in enumerate(self.data):
            if word != 0:
                # 找这个字内的第一个 1
                for bit_idx in range(self.BITS_PER_WORD):
                    if (word >> bit_idx) & 1:
                        return word_idx * self.BITS_PER_WORD + bit_idx
        return None
    
    def find_last(self) -> Optional[int]:
        """
        找到最后一个 1 的位置。
        
        Returns:
            最后一个 1 的位置，如果没有 1 则返回 None
        """
        for word_idx in range(self.m - 1, -1, -1):
            word = self.data[word_idx]
            if word != 0:
                # 找这个字内的最后一个 1
                for bit_idx in range(self.BITS_PER_WORD - 1, -1, -1):
                    if (word >> bit_idx) & 1:
                        pos = word_idx * self.BITS_PER_WORD + bit_idx
                        if pos < self.n:
                            return pos
        return None
    
    # 逻辑操作
    
    def __and__(self, other: 'Bitset') -> 'Bitset':
        """
        按位与。
        
        结果大小为两个位集合大小的最小值。
        """
        result_size = min(self.n, other.n)
        result = Bitset(result_size)
        
        for i in range(result.m):
            result.data[i] = self.data[i] & other.data[i]
        
        return result
    
    def __iand__(self, other: 'Bitset') -> 'Bitset':
        """原地按位与。"""
        for i in range(min(self.m, other.m)):
            self.data[i] &= other.data[i]
        
        # 清除多余的字
        for i in range(min(self.m, other.m), self.m):
            self.data[i] = 0
        
        return self
    
    def __or__(self, other: 'Bitset') -> 'Bitset':
        """按位或。"""
        result_size = max(self.n, other.n)
        result = Bitset(result_size)
        
        for i in range(result.m):
            if i < self.m and i < other.m:
                result.data[i] = self.data[i] | other.data[i]
            elif i < self.m:
                result.data[i] = self.data[i]
            else:
                result.data[i] = other.data[i]
        
        return result
    
    def __ior__(self, other: 'Bitset') -> 'Bitset':
        """原地按位或。"""
        # 确保足够的空间
        if other.m > self.m:
            self.data.extend([0] * (other.m - self.m))
            self.m = other.m
            self.n = max(self.n, other.n)
        
        for i in range(min(self.m, other.m)):
            self.data[i] |= other.data[i]
        
        return self
    
    def __xor__(self, other: 'Bitset') -> 'Bitset':
        """按位异或。"""
        result_size = max(self.n, other.n)
        result = Bitset(result_size)
        
        for i in range(result.m):
            if i < self.m and i < other.m:
                result.data[i] = self.data[i] ^ other.data[i]
            elif i < self.m:
                result.data[i] = self.data[i]
            else:
                result.data[i] = other.data[i]
        
        return result
    
    def __ixor__(self, other: 'Bitset') -> 'Bitset':
        """原地按位异或。"""
        if other.m > self.m:
            self.data.extend([0] * (other.m - self.m))
            self.m = other.m
            self.n = max(self.n, other.n)
        
        for i in range(min(self.m, other.m)):
            self.data[i] ^= other.data[i]
        
        return self
    
    def __invert__(self) -> 'Bitset':
        """按位取反。"""
        result = Bitset(self.n)
        
        for i in range(self.m):
            result.data[i] = ~self.data[i]
        
        # 清除多余的位
        if self.n % self.BITS_PER_WORD != 0:
            mask = (1 << (self.n % self.BITS_PER_WORD)) - 1
            result.data[-1] &= mask
        
        return result
    
    # 统计操作
    
    def and_count(self, other: 'Bitset') -> int:
        """计算按位与的结果中 1 的个数。"""
        count = 0
        for i in range(min(self.m, other.m)):
            count += popcount(self.data[i] & other.data[i])
        return count
    
    def or_count(self, other: 'Bitset') -> int:
        """计算按位或的结果中 1 的个数。"""
        count = 0
        
        # 共同部分
        for i in range(min(self.m, other.m)):
            count += popcount(self.data[i] | other.data[i])
        
        # 非共同部分
        if self.m > other.m:
            for i in range(other.m, self.m):
                count += popcount(self.data[i])
        else:
            for i in range(self.m, other.m):
                count += popcount(other.data[i])
        
        return count
    
    def xor_count(self, other: 'Bitset') -> int:
        """计算按位异或的结果中 1 的个数。"""
        count = 0
        
        # 共同部分
        for i in range(min(self.m, other.m)):
            count += popcount(self.data[i] ^ other.data[i])
        
        # 非共同部分
        if self.m > other.m:
            for i in range(other.m, self.m):
                count += popcount(self.data[i])
        else:
            for i in range(self.m, other.m):
                count += popcount(other.data[i])
        
        return count
    
    # 移位操作
    
    def __rshift__(self, shift: int) -> 'Bitset':
        """右移 shift 位。"""
        if shift < 0:
            raise ValueError("Negative shift count")
        if shift >= self.n:
            return Bitset(self.n)
        
        result = Bitset(self.n)
        
        # 按字移位
        word_shift = shift // self.BITS_PER_WORD
        bit_shift = shift % self.BITS_PER_WORD
        
        # 复制数据
        for i in range(word_shift, self.m):
            result.data[i - word_shift] = self.data[i]
        
        # 按位移位
        if bit_shift != 0:
            mask = (1 << bit_shift) - 1
            for i in range(result.m):
                if i + 1 < result.m:
                    # 从高字取低位，移到当前字的高位
                    result.data[i] = (result.data[i] >> bit_shift) | \
                                     ((result.data[i + 1] & mask) << (self.BITS_PER_WORD - bit_shift))
                else:
                    result.data[i] = result.data[i] >> bit_shift
        
        return result
    
    def __irshift__(self, shift: int) -> 'Bitset':
        """原地右移。"""
        if shift < 0:
            raise ValueError("Negative shift count")
        if shift >= self.n:
            self.reset()
            return self
        
        word_shift = shift // self.BITS_PER_WORD
        bit_shift = shift % self.BITS_PER_WORD
        
        # 移动数据
        for i in range(self.m - word_shift):
            self.data[i] = self.data[i + word_shift]
        
        for i in range(self.m - word_shift, self.m):
            self.data[i] = 0
        
        # 按位移位
        if bit_shift != 0:
            mask = (1 << bit_shift) - 1
            for i in range(self.m):
                if i + 1 < self.m:
                    self.data[i] = (self.data[i] >> bit_shift) | \
                                   ((self.data[i + 1] & mask) << (self.BITS_PER_WORD - bit_shift))
                else:
                    self.data[i] = self.data[i] >> bit_shift
        
        return self
    
    def __lshift__(self, shift: int) -> 'Bitset':
        """左移 shift 位。"""
        if shift < 0:
            raise ValueError("Negative shift count")
        if shift == 0:
            result = Bitset(self.n)
            for i in range(self.m):
                result.data[i] = self.data[i]
            return result
        
        result = Bitset(self.n)
        
        word_shift = shift // self.BITS_PER_WORD
        bit_shift = shift % self.BITS_PER_WORD
        
        # 从后往前复制（避免覆盖）
        for i in range(self.m - 1, -1, -1):
            if i + word_shift < result.m:
                result.data[i + word_shift] = self.data[i]
        
        # 按位移位
        if bit_shift != 0:
            for i in range(result.m - 1, -1, -1):
                result.data[i] <<= bit_shift
                if i > 0:
                    # 从低字的高位取数
                    result.data[i] |= result.data[i - 1] >> (self.BITS_PER_WORD - bit_shift)
        
        return result
    
    def __ilshift__(self, shift: int) -> 'Bitset':
        """原地左移。"""
        if shift < 0:
            raise ValueError("Negative shift count")
        if shift == 0:
            return self
        
        word_shift = shift // self.BITS_PER_WORD
        bit_shift = shift % self.BITS_PER_WORD
        
        # 从后往前移动字
        for i in range(self.m - 1, word_shift - 1, -1):
            self.data[i] = self.data[i - word_shift]
        
        for i in range(min(word_shift, self.m)):
            self.data[i] = 0
        
        # 按位移位
        if bit_shift != 0:
            for i in range(self.m - 1, -1, -1):
                self.data[i] <<= bit_shift
                if i > 0:
                    self.data[i] |= self.data[i - 1] >> (self.BITS_PER_WORD - bit_shift)
        
        return self
        return self

def test_bitset():
    """测试 Bitset"""
    bs = Bitset(10)
    bs[3] = 1
    bs[5] = 1
    assert bs[3] == 1, "bit 3 should be 1"
    assert bs[4] == 0, "bit 4 should be 0"
    print("✓ test_set_get passed")
    
    # 计数
    assert bs.count() == 2, "Should have 2 ones"
    print("✓ test_count passed")


if __name__ == "__main__":
    test_bitset()
    print("\n所有 Bitset 测试通过！✓")
