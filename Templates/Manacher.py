"""
Manacher 算法：线性时间找所有回文子串。

用于快速找出字符串中的所有回文子串（回文长度）。

时间复杂度：O(n)
空间复杂度：O(n)

核心思想：
1. 在每个字符和字符间插入分隔符（如 '#'），使偶数长度回文转换为奇数长度
2. 维护回文中心和右边界
3. 对称性优化：利用已计算的对称位置的回文信息

应用：
- 找最长回文子串
- 计算所有回文子串
- 统计特定长度的回文
"""

from typing import List, Tuple


def manacher(s: str, separator: str = '#') -> Tuple[List[int], str]:
    """
    Manacher 算法：找所有回文子串的长度。
    
    Args:
        s: 输入字符串
        separator: 分隔符（默认 '#'）
        
    Returns:
        (radius, expanded_s)
        - radius[i] 是以 expanded_s[i] 为中心的回文半径（包括中心）
        - expanded_s 是插入分隔符后的字符串
        
    示例:
        >>> radius, exp_s = manacher("ababa")
        >>> # 找最长回文子串的长度
        >>> max_radius = max(radius)
        >>> palindrome_length = 2 * (max_radius - 1) + 1  # 5
    """
    # 插入分隔符，使得所有回文都变成奇数长度
    # 格式：separator + char1 + separator + char2 + ... + separator
    expanded = [separator]
    for char in s:
        expanded.append(char)
        expanded.append(separator)
    
    n = len(expanded)
    
    # radius[i] = 以 i 为中心、包括中心的回文半径
    # 即 expanded[i-radius[i]:i+radius[i]+1] 是回文
    radius = [0] * n
    
    # center 和 right 维护当前找到的最右回文的中心和右边界
    center = 0
    right = 0
    
    for i in range(n):
        # 镜像位置
        mirror = 2 * center - i
        
        # 初始化 radius[i]
        if i >= right:
            # i 在当前最右回文外，暴力扩展
            radius[i] = 0
        else:
            # i 在当前最右回文内，利用对称性
            # radius[i] 至少等于 radius[mirror]（或受边界限制）
            radius[i] = min(radius[mirror], right - i)
        
        # 尝试扩展
        while (i - radius[i] - 1 >= 0 and 
               i + radius[i] + 1 < n and
               expanded[i - radius[i] - 1] == expanded[i + radius[i] + 1]):
            radius[i] += 1
        
        # 更新最右回文的中心和右边界
        if i + radius[i] > right:
            center = i
            right = i + radius[i]
    
    return radius, ''.join(expanded)


def find_all_palindromes(s: str) -> List[Tuple[int, int, str]]:
    """
    找所有回文子串。
    
    Args:
        s: 输入字符串
        
    Returns:
        列表，每个元素是 (start, end, palindrome_str)
        其中 [start, end) 是原字符串中回文的范围
        
    示例:
        >>> find_all_palindromes("aba")
        [(0, 1, 'a'), (0, 3, 'aba'), (2, 3, 'a')]
    """
    if not s:
        return []
    
    radius, expanded = manacher(s)
    n = len(s)
    palindromes = []
    
    for i in range(len(expanded)):
        if radius[i] > 0:
            # 将 expanded 中的位置转换回原字符串的位置
            # expanded 中：separator 在偶数位，字符在奇数位
            # radius[i] 中：计数包括中心的分隔符
            
            center_in_original = (i - 1) // 2
            pal_len = radius[i] - 1  # 减去中心的分隔符贡献
            
            start = center_in_original - (pal_len // 2)
            end = center_in_original + (pal_len // 2) + 1
            
            if 0 <= start and end <= n:
                palindromes.append((start, end, s[start:end]))
    
    return palindromes


def longest_palindrome_substring(s: str) -> Tuple[str, int, int]:
    """
    找最长回文子串。
    
    Args:
        s: 输入字符串
        
    Returns:
        (palindrome_str, start, end)
        
    示例:
        >>> longest_palindrome_substring("babad")
        ('bab', 0, 3)
    """
    if not s:
        return "", 0, 0
    
    radius, expanded = manacher(s)
    
    # 找最长回文
    max_radius = 0
    best_center = 0
    for i in range(len(expanded)):
        if radius[i] > max_radius:
            max_radius = radius[i]
            best_center = i
    
    if max_radius == 0:
        return s[0], 0, 1
    
    # 将中心位置转换回原字符串
    center_in_original = (best_center - 1) // 2
    pal_len = max_radius - 1
    
    start = center_in_original - (pal_len // 2)
    end = center_in_original + (pal_len // 2) + 1
    
    return s[start:end], start, end


def count_palindromic_substrings(s: str) -> int:
    """
    统计所有回文子串的个数。
    
    Args:
        s: 输入字符串
        
    Returns:
        回文子串的个数
        
    示例:
        >>> count_palindromic_substrings("abc")
        3  # "a", "b", "c"
        >>> count_palindromic_substrings("aba")
        4  # "a", "b", "a", "aba"
    """
    if not s:
        return 0
    
    radius, _ = manacher(s)
    
    # 每个位置对应的回文个数 = (radius - 1 + 1) // 2（四舍五入）
    # 实际上，expanded[i] 处的所有回文个数 = radius[i]
    # 但要注意，不是所有位置都对应原字符串的回文
    
    total = 0
    for i in range(len(radius)):
        # 只计算奇数位（对应原字符串的字符）
        if i % 2 == 1:
            # 以 s[(i-1)//2] 为中心的回文个数
            # radius[i] 给出了最大回文半径
            total += (radius[i] + 1) // 2
    
    return total


# 旧版本的兼容接口
def manacher_old_style(string: str) -> List[int]:
    """
    Manacher 算法的旧风格接口（直接返回结果长度列表）。
    
    返回每个原始位置对应的最长回文长度。
    
    Args:
        string: 输入字符串
        
    Returns:
        长度列表
    """
    radius, _ = manacher(string)
    
    result = []
    for i in range(len(string)):
        # expanded 中对应的位置是 2*i + 1
        expanded_idx = 2 * i + 1
        r = radius[expanded_idx]
        
        # 以原字符串位置 i 为中心的回文长度
        # odd_length = 2*r - 1（r 包括中心的分隔符）
        # even_length = 2*(r-1)
        result.append(r - 1)
    
    return result


    return res