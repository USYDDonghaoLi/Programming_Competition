"""
位运算工具库。

包含：
- 位计数（popcount）：计算整数的二进制表示中 1 的个数
- 子集枚举（enumerate_subsets）：枚举一个掩码的所有非空子集
"""


def popcount(n: int) -> int:
    """
    计算整数 n 的二进制表示中 1 的个数（汉明权重）。
    
    使用 Brian Kernighan 算法的位运算优化版本。
    该实现采用"分治"的思路：
    1. 将相邻的位两两相加（汉明距离）
    2. 递归地将结果合并，最终得到总计数
    
    时间复杂度：O(1)（对 64 位整数）
    
    Args:
        n: 非负整数
        
    Returns:
        n 的二进制表示中 1 的个数
        
    示例:
        >>> popcount(7)        # 0b111 = 3
        3
        >>> popcount(12)       # 0b1100 = 2
        2
        >>> popcount(15)       # 0b1111 = 4
        4
    """
    # 第一步：相邻1位分组计算
    # 0x5555555555555555 = 0101010101...（奇数位掩码）
    c = (n & 0x5555555555555555) + ((n >> 1) & 0x5555555555555555)
    
    # 第二步：2位数据分组计算
    # 0x3333333333333333 = 0011001100...（每4位中的低2位掩码）
    c = (c & 0x3333333333333333) + ((c >> 2) & 0x3333333333333333)
    
    # 第三步：4位数据分组计算
    # 0x0F0F0F0F0F0F0F0F = 00001111...（每8位的低4位掩码）
    c = (c & 0x0F0F0F0F0F0F0F0F) + ((c >> 4) & 0x0F0F0F0F0F0F0F0F)
    
    # 第四步：8位数据分组计算
    c = (c & 0x00FF00FF00FF00FF) + ((c >> 8) & 0x00FF00FF00FF00FF)
    
    # 第五步：16位数据分组计算
    c = (c & 0x0000FFFF0000FFFF) + ((c >> 16) & 0x0000FFFF0000FFFF)
    
    # 第六步：32位数据分组计算（得到最终结果）
    c = (c & 0x00000000FFFFFFFF) + ((c >> 32) & 0x00000000FFFFFFFF)
    
    return c


def popcount_builtin(n: int) -> int:
    """
    使用 Python 内置函数计算位数（推荐）。
    
    Python 3.10+ 内置 int.bit_count()，速度更快。
    对于旧版本，此函数可作为备选。
    
    时间复杂度：O(1)
    
    Args:
        n: 非负整数
        
    Returns:
        n 的二进制表示中 1 的个数
    """
    return bin(n).count('1')


def enumerate_subsets(mask: int) -> list:
    """
    枚举一个掩码的所有非空子集。
    
    子集的定义：S 是 mask 的子集当且仅当 S & mask == S。
    
    算法：
    1. 从 mask 开始
    2. 重复执行 sub = (sub - 1) & mask
    3. 直到 sub == 0（即已枚举所有子集）
    
    时间复杂度：O(3^popcount(mask))
    空间复杂度：O(2^popcount(mask))
    
    Args:
        mask: 掩码（通常是某些位的组合）
        
    Returns:
        mask 的所有非空子集列表
        
    示例:
        >>> enumerate_subsets(0b101)
        [5, 4, 1]  # 0b101, 0b100, 0b001
        
        >>> enumerate_subsets(0b111)
        [7, 6, 5, 4, 3, 2, 1]  # 所有从 7 到 1 的子集
    """
    if mask == 0:
        return []
    
    subsets = []
    sub = mask
    
    while sub > 0:
        subsets.append(sub)
        sub = (sub - 1) & mask  # 得到下一个子集
    
    return subsets


def enumerate_subsets_including_empty(mask: int) -> list:
    """
    枚举一个掩码的所有子集，包括空集。
    
    Args:
        mask: 掩码
        
    Returns:
        mask 的所有子集列表（包括空集）
        
    示例:
        >>> enumerate_subsets_including_empty(0b11)
        [3, 2, 1, 0]  # 0b11, 0b10, 0b01, 0b00
    """
    subsets = []
    sub = mask
    
    while True:
        subsets.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask
    
    return subsets


def is_power_of_two(n: int) -> bool:
    """
    判断一个整数是否是 2 的幂次。
    
    时间复杂度：O(1)
    
    Args:
        n: 正整数
        
    Returns:
        True 如果 n 是 2 的幂次，否则 False
        
    示例:
        >>> is_power_of_two(8)
        True
        >>> is_power_of_two(6)
        False
    """
    return n > 0 and (n & (n - 1)) == 0


def count_trailing_zeros(n: int) -> int:
    """
    计算 n 的二进制表示末尾 0 的个数。
    
    时间复杂度：O(1)
    
    Args:
        n: 正整数
        
    Returns:
        n 的末尾 0 的个数
        
    示例:
        >>> count_trailing_zeros(8)  # 0b1000
        3
        >>> count_trailing_zeros(12)  # 0b1100
        2
    """
    if n == 0:
        return 0
    return (n & -n).bit_length() - 1


def highest_power_of_two(n: int) -> int:
    """
    找到不超过 n 的最大 2 的幂次。
    
    时间复杂度：O(log n)
    
    Args:
        n: 正整数
        
    Returns:
        不超过 n 的最大 2 的幂次
        
    示例:
        >>> highest_power_of_two(10)
        8
        >>> highest_power_of_two(16)
        16
    """
    return 1 << (n.bit_length() - 1)
