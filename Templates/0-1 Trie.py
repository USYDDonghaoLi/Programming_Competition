"""
0-1 Trie（二进制字典树）

用于处理二进制数字的 Trie，特别用于异或问题。

特点：
- 按二进制位分层构建
- 支持快速 XOR 最大/最小值查询
- 支持插入、删除、查询操作

应用：
- XOR 最大值问题
- XOR 基向量空间
- 线性基优化

复杂度：
- 插入/删除/查询：O(log MAX_VAL)
- 空间：O(n * log MAX_VAL)
"""

class TrieNode:

    __slots__ = {'count', 'children'}

    def __init__(self):
        self.count = 0
        self.children = [None, None]

class Trie:

    __slots__ = {'root', 'MAX_BIT'}

    def __init__(self):
        self.root = TrieNode()
        self.MAX_BIT = 30

    def insert(self, num):
        node = self.root
        for bit in range(self.MAX_BIT, -1, -1):
            bitVal = (num >> bit) & 1
            if node.children[bitVal] is None:
                node.children[bitVal] = TrieNode()
            node = node.children[bitVal]
            node.count += 1

    def delete(self, num):
        node = self.root
        for bit in range(self.MAX_BIT, -1, -1):
            bitVal = (num >> bit) & 1
            if node.children[bitVal] is None:
                return  # element does not exist
            node = node.children[bitVal]
            node.count -= 1

    def maxXor(self, num):
        node = self.root
        max_xor = 0
        for bit in range(self.MAX_BIT, -1, -1):
            bitVal = (num >> bit) & 1
            if node.children[1 - bitVal] and node.children[1 - bitVal].count > 0:
                max_xor |= (1 << bit)
                node = node.children[1 - bitVal]
            else:
                node = node.children[bitVal]
        return max_xor

    def minXor(self, num):
        node = self.root
        min_xor = 0
        for bit in range(self.MAX_BIT, -1, -1):
            bitVal = (num >> bit) & 1
            if node.children[bitVal] and node.children[bitVal].count > 0:
                node = node.children[bitVal]
            else:
                min_xor |= (1 << bit)
                node = node.children[1 - bitVal]
        return min_xor
    
    def countXorLessThan(self, num, limit):
        node = self.root
        count = 0
        for bit in range(self.MAX_BIT, -1, -1):
            bitVal = (num >> bit) & 1
            limitBit = (limit >> bit) & 1
            if limitBit:
                if node.children[bitVal] is not None:
                    count += node.children[bitVal].count
                if node.children[1 - bitVal] is not None:
                    node = node.children[1 - bitVal]
                else:
                    break
            else:
                if node.children[bitVal] is not None:
                    node = node.children[bitVal]
                else:
                    break
        return count
    
    def countXorLessThanEqual(self, num, limit):
        return self.countXorLessThan(num, limit + 1)

    def countXorGreaterThan(self, num, limit):
        total = sum(c.count for c in self.root.children if c is not None)
        return total - self.countXorLessThanEqual(num, limit)

    def countXorGreatThanEqual(self, num, limit):
        total = sum(c.count for c in self.root.children if c is not None)
        return total - self.countXorLessThan(num, limit)