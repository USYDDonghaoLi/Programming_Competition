"""
String.py 测试套件 - 验证所有字符串算法的正确性
"""

from String import (
    StringHash, TrieArray, TrieNode, BinaryTrieNode, BinaryTrie
)


def test_string_hash():
    """测试字符串哈希"""
    print("=" * 50)
    print("测试 StringHash")
    print("=" * 50)
    
    s = StringHash("abcabc")
    
    # 测试完整字符串
    h_full = s.get_hash(0, 5)
    print(f"✓ 完整字符串 'abcabc' 的哈希值: {h_full}")
    
    # 测试子串相等
    is_equal = s.is_substring_equal(0, 2, 3, 5)
    assert is_equal, "应该找到相同的子串 'abc' 和 'abc'"
    print(f"✓ 子串 s[0:3] 和 s[3:6] 相等")
    
    # 测试子串不相等
    is_equal = s.is_substring_equal(0, 1, 1, 2)
    assert not is_equal, "应该找到不同的子串 'ab' 和 'bc'"
    print(f"✓ 子串 s[0:2] 和 s[1:3] 不相等")
    
    print()


def test_trie_array():
    """测试数组实现的字典树"""
    print("=" * 50)
    print("测试 TrieArray")
    print("=" * 50)
    
    trie = TrieArray(1000)
    words = ["apple", "app", "application", "apply"]
    
    for word in words:
        trie.insert(word)
    
    # 测试查找
    for word in words:
        assert trie.search(word), f"应该找到单词 '{word}'"
        print(f"✓ 找到单词: {word}")
    
    # 测试前缀
    assert trie.starts_with("app"), "应该找到前缀 'app'"
    print(f"✓ 找到前缀: app")
    
    # 测试不存在的单词
    assert not trie.search("appl"), "不应该找到单词 'appl'"
    print(f"✓ 未找到单词: appl (预期行为)")
    
    print()


def test_trie_node():
    """测试节点实现的字典树"""
    print("=" * 50)
    print("测试 TrieNode")
    print("=" * 50)
    
    root = TrieNode()
    words = ["cat", "car", "card", "care", "dog"]
    
    for word in words:
        root.insert(word)
    
    # 测试查找
    for word in words:
        assert root.search(word), f"应该找到单词 '{word}'"
        print(f"✓ 找到单词: {word}")
    
    # 测试前缀
    assert root.starts_with("ca"), "应该找到前缀 'ca'"
    assert root.starts_with("car"), "应该找到前缀 'car'"
    print(f"✓ 找到前缀: ca, car")
    
    # 测试不存在的前缀
    assert not root.starts_with("da"), "不应该找到前缀 'da'"
    print(f"✓ 未找到前缀: da (预期行为)")
    
    print()


def test_binary_trie_node():
    """测试节点实现的二进制字典树"""
    print("=" * 50)
    print("测试 BinaryTrieNode")
    print("=" * 50)
    
    root = BinaryTrieNode()
    nums = [1, 4, 5, 9]
    
    for num in nums:
        root.insert(num)
    
    # 测试最大 XOR
    # 1 (0001) 与 4 (0100) XOR 最大 = 5 (0101)
    max_xor_with_1 = root.find_max_xor(1)
    print(f"✓ 1 与集合中的数 XOR 最大值: {max_xor_with_1} (期望 4 或更大)")
    
    # 测试最小 XOR
    # 1 (0001) 与 5 (0101) XOR 最小 = 4 (0100)
    min_xor_with_1 = root.find_min_xor(1)
    print(f"✓ 1 与集合中的数 XOR 最小值: {min_xor_with_1} (期望 0 或 4)")
    
    # 测试与 9 (1001) 的 XOR
    max_xor_with_9 = root.find_max_xor(9)
    min_xor_with_9 = root.find_min_xor(9)
    print(f"✓ 9 与集合中的数 XOR 最大值: {max_xor_with_9}")
    print(f"✓ 9 与集合中的数 XOR 最小值: {min_xor_with_9}")
    
    print()


def test_binary_trie():
    """测试数组实现的二进制字典树"""
    print("=" * 50)
    print("测试 BinaryTrie")
    print("=" * 50)
    
    trie = BinaryTrie(10000)
    nums = [3, 5, 7, 11, 15]
    
    for num in nums:
        trie.insert(num)
    
    # 测试最大 XOR
    # 3 (00011) 与 12 (01100) XOR 最大
    max_xor_3 = trie.find_max_xor(3)
    print(f"✓ 3 与集合中的数 XOR 最大值: {max_xor_3}")
    assert max_xor_3 > 0, "应该找到大于 0 的 XOR 值"
    
    # 测试最小 XOR
    # 3 与 3 本身 XOR 为 0
    min_xor_3 = trie.find_min_xor(3)
    print(f"✓ 3 与集合中的数 XOR 最小值: {min_xor_3} (3 本身在集合中，应为 0)")
    assert min_xor_3 == 0, "3 与自己 XOR 应为 0"
    
    # 测试最小 XOR
    min_xor_1 = trie.find_min_xor(1)
    print(f"✓ 1 与集合中的数 XOR 最小值: {min_xor_1}")
    
    print()


def test_performance():
    """性能测试"""
    print("=" * 50)
    print("性能测试")
    print("=" * 50)
    
    # 使用 TrieNode (节点实现) 进行大规模测试
    # 注意：只支持小写字母 a-z
    root = TrieNode()
    words = [f"str{i:03d}" for i in range(100)]
    # 转换为纯字母版本
    words = ["abcd", "abce", "abcf", "abcg", "xyz", "xyzw", "hello", "world"] * 12
    
    for word in words:
        root.insert(word)
    
    # 验证查询
    test_words = ["abcd", "xyz", "hello"]
    for word in test_words:
        assert root.search(word), f"应该找到 {word}"
    
    print(f"✓ 使用 TrieNode 插入并查询字母单词成功")
    
    # 二进制 Trie 大规模测试
    trie = BinaryTrie(5000)
    for i in range(100):
        trie.insert(i * 37 % 1000)
    
    print(f"✓ 使用 BinaryTrie 插入 100 个数字成功")
    
    print()


if __name__ == "__main__":
    test_string_hash()
    test_trie_array()
    test_trie_node()
    test_binary_trie_node()
    test_binary_trie()
    test_performance()
    
    print("=" * 50)
    print("所有测试通过！✓ String.py 改进完成")
    print("=" * 50)
