"""
Tarjan 算法测试套件 - 验证桥、割点、SCC 的正确性
"""

from Tarjan_Bridge import TarjanBridge
from Tarjan_Cut import TarjanCut
from Tarjan_SCC import TarjanSCC


def test_tarjan_bridge():
    """测试桥算法"""
    print("=" * 50)
    print("测试 TarjanBridge (桥)")
    print("=" * 50)
    
    # 创建一个简单的图：0-1-2-3（链）
    # 在这个图中，所有边都是桥
    bridge = TarjanBridge(4)
    bridge.add_edge(0, 1)
    bridge.add_edge(1, 2)
    bridge.add_edge(2, 3)
    
    bridges = bridge.find_bridges()
    print(f"✓ 链图中找到的桥: {bridges}")
    assert len(bridges) == 3, "链图中应该有 3 条桥"
    
    print()


def test_tarjan_cut():
    """测试割点算法"""
    print("=" * 50)
    print("测试 TarjanCut (割点)")
    print("=" * 50)
    
    # 创建一个有多个割点的图
    # 0 - 1 - 2
    #         |
    #         3
    # 其中 1 和 2 是割点
    cut = TarjanCut(4)
    cut.add_edge(0, 1)
    cut.add_edge(1, 2)
    cut.add_edge(2, 3)
    
    articulations = cut.find_articulation_points()
    print(f"✓ 找到割点: {articulations}")
    
    # 分析：
    # - 删除 0：其他节点仍连通，所以 0 不是割点
    # - 删除 1：{0} 和 {2,3} 分离，所以 1 是割点
    # - 删除 2：{0,1} 和 {3} 分离，所以 2 是割点
    # - 删除 3：其他节点仍连通，所以 3 不是割点
    assert 1 in articulations, "节点 1 应该是割点"
    assert 2 in articulations, "节点 2 应该是割点"
    
    print()


def test_tarjan_scc():
    """测试强连通分量算法"""
    print("=" * 50)
    print("测试 TarjanSCC (强连通分量)")
    print("=" * 50)
    
    # 创建一个有向图，包含多个 SCC
    # 0 -> 1 -> 2
    # ^         |
    # |_________|
    # 
    # 3 -> 4
    # ^    |
    # |____|
    scc = TarjanSCC(5)
    scc.add_edge(0, 1)
    scc.add_edge(1, 2)
    scc.add_edge(2, 0)
    scc.add_edge(3, 4)
    scc.add_edge(4, 3)
    
    scc_count, sccs, scc_id = scc.find_scc()
    print(f"✓ SCC 数量: {scc_count}")
    print(f"✓ SCC 列表: {sccs}")
    
    # 0, 1, 2 应该在同一个 SCC
    assert scc_id[0] == scc_id[1], "节点 0 和 1 应该在同一个 SCC"
    assert scc_id[1] == scc_id[2], "节点 1 和 2 应该在同一个 SCC"
    
    # 3, 4 应该在同一个 SCC（不同于 0,1,2）
    assert scc_id[3] == scc_id[4], "节点 3 和 4 应该在同一个 SCC"
    assert scc_id[0] != scc_id[3], "SCC {0,1,2} 和 SCC {3,4} 应该不同"
    
    print()


def test_complex_bridge():
    """复杂图的桥测试"""
    print("=" * 50)
    print("复杂图桥测试")
    print("=" * 50)
    
    # 两个完全子图通过一条边连接
    #   0-1      3-4
    #   | X  +   | X
    #   2-/   2-5
    bridge = TarjanBridge(6)
    
    # 第一个完全子图 (0,1,2)
    bridge.add_edge(0, 1)
    bridge.add_edge(1, 2)
    bridge.add_edge(2, 0)
    
    # 连接边
    bridge.add_edge(2, 3)
    
    # 第二个完全子图 (3,4,5)
    bridge.add_edge(3, 4)
    bridge.add_edge(4, 5)
    bridge.add_edge(5, 3)
    
    bridges = bridge.find_bridges()
    print(f"✓ 找到桥: {bridges}")
    assert len(bridges) == 1, "应该只有一条桥"
    assert (2, 3) in bridges or (3, 2) in bridges, "桥应该是 (2,3)"
    
    print()


if __name__ == "__main__":
    test_tarjan_bridge()
    test_tarjan_cut()
    test_tarjan_scc()
    test_complex_bridge()
    
    print("=" * 50)
    print("所有 Tarjan 测试通过！✓")
    print("=" * 50)
