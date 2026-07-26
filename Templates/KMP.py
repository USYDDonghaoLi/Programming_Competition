class KMP:
    """
    KMP（Knuth-Morris-Pratt）字符串匹配算法。
    用于在文本中查找模式串，时间复杂度 O(n + m)。
    """
    
    def __init__(self, text: str, pattern: str):
        """
        初始化 KMP 匹配器。
        Args:
            text: 文本串（待搜索）
            pattern: 模式串（待查找）
        """
        self.text = ' ' + text  # 添加哨兵以使用 1-indexed
        self.pattern = ' ' + pattern  # 添加哨兵
        self.n = len(text)
        self.m = len(pattern)
        
        # failure[i] = pattern[1..i] 的最长真前缀后缀长度
        self.failure = [0] * (self.m + 1)
        # matched_len[i] = text[1..i] 匹配 pattern 的长度
        self.matched_len = [0] * (self.n + 1)

    def _build_failure_function(self) -> None:
        """
        构建失败函数（也称为 next 数组或前缀函数）。
        failure[i] 表示 pattern[1..i] 的最长真前缀后缀长度。
        时间复杂度：O(m)
        """
        j = 0
        for i in range(2, self.m + 1):
            # 当不匹配时，向后跳转
            while j > 0 and self.pattern[j + 1] != self.pattern[i]:
                j = self.failure[j]
            # 匹配则增加长度
            if self.pattern[j + 1] == self.pattern[i]:
                j += 1
            self.failure[i] = j

    def search(self) -> list:
        """
        在文本中搜索所有模式串出现的位置。
        时间复杂度：O(n + m)
        Returns:
            模式串出现位置的列表（1-indexed 位置）
        """
        self._build_failure_function()
        j = 0
        matches = []
        
        for i in range(1, self.n + 1):
            # 当不匹配时，向后跳转
            while j == self.m or (j > 0 and self.pattern[j + 1] != self.text[i]):
                j = self.failure[j]
            # 匹配则增加长度
            if self.pattern[j + 1] == self.text[i]:
                j += 1
            self.matched_len[i] = j
            
            # 找到完全匹配
            if j == self.m:
                matches.append(i - self.m + 1)
        
        return matches

    def get_failure_function(self) -> list:
        """
        获取失败函数数组（不包括哨兵）。
        Returns:
            failure[1:] 的列表
        """
        self._build_failure_function()
        return self.failure[1:]

    def get_matched_lengths(self) -> list:
        """
        获取每个位置的匹配长度数组。
        Returns:
            matched_len[1:] 的列表
        """
        self.search()
        return self.matched_len[1:]


def test_kmp():
    """测试 KMP 算法"""
    # 基本测试
    kmp = KMP("abcabcabc", "abc")
    result = kmp.search()
    assert result == [1, 4, 7], f"Expected [1, 4, 7], got {result}"
    print("✓ test_basic passed")
    
    # 无匹配
    kmp = KMP("abcdef", "xyz")
    result = kmp.search()
    assert result == [], f"Expected [], got {result}"
    print("✓ test_no_match passed")
    
    # 重叠匹配
    kmp = KMP("aaaa", "aa")
    result = kmp.search()
    assert result == [1, 2, 3], f"Expected [1, 2, 3], got {result}"
    print("✓ test_overlapping passed")


if __name__ == "__main__":
    test_kmp()
    print("\n所有 KMP 测试通过！✓")
