"""
其他模板的测试文件
测试：UnionFind, Prime, Fenwick Tree, KMP, Z_Algorithm
"""

import sys
sys.path.insert(0, '/Users/wangzhinuo/Desktop/Ldh/Programming_Competition/Templates')

from UnionFind import UnionFind
from Prime import Prime
import importlib.util

# 动态导入包含空格的模块
spec = importlib.util.spec_from_file_location("fenwick", "/Users/wangzhinuo/Desktop/Ldh/Programming_Competition/Templates/Fenwick Tree.py")
fenwick_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fenwick_module)
FenwickTree = fenwick_module.FenwickTree

from KMP import KMP
from Z_Algorithm import z_algorithm


def test_union_find():
    """测试并查集"""
    print("=" * 50)
    print("测试 1: UnionFind 并查集")
    print("=" * 50)
    
    uf = UnionFind(5)
    print(f"初始连通分量个数: {uf.get_component_count()}")
    
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)
    
    print(f"union(0,1), union(1,2), union(3,4) 后: {uf.get_component_count()} 个分量")
    print(f"is_connected(0, 2): {uf.is_connected(0, 2)}")
    print(f"is_connected(0, 3): {uf.is_connected(0, 3)}")
    
    print(f"元素 0 所在分量的大小: {uf.get_component_size(0)}")
    print(f"所有根节点: {uf.get_roots()}")
    print(f"所有分量: {uf.get_all_components()}")
    print()


def test_prime():
    """测试素数相关算法"""
    print("=" * 50)
    print("测试 2: Prime 素数库")
    print("=" * 50)
    
    prime = Prime(50)
    print(f"50 以内的素数: {prime.primes}")
    print()
    
    # 素因数分解
    print("素因数分解:")
    for n in [12, 24, 100]:
        factors = prime.factorize(n)
        print(f"  {n} = {' × '.join(f'{p}^{c}' if c > 1 else str(p) for p, c in factors)}")
    print()
    
    # 获取所有因子
    print("所有因子:")
    for n in [12, 24]:
        all_factors = sorted(prime.get_all_factors(n))
        print(f"  {n} 的因子: {all_factors}")
    print()
    
    # 原根
    print("原根计算 (素数 p=7):")
    g = prime.primitive_root(7)
    print(f"  7 的最小原根: {g}")
    print(f"  验证 g^k mod 7 的循环:")
    for k in range(1, 7):
        print(f"    {g}^{k} mod 7 = {pow(g, k, 7)}", end="  ")
    print()
    print()


def test_fenwick_tree():
    """测试树状数组"""
    print("=" * 50)
    print("测试 3: Fenwick Tree 树状数组")
    print("=" * 50)
    
    arr = [1, 2, 3, 4, 5]
    ft = FenwickTree(len(arr))
    ft.build(arr)
    
    print(f"数组: {arr}")
    print(f"前缀和 query(0): {ft.query(1)}")  # 1-indexed
    print(f"前缀和 query(1): {ft.query(2)}")  # 1+2 = 3
    print(f"前缀和 query(4): {ft.query(5)}")  # 1+2+3+4+5 = 15
    print()
    
    print("区间和:")
    print(f"  [0, 2] (1-indexed [1,3]): {ft.range_query(1, 3)}")  # 1+2+3 = 6
    print(f"  [1, 4] (1-indexed [2,5]): {ft.range_query(2, 5)}")  # 2+3+4+5 = 14
    print()
    
    print("单点修改:")
    ft.update(1, 5)  # arr[0] += 5, 变成 6
    print(f"  update(1, +5) 后，query(1) = {ft.query(1)}")  # 6
    print(f"  update(1, +5) 后，query(5) = {ft.query(5)}")  # 6+2+3+4+5 = 20
    print()


def test_kmp():
    """测试 KMP 字符串匹配"""
    print("=" * 50)
    print("测试 4: KMP 字符串匹配")
    print("=" * 50)
    
    text = "ababacabab"
    pattern = "abab"
    kmp = KMP(text, pattern)
    
    print(f"文本: '{text}'")
    print(f"模式: '{pattern}'")
    
    matches = kmp.search()
    print(f"匹配位置 (1-indexed): {matches}")
    print(f"实际位置 (0-indexed): {[m - 1 for m in matches]}")
    print()
    
    failure = kmp.get_failure_function()
    print(f"失败函数: {failure}")
    print()


def test_z_algorithm():
    """测试 Z 算法"""
    print("=" * 50)
    print("测试 5: Z Algorithm Z 算法")
    print("=" * 50)
    
    s = "aabaaab"
    z = z_algorithm(s)
    
    print(f"字符串: '{s}'")
    print(f"Z 数组: {z}")
    print()
    
    # 字符串匹配应用
    text = "ababacabab"
    pattern = "abab"
    combined = pattern + "$" + text
    z_match = z_algorithm(combined)
    
    print(f"字符串匹配应用:")
    print(f"  模式: '{pattern}'")
    print(f"  文本: '{text}'")
    print(f"  合并: '{combined}'")
    print(f"  Z 数组: {z_match}")
    matches = [i - len(pattern) - 1 for i in range(len(combined)) if z_match[i] == len(pattern)]
    print(f"  匹配位置 (0-indexed): {matches}")
    print()


def test_comprehensive():
    """综合测试"""
    print("=" * 50)
    print("测试 6: 综合应用")
    print("=" * 50)
    
    # 使用并查集找出图的连通分量
    print("图的连通分量检测:")
    edges = [(0, 1), (1, 2), (3, 4), (4, 5)]
    uf = UnionFind(6)
    for u, v in edges:
        uf.union(u, v)
    
    print(f"  边: {edges}")
    print(f"  连通分量数: {uf.get_component_count()}")
    print(f"  所有分量: {uf.get_all_components()}")
    print()
    
    # 用树状数组计算区间和
    print("区间统计应用:")
    nums = [1, 3, 5, 7, 9, 11]
    ft = FenwickTree(len(nums))
    ft.build(nums)
    
    print(f"  数组: {nums}")
    print(f"  sum([1, 4]): {ft.range_query(2, 5)}")  # 3+5+7+9 = 24
    print()


if __name__ == "__main__":
    test_union_find()
    test_prime()
    test_fenwick_tree()
    test_kmp()
    test_z_algorithm()
    test_comprehensive()
    
    print("=" * 50)
    print("所有测试完成！")
    print("=" * 50)
