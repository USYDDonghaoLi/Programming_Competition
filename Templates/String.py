"""
字符串算法库 - 包含字符串哈希、字典树等常用数据结构和算法。
"""


class StringHash:
    """
    字符串哈希（前缀哈希）。用于快速比较子串是否相等。
    时间复杂度：初始化 O(n)，查询 O(1)
    空间复杂度：O(n)
    """

    __slots__ = {'n', 'base', 'mod', 'power', 'hash_val'}

    def __init__(self, string: str, base: int = 131, mod: int = 10**9 + 7):
        """
        初始化字符串哈希。
        Args:
            string: 输入字符串（小写字母）
            base: 哈希基数（通常选素数）
            mod: 模数（避免哈希冲突）
        """
        self.n = len(string)
        self.base = base
        self.mod = mod

        # 预计算 base 的幂次
        self.power = [1] * (self.n + 1)
        for i in range(1, self.n + 1):
            self.power[i] = self.power[i - 1] * self.base % self.mod

        # 前缀哈希值，hash_val[i] = s[0..i-1] 的哈希
        self.hash_val = [0] * (self.n + 1)
        for i in range(1, self.n + 1):
            self.hash_val[i] = (self.hash_val[i - 1] * self.base + ord(string[i - 1]) - ord('a') + 1) % self.mod
    
    def get_hash(self, left: int, right: int) -> int:
        """
        获取子串 s[left..right] 的哈希值（0-indexed，闭区间）。
        Args:
            left: 左端点
            right: 右端点
        Returns:
            子串的哈希值
        """
        assert right >= left, "右端点必须 >= 左端点"
        return (self.hash_val[right + 1] - self.hash_val[left] * self.power[right - left + 1]) % self.mod
    
    def is_substring_equal(self, l1: int, r1: int, l2: int, r2: int) -> bool:
        """
        判断两个子串是否相等。
        Args:
            l1, r1: 第一个子串的端点（0-indexed，闭区间）
            l2, r2: 第二个子串的端点（0-indexed，闭区间）
        Returns:
            两个子串是否相等
        """
        assert r1 - l1 == r2 - l2, "两个子串长度必须相同"
        return self.get_hash(l1, r1) == self.get_hash(l2, r2)


class TrieArray:
    """
    字典树（Trie Tree）- 数组实现版本。
    用于存储和查询一组字符串，支持前缀匹配。
    时间复杂度：插入和查找都是 O(m)，其中 m 是字符串长度
    空间复杂度：O(字母表大小 × 节点数)
    """
    
    __slots__ = {'node_count', 'children', 'is_end'}

    def __init__(self, max_nodes: int):
        """
        初始化 Trie。
        Args:
            max_nodes: 最多的节点数
        """
        self.node_count = 1  # 根节点
        # children[i][c] = 节点 i 的字符 c 对应的子节点编号
        self.children = [[0] * 26 for _ in range(max_nodes)]
        self.is_end = [False] * max_nodes
    
    def insert(self, word: str) -> None:
        """
        向 Trie 中插入一个单词。
        Args:
            word: 待插入的单词（小写字母）
        """
        node = 0
        for ch in word:
            char_idx = ord(ch) - ord('a')
            if not self.children[node][char_idx]:
                self.node_count += 1
                self.children[node][char_idx] = self.node_count - 1
            node = self.children[node][char_idx]
        self.is_end[node] = True
    
    def search(self, word: str) -> bool:
        """
        查找单词是否完整存在于 Trie 中。
        Args:
            word: 待查询的单词
        Returns:
            单词是否存在
        """
        node = 0
        for ch in word:
            char_idx = ord(ch) - ord('a')
            if not self.children[node][char_idx]:
                return False
            node = self.children[node][char_idx]
        return self.is_end[node]
    
    def starts_with(self, prefix: str) -> bool:
        """
        检查 Trie 中是否存在以给定前缀开头的单词。
        Args:
            prefix: 前缀
        Returns:
            是否存在这样的前缀
        """
        node = 0
        for ch in prefix:
            char_idx = ord(ch) - ord('a')
            if not self.children[node][char_idx]:
                return False
            node = self.children[node][char_idx]
        return True


class TrieNode:
    """
    字典树节点 - 用于 Trie Tree 的节点实现。
    每个节点包含 26 个指向子节点的指针（小写字母 a-z）。
    """
    
    def __init__(self):
        """
        初始化 Trie 节点。
        """
        self.children = [None] * 26  # children[i] 表示字符 chr(ord('a')+i) 的子节点
        self.is_end = False  # 标记是否为某个单词的结尾
    
    def insert(self, word: str) -> None:
        """
        从该节点开始插入一个单词。
        Args:
            word: 待插入的单词（小写字母）
        """
        node = self
        for ch in word:
            char_idx = ord(ch) - ord('a')
            if not node.children[char_idx]:
                node.children[char_idx] = TrieNode()
            node = node.children[char_idx]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        """
        查找单词是否完整存在。
        Args:
            word: 待查询的单词
        Returns:
            单词是否存在
        """
        node = self
        for ch in word:
            char_idx = ord(ch) - ord('a')
            if not node.children[char_idx]:
                return False
            node = node.children[char_idx]
        return node.is_end
    
    def starts_with(self, prefix: str) -> bool:
        """
        检查是否存在以给定前缀开头的单词。
        Args:
            prefix: 前缀
        Returns:
            是否存在这样的前缀
        """
        node = self
        for ch in prefix:
            char_idx = ord(ch) - ord('a')
            if not node.children[char_idx]:
                return False
            node = node.children[char_idx]
        return True


class BinaryTrieNode:
    """
    二进制字典树节点 - 用于 XOR 相关问题。
    每个节点有两个子节点，表示二进制的 0 和 1。
    """
    
    __slots__ = {'children'}

    def __init__(self):
        """
        初始化二进制 Trie 节点。
        children[0] 表示二进制 0，children[1] 表示二进制 1
        """
        self.children = [None, None]
    
    def insert(self, num: int) -> None:
        """
        插入一个整数的二进制表示。
        Args:
            num: 待插入的整数
        """
        node = self
        for bit in range(31, -1, -1):
            bit_val = (num >> bit) & 1
            if not node.children[bit_val]:
                node.children[bit_val] = BinaryTrieNode()
            node = node.children[bit_val]

    def find_max_xor(self, num: int) -> int:
        """
        找与 num XOR 结果最大的数。
        原理：尽可能选择与 num 的当前位相反的分支。
        Args:
            num: 输入数
        Returns:
            最大 XOR 结果
        """
        result = 0
        node = self
        for bit in range(31, -1, -1):
            bit_val = (num >> bit) & 1
            # 优先选择相反的位（1 XOR 0 = 1, 0 XOR 1 = 1）
            if node.children[1 - bit_val]:
                result |= 1 << bit
                node = node.children[1 - bit_val]
            else:
                node = node.children[bit_val]
        return result
    
    def find_min_xor(self, num: int) -> int:
        """
        找与 num XOR 结果最小的数。
        原理：尽可能选择与 num 的当前位相同的分支。
        Args:
            num: 输入数
        Returns:
            最小 XOR 结果
        """
        result = 0
        node = self
        for bit in range(31, -1, -1):
            bit_val = (num >> bit) & 1
            # 优先选择相同的位（0 XOR 0 = 0, 1 XOR 1 = 0）
            if node.children[bit_val]:
                node = node.children[bit_val]
            else:
                result |= 1 << bit
                node = node.children[1 - bit_val]
        return result


class BinaryTrie:
    """
    二进制字典树 - 数组实现版本。
    用于 XOR 相关问题，支持快速找最大/最小 XOR 值。
    时间复杂度：插入 O(log n)，查询 O(log n)（n 是最大数值）
    空间复杂度：O(节点数 × 2)
    """
    
    __slots__ = {'node_count', 'children'}

    def __init__(self, max_nodes: int):
        """
        初始化二进制 Trie。
        Args:
            max_nodes: 最多的节点数
        """
        self.node_count = 1  # 根节点
        # children[i][bit] = 节点 i 的第 bit 位对应的子节点编号
        self.children = [[0, 0] for _ in range(max_nodes)]
    
    def insert(self, num: int) -> None:
        """
        插入一个整数的二进制表示。
        Args:
            num: 待插入的整数
        """
        node = 0
        for bit in range(31, -1, -1):
            bit_val = (num >> bit) & 1
            if not self.children[node][bit_val]:
                self.node_count += 1
                self.children[node][bit_val] = self.node_count - 1
            node = self.children[node][bit_val]
    
    def find_max_xor(self, num: int) -> int:
        """
        找与 num XOR 结果最大的数。
        Args:
            num: 输入数
        Returns:
            最大 XOR 结果
        """
        node = 0
        result = 0
        for bit in range(31, -1, -1):
            bit_val = (num >> bit) & 1
            # 优先选择相反的位
            if self.children[node][1 - bit_val]:
                result |= 1 << bit
                node = self.children[node][1 - bit_val]
            else:
                node = self.children[node][bit_val]
        return result
    
    def find_min_xor(self, num: int) -> int:
        """
        找与 num XOR 结果最小的数。
        Args:
            num: 输入数
        Returns:
            最小 XOR 结果
        """
        node = 0
        result = 0
        for bit in range(31, -1, -1):
            bit_val = (num >> bit) & 1
            # 优先选择相同的位
            if self.children[node][bit_val]:
                node = self.children[node][bit_val]
            else:
                result |= 1 << bit
                node = self.children[node][1 - bit_val]
        return result
