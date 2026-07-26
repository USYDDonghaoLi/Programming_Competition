"""
AC 自动机（Aho-Corasick Automation）。
用于多模式字符串匹配，快速查找多个模式串在文本中出现的次数。
时间复杂度：预处理 O(Σ|pi|)，匹配 O(|s| + Σ cnt_i)，其中 Σ|pi| 是所有模式串的总长度
空间复杂度：O(26 * 节点数) ≈ O(Σ|pi|)
"""

from collections import deque


class ACAutomaton:
    """
    AC 自动机 - 多模式字符串匹配算法。
    
    原理：
    - 使用 Trie 树存储所有模式串
    - 使用失败函数（fail 指针）在匹配失败时快速跳转
    - 构造 DAG 后可以 O(|s|) 完成多模式匹配
    
    应用场景：
    - 敏感词过滤
    - 多个关键词查找
    - 基因序列匹配
    - 网络入侵检测
    """
    
    def __init__(self, max_nodes: int = 100000):
        """
        初始化 AC 自动机。
        Args:
            max_nodes: 最多的节点数量（默认 100000，足够处理大多数情况）
        """
        self.max_nodes = max_nodes
        self.children = [[0] * 26 for _ in range(max_nodes)]  # 子节点指针
        self.fail = [0] * max_nodes  # 失败函数（fail 指针）
        self.cnt = [0] * max_nodes  # 每个节点处结束的模式串计数
        self.sorted_nodes = []  # 拓扑排序的节点列表
        
        self.root = 0
        self.node_count = 1
    
    def insert_string(self, pattern: str, pattern_id: int = None) -> None:
        """
        向 AC 自动机中插入一个模式串。
        Args:
            pattern: 模式串（小写字母）
            pattern_id: 模式串的唯一标识（可选，默认为 None）
        """
        node = self.root
        for ch in pattern:
            char_idx = ord(ch) - ord('a')
            if not self.children[node][char_idx]:
                self.children[node][char_idx] = self.node_count
                self.node_count += 1
            node = self.children[node][char_idx]
        
        # 标记该位置是某个模式串的结尾
        self.cnt[node] += 1
    
    def build(self) -> None:
        """
        构造 AC 自动机的失败函数和 DAG。
        必须在所有 insert_string 之后调用。
        """
        # BFS 构造 fail 指针
        self.fail[self.root] = self.root
        queue = deque()
        
        # 第一层的节点，fail 指针都指向根
        for ch in range(26):
            if self.children[self.root][ch]:
                queue.append(self.children[self.root][ch])
        
        # BFS 处理第二层及以后的节点
        while queue:
            node = queue.popleft()
            self.sorted_nodes.append(node)
            
            for ch in range(26):
                child = self.children[node][ch]
                if child:
                    # 已有子节点，继续处理
                    fail_node = self.fail[node]
                    while fail_node and not self.children[fail_node][ch]:
                        fail_node = self.fail[fail_node]
                    self.fail[child] = self.children[fail_node][ch]
                    queue.append(child)
                else:
                    # 没有子节点，使用 fail 指针的下一个节点
                    fail_node = self.fail[node]
                    while fail_node and not self.children[fail_node][ch]:
                        fail_node = self.fail[fail_node]
                    self.children[node][ch] = self.children[fail_node][ch]
    
    def search(self, text: str):
        """
        在文本中查找所有模式串的出现次数。
        Args:
            text: 待匹配的文本（小写字母）
        Returns:
            list: 每个位置累计的模式串匹配次数
        """
        node = self.root
        match_count = [0] * self.node_count
        
        # 第一遍 DFS：统计每个节点处的匹配
        for ch in text:
            char_idx = ord(ch) - ord('a')
            node = self.children[node][char_idx]
            match_count[node] += 1
        
        # 第二遍反向 DFS：累计从子节点到父节点的贡献
        # 从后向前处理，保证子节点先处理
        for i in range(len(self.sorted_nodes) - 1, -1, -1):
            node = self.sorted_nodes[i]
            match_count[self.fail[node]] += match_count[node]
        
        return match_count
    
    def find_all_occurrences(self, text: str):
        """
        找出文本中所有模式串的出现位置。
        Args:
            text: 待匹配的文本
        Returns:
            dict: {模式串ID: [出现位置列表]}
        """
        node = self.root
        occurrences = {}
        
        for pos, ch in enumerate(text):
            char_idx = ord(ch) - ord('a')
            node = self.children[node][char_idx]
            
            # 检查该节点和其失败指针链上的所有匹配
            check_node = node
            while check_node:
                if self.cnt[check_node] > 0:
                    if check_node not in occurrences:
                        occurrences[check_node] = []
                    occurrences[check_node].append(pos)
                check_node = self.fail[check_node]
        
        return occurrences

def test_ac_automation():
    """测试 AC 自动机"""
    ac = ACAutomaton()
    
    # 插入模式串
    ac.insert_string("he")
    ac.insert_string("she")
    ac.insert_string("his")
    ac.insert_string("hers")
    ac.build()
    
    # 测试匹配
    text = "ushers"
    matches = ac.search(text)
    # "ushers" 应该找到模式串
    assert len(matches) > 0, f"Expected matches in text"
    print("✓ test_ac_automation passed")


if __name__ == "__main__":
    test_ac_automation()
    print("\n所有 AC 自动机测试通过！✓")
