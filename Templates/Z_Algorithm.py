def z_algorithm(s: str) -> list:
    """
    Z 算法：线性时间计算前缀数组。
    Z[i] = S[i:] 与 S 的最长公共前缀长度。
    时间复杂度：O(n)
    
    应用：
    - 字符串匹配：将 pattern + '$' + text 构造新串，Z[i] == len(pattern) 即为匹配位置
    - 周期性检测：若 i + Z[i] == n 且 i 是最小周期则为周期点
    
    Args:
        s: 输入字符串
    Returns:
        Z 数组，其中 Z[0] = len(s)，Z[i] 表示 s[i:] 与 s 的最长公共前缀长度
    
    Example:
        z_algorithm("aaab") -> [4, 2, 1, 0]
        z_algorithm("abcabc") -> [6, 0, 0, 3, 0, 0]
    """
    n = len(s)
    z_array = [0] * n
    left = right = 0  # [left, right] 是当前已知的最远匹配区间

    for i in range(1, n):
        # 利用已知信息快速初始化
        z_val = z_array[i - left] if i <= right else 0
        
        # 如果超出已知区间，需要重新计算
        if i + z_val > right:
            z_val = max(right - i, 0)
            while i + z_val < n and s[z_val] == s[i + z_val]:
                z_val += 1
            left, right = i, i + z_val

        z_array[i] = z_val

    z_array[0] = n
    return z_array