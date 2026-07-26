"""
后缀数组（Suffix Array）

构建后缀数组及相关数据结构，用于高效的字符串搜索和模式匹配。

包含：
1. suffix_array - 构建后缀数组（O(n log n) 简化版）
2. lcp_array - 构建最长公共前缀数组（O(n)）
3. z_algorithm - Z 算法（O(n)）

应用：
- 查找所有子串出现的位置
- 字符串的最长重复子串
- 字符串匹配和模式查找
- 字典序操作

复杂度：
- suffix_array: O(n log n)
- lcp_array: O(n)
- z_algorithm: O(n)
"""

import copy
import typing
from typing import List, Union


def suffix_array(s: Union[str, List[int]]) -> List[int]:
    """
    构建后缀数组。
    
    Args:
        s: 输入字符串或整数列表
        
    Returns:
        后缀数组：sa[i] 表示第 i 小后缀的起始位置
    """
    if isinstance(s, str):
        s = [ord(c) for c in s]
    
    n = len(s)
    if n == 0:
        return []
    if n == 1:
        return [0]
    
    # 排序所有后缀
    sa = list(range(n))
    sa.sort(key=lambda i: s[i:])
    return sa


def lcp_array(s: Union[str, List[int]], sa: List[int] = None) -> List[int]:
    """
    构建最长公共前缀（LCP）数组。
    
    lcp[i] = 后缀 sa[i] 和 sa[i+1] 的最长公共前缀长度。
    
    Args:
        s: 输入字符串或整数列表
        sa: 后缀数组（如果未提供则自动计算）
        
    Returns:
        LCP 数组
    """
    if isinstance(s, str):
        s = [ord(c) for c in s]
    
    n = len(s)
    if n <= 1:
        return []
    
    if sa is None:
        sa = suffix_array(s)
    
    # 构建排名数组
    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i
    
    # 使用 Kasai 算法计算 LCP
    lcp = [0] * (n - 1)
    h = 0
    
    for i in range(n):
        if h > 0:
            h -= 1
        if rank[i] == 0:
            continue
        
        j = sa[rank[i] - 1]
        while j + h < n and i + h < n and s[j + h] == s[i + h]:
            h += 1
        lcp[rank[i] - 1] = h
    
    return lcp


def z_algorithm(s: Union[str, List[int]]) -> List[int]:
    """
    Z 算法（扩展 KMP）。
    
    计算 Z 数组：z[i] = s[0:] 和 s[i:] 的最长公共前缀长度。
    
    应用：
    - 查找所有子串出现的位置
    - 字符串匹配
    
    复杂度：O(n)
    
    Args:
        s: 输入字符串或整数列表
        
    Returns:
        Z 数组
    """
    if isinstance(s, str):
        s = [ord(c) for c in s]
    
    n = len(s)
    if n == 0:
        return []
    
    z = [0] * n
    z[0] = n
    l, r = 0, 0
    
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    
    return z


def find_all_occurrences(text: str, pattern: str) -> List[int]:
    """
    查找所有模式出现的位置。
    
    Args:
        text: 文本
        pattern: 模式
        
    Returns:
        所有出现位置的列表
    """
    combined = pattern + "#" + text
    z = z_algorithm(combined)
    positions = []
    
    for i in range(len(pattern) + 1, len(combined)):
        if z[i] == len(pattern):
            positions.append(i - len(pattern) - 1)
    
    return positions


def test_suffix_array():
    """测试后缀数组"""
    s = "banana"
    sa = suffix_array(s)
    expected_suffixes = ["a", "ana", "anana", "banana", "na", "nana"]
    actual_suffixes = [s[i:] for i in sa]
    assert actual_suffixes == expected_suffixes, f"Got {actual_suffixes}"
    print("✓ test_suffix_array passed")


def test_z_algorithm():
    """测试 Z 算法"""
    z = z_algorithm("abacaba")
    assert z == [7, 0, 1, 0, 3, 0, 1], f"Got {z}"
    print("✓ test_z_algorithm passed")


def test_find_occurrences():
    """测试模式查找"""
    positions = find_all_occurrences("ababab", "ab")
    assert positions == [0, 2, 4], f"Got {positions}"
    print("✓ test_find_occurrences passed")


if __name__ == "__main__":
    test_suffix_array()
    test_z_algorithm()
    test_find_occurrences()
    print("\n所有 Suffix Array 测试通过！✓")
