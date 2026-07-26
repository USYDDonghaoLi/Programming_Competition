"""
UnionFind 大规模数据测试
验证迭代路径压缩在超过递归限制时的表现
"""

import sys
sys.path.insert(0, '/Users/wangzhinuo/Desktop/Ldh/Programming_Competition/Templates')

from UnionFind import UnionFind


def test_large_chain():
    """测试超长链（超过1000个节点）"""
    print("=" * 50)
    print("测试 1: 超长链（2000 个节点）")
    print("=" * 50)
    
    n = 2000
    uf = UnionFind(n)
    
    # 创建一条长链：0-1-2-3-...1999
    for i in range(1, n):
        uf.union(i-1, i)
    
    # 测试多个位置的查询
    test_positions = [0, 500, 1000, 1500, 1999]
    print(f"测试位置的根节点查询:")
    for pos in test_positions:
        root = uf.find(pos)
        print(f"  find({pos}) = {root}")
    
    assert uf.get_component_count() == 1, "应该只有 1 个分量"
    print(f"✓ 连通分量数: {uf.get_component_count()}")
    print()


def test_multiple_chains():
    """测试多条不相连的长链"""
    print("=" * 50)
    print("测试 2: 多条长链（5 条 × 400 节点）")
    print("=" * 50)
    
    n = 2000
    chain_count = 5
    chain_len = n // chain_count
    
    uf = UnionFind(n)
    
    # 创建 5 条独立的长链
    for chain_id in range(chain_count):
        start = chain_id * chain_len
        for i in range(start + 1, start + chain_len):
            uf.union(i - 1, i)
    
    print(f"创建了 {chain_count} 条长度为 {chain_len} 的链")
    print(f"连通分量数: {uf.get_component_count()}")
    
    # 测试每条链内的连通性
    for chain_id in range(chain_count):
        start = chain_id * chain_len
        assert uf.is_connected(start, start + chain_len - 1), f"链 {chain_id} 内应该连通"
    
    # 测试不同链之间的非连通性
    assert not uf.is_connected(0, chain_len), f"不同链之间不应该连通"
    print(f"✓ 所有连通性检查通过")
    print()


def test_star_graph():
    """测试星形图（一个中心连接大量节点）"""
    print("=" * 50)
    print("测试 3: 星形图（中心连接 1999 个节点）")
    print("=" * 50)
    
    n = 2000
    uf = UnionFind(n)
    
    center = 0
    # 将所有其他节点连接到中心
    for i in range(1, n):
        uf.union(center, i)
    
    print(f"中心节点连接了 {n-1} 个其他节点")
    
    # 任意两个节点都应该连通
    test_pairs = [(0, 100), (500, 1000), (1500, 1999), (100, 1500)]
    for a, b in test_pairs:
        assert uf.is_connected(a, b), f"{a} 和 {b} 应该连通"
    
    print(f"✓ 所有节点连通，分量数: {uf.get_component_count()}")
    print()


def test_binary_tree():
    """测试二叉树结构"""
    print("=" * 50)
    print("测试 4: 二叉树结构（完全二叉树，11 层 ~2000 节点）")
    print("=" * 50)
    
    n = 2047  # 2^11 - 1 的完全二叉树
    uf = UnionFind(n)
    
    # 构建完全二叉树连接
    for i in range(n // 2):
        left_child = 2 * i + 1
        right_child = 2 * i + 2
        if left_child < n:
            uf.union(i, left_child)
        if right_child < n:
            uf.union(i, right_child)
    
    print(f"构建了包含 {n} 个节点的完全二叉树")
    
    # 所有节点应该连通
    assert uf.is_connected(0, n - 1), "根和叶应该连通"
    assert uf.get_component_count() == 1, "应该只有 1 个分量"
    print(f"✓ 树连通，分量数: {uf.get_component_count()}")
    print()


def test_random_graph():
    """测试随机图"""
    print("=" * 50)
    print("测试 5: 随机图（2000 个节点，~3000 条边）")
    print("=" * 50)
    
    import random
    random.seed(42)
    
    n = 2000
    uf = UnionFind(n)
    
    # 添加随机边
    edges = set()
    while len(edges) < 3000:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (min(u, v), max(u, v)) not in edges:
            edges.add((min(u, v), max(u, v)))
            uf.union(u, v)
    
    print(f"添加了 {len(edges)} 条随机边")
    print(f"形成了 {uf.get_component_count()} 个连通分量")
    print(f"✓ 随机图处理完成")
    print()


if __name__ == "__main__":
    test_large_chain()
    test_multiple_chains()
    test_star_graph()
    test_binary_tree()
    test_random_graph()
    
    print("=" * 50)
    print("所有大规模数据测试通过！")
    print("✓ UnionFind 迭代实现可安全处理超过 1000 个节点")
    print("=" * 50)
