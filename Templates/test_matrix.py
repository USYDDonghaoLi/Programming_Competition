"""
Matrix.py 测试文件
对矩阵类的所有函数进行功能测试
"""

import sys
sys.path.insert(0, '/Users/wangzhinuo/Desktop/Ldh/Programming_Competition/Templates')

from Matrix import Matrix


def test_init_and_build():
    """测试 __init__ 和 build 方法"""
    print("=" * 50)
    print("测试 1: __init__ 和 build")
    print("=" * 50)
    
    # 创建 2x3 矩阵
    m = Matrix(2, 3)
    print(f"创建 2x3 矩阵 (无mod):")
    print(m)
    print()
    
    # 使用 build 初始化
    m.build([[1, 2, 3], [4, 5, 6]])
    print("使用 build 初始化 [[1,2,3], [4,5,6]]:")
    print(m)
    print()
    
    # 创建带 mod 的矩阵
    m_mod = Matrix(2, 2, mod=7)
    m_mod.build([[1, 2], [3, 4]])
    print("创建 2x2 矩阵 (mod=7):")
    print(m_mod)
    print()


def test_getitem_setitem():
    """测试 __getitem__ 和 __setitem__"""
    print("=" * 50)
    print("测试 2: __getitem__ 和 __setitem__")
    print("=" * 50)
    
    m = Matrix(2, 2)
    m[0, 0] = 1
    m[0, 1] = 2
    m[1, 0] = 3
    m[1, 1] = 4
    
    print("设置元素后的矩阵:")
    print(m)
    print(f"m[0,0] = {m[0, 0]}, m[1,1] = {m[1, 1]}")
    print()


def test_copy_and_transpose():
    """测试 copy 和 transpose"""
    print("=" * 50)
    print("测试 3: copy 和 transpose")
    print("=" * 50)
    
    m = Matrix(2, 3)
    m.build([[1, 2, 3], [4, 5, 6]])
    
    print("原矩阵:")
    print(m)
    print()
    
    # 测试 copy
    m_copy = m.copy()
    m_copy[0, 0] = 99
    print("深拷贝后修改副本的 [0,0] = 99:")
    print("原矩阵 [0,0]:", m[0, 0])
    print("副本 [0,0]:", m_copy[0, 0])
    print()
    
    # 测试 transpose
    m_t = m.transpose()
    print("转置矩阵 (2x3 -> 3x2):")
    print(m_t)
    print()


def test_iter():
    """测试迭代器"""
    print("=" * 50)
    print("测试 4: __iter__ (迭代)")
    print("=" * 50)
    
    m = Matrix(2, 2)
    m.build([[1, 2], [3, 4]])
    
    print("矩阵:")
    print(m)
    print("遍历所有元素:", end=" ")
    print([x for x in m])
    print()


def test_build_identity():
    """测试单位矩阵构造"""
    print("=" * 50)
    print("测试 5: build_identity")
    print("=" * 50)
    
    m = Matrix(3, 3)
    m.build_identity(2)
    print("3x3 单位矩阵 (lim=2):")
    print(m)
    print()


def test_matrix_addition():
    """测试矩阵加法"""
    print("=" * 50)
    print("测试 6: 矩阵加法 (__add__)")
    print("=" * 50)
    
    # 不取模的情况
    m1 = Matrix(2, 2)
    m1.build([[1, 2], [3, 4]])
    m2 = Matrix(2, 2)
    m2.build([[5, 6], [7, 8]])
    
    print("矩阵 A:")
    print(m1)
    print("\n矩阵 B:")
    print(m2)
    
    m3 = m1 + m2
    print("\nA + B:")
    print(m3)
    print()
    
    # 取模的情况
    m4 = Matrix(2, 2, mod=5)
    m4.build([[1, 2], [3, 4]])
    m5 = Matrix(2, 2, mod=5)
    m5.build([[5, 6], [7, 8]])
    
    print("矩阵 A (mod=5):")
    print(m4)
    print("\n矩阵 B (mod=5):")
    print(m5)
    
    m6 = m4 + m5
    print("\n(A + B) mod 5:")
    print(m6)
    print()


def test_matrix_subtraction():
    """测试矩阵减法"""
    print("=" * 50)
    print("测试 7: 矩阵减法 (__sub__)")
    print("=" * 50)
    
    m1 = Matrix(2, 2)
    m1.build([[5, 6], [7, 8]])
    m2 = Matrix(2, 2)
    m2.build([[1, 2], [3, 4]])
    
    print("矩阵 A:")
    print(m1)
    print("\n矩阵 B:")
    print(m2)
    
    m3 = m1 - m2
    print("\nA - B:")
    print(m3)
    print()


def test_matrix_multiplication():
    """测试矩阵乘法"""
    print("=" * 50)
    print("测试 8: 矩阵乘法 (__mul__)")
    print("=" * 50)
    
    # 不取模的情况
    m1 = Matrix(2, 3)
    m1.build([[1, 2, 3], [4, 5, 6]])
    m2 = Matrix(3, 2)
    m2.build([[7, 8], [9, 10], [11, 12]])
    
    print("矩阵 A (2x3):")
    print(m1)
    print("\n矩阵 B (3x2):")
    print(m2)
    
    m3 = m1 * m2
    print("\nA * B (2x2):")
    print(m3)
    print("验证: [0,0] = 1*7 + 2*9 + 3*11 = 58")
    print()
    
    # 取模的情况
    m4 = Matrix(2, 2, mod=11)
    m4.build([[1, 2], [3, 4]])
    m5 = Matrix(2, 2, mod=11)
    m5.build([[5, 6], [7, 8]])
    
    print("矩阵 A (mod=11):")
    print(m4)
    print("\n矩阵 B (mod=11):")
    print(m5)
    
    m6 = m4 * m5
    print("\n(A * B) mod 11:")
    print(m6)
    print("验证: [0,0] = (1*5 + 2*7) mod 11 = 19 mod 11 = 8")
    print()


def test_matrix_power():
    """测试矩阵快速幂"""
    print("=" * 50)
    print("测试 9: 矩阵快速幂 (matrix_power)")
    print("=" * 50)
    
    # 不取模
    m = Matrix(2, 2)
    m.build([[1, 1], [1, 0]])
    
    print("矩阵 A (斐波那契矩阵):")
    print(m)
    print()
    
    m2 = m.matrix_power(2)
    print("A^2:")
    print(m2)
    print()
    
    m3 = m.matrix_power(3)
    print("A^3:")
    print(m3)
    print()
    
    # 取模
    m_mod = Matrix(2, 2, mod=1000000007)
    m_mod.build([[1, 1], [1, 0]])
    m_mod_10 = m_mod.matrix_power(10)
    print("A^10 (mod=1000000007):")
    print(m_mod_10)
    print()


def test_gauss_float():
    """测试浮点数高斯消元"""
    print("=" * 50)
    print("测试 10: 高斯消元 (浮点数)")
    print("=" * 50)
    
    # 唯一解的情况
    a1 = [
        [1.0, 2.0, 3.0],  # x + 2y = 3
        [2.0, 1.0, 3.0]   # 2x + y = 3
    ]
    result1 = Matrix.gauss_float(2, a1)
    print("方程组 1 (唯一解):")
    print("x + 2y = 3")
    print("2x + y = 3")
    print(f"结果: {result1}")
    print("验证: x=1, y=1")
    print()
    
    # 无穷多解的情况
    a2 = [
        [1.0, 2.0, 3.0],
        [2.0, 4.0, 6.0]  # 第二个方程是第一个的 2 倍
    ]
    result2 = Matrix.gauss_float(2, a2)
    print("方程组 2 (无穷多解):")
    print("x + 2y = 3")
    print("2x + 4y = 6")
    print(f"结果: {result2}")
    print()
    
    # 无解的情况
    a3 = [
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 4.0]  # 系数相同但常数项不同
    ]
    result3 = Matrix.gauss_float(2, a3)
    print("方程组 3 (无解):")
    print("x + 2y = 3")
    print("x + 2y = 4")
    print(f"结果: {result3}")
    print()


def test_gauss_jordan_mod():
    """测试高斯-约当消元（模运算）"""
    print("=" * 50)
    print("测试 11: 高斯-约当消元 (mod=7)")
    print("=" * 50)
    
    # 扩展矩阵: [A | I]
    m = Matrix(2, 4, mod=7)
    m.build([
        [1, 2, 1, 0],
        [3, 4, 0, 1]
    ])
    
    print("扩展矩阵 [A | I] (mod=7):")
    print(m)
    print()
    
    result = m.gauss_jordan_mod(2)
    print(f"是否有解: {result}")
    print("消元后的矩阵 [I | A^-1]:")
    print(m)
    print()


def test_get_inverse_mod():
    """测试矩阵逆（模运算）"""
    print("=" * 50)
    print("测试 12: 求逆矩阵 (mod=7)")
    print("=" * 50)
    
    m = Matrix(2, 2, mod=7)
    m.build([[1, 2], [3, 4]])
    
    print("原矩阵 A (mod=7):")
    print(m)
    print()
    
    try:
        m_inv = m.get_inverse_mod(2)
        print("A^-1 (mod=7):")
        print(m_inv)
        print()
        
        # 验证 A * A^-1 = I
        identity = m * m_inv
        print("验证 A * A^-1 = I (mod=7):")
        print(identity)
    except Exception as e:
        print(f"错误: {e}")
    print()


def test_determinant_float():
    """测试浮点数行列式"""
    print("=" * 50)
    print("测试 13: 行列式计算 (浮点数)")
    print("=" * 50)
    
    # 2x2 矩阵
    m1 = Matrix(2, 2)
    m1.build([[1, 2], [3, 4]])
    
    print("矩阵 A (2x2):")
    print(m1)
    det1 = m1.determinant_float()
    print(f"det(A) = {det1}")
    print("验证: 1*4 - 2*3 = -2")
    print()
    
    # 3x3 矩阵
    m2 = Matrix(3, 3)
    m2.build([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
    
    print("矩阵 B (3x3):")
    print(m2)
    det2 = m2.determinant_float()
    print(f"det(B) = {det2}")
    print()
    
    # 行列式为 0 的矩阵
    m3 = Matrix(2, 2)
    m3.build([[1, 2], [2, 4]])
    
    print("矩阵 C (行列式为 0):")
    print(m3)
    det3 = m3.determinant_float()
    print(f"det(C) = {det3}")
    print()


def test_determinant_mod():
    """测试模运算行列式（素数模）"""
    print("=" * 50)
    print("测试 14: 行列式计算 (mod=7)")
    print("=" * 50)
    
    m = Matrix(2, 2, mod=7)
    m.build([[1, 2], [3, 4]])
    
    print("矩阵 A (mod=7):")
    print(m)
    det = m.determinant_mod()
    print(f"det(A) mod 7 = {det}")
    print("验证: (1*4 - 2*3) mod 7 = -2 mod 7 = 5")
    print()


def test_determinant_general_mod():
    """测试通用模数行列式"""
    print("=" * 50)
    print("测试 15: 行列式计算 (通用 mod=10)")
    print("=" * 50)
    
    m = Matrix(2, 2, mod=10)
    m.build([[1, 2], [3, 4]])
    
    print("矩阵 A (mod=10):")
    print(m)
    det = m.determinant_general_mod()
    print(f"det(A) mod 10 = {det}")
    print()


def test_set_mod():
    """测试 set_mod 方法"""
    print("=" * 50)
    print("测试 16: set_mod 方法")
    print("=" * 50)
    
    m = Matrix(2, 2)
    print(f"初始 mod: {m.mod}")
    
    m.set_mod(7)
    print(f"设置 mod=7 后: {m.mod}")
    
    m.build([[1, 2], [3, 4]])
    m_add = m + m
    print("2A (mod=7):")
    print(m_add)
    print()


def test_comprehensive():
    """综合测试"""
    print("=" * 50)
    print("测试 17: 综合应用")
    print("=" * 50)
    
    # 计算 Fibonacci 数列
    # F(n) 可以通过矩阵 [[1,1],[1,0]]^n 的 [0,1] 位置得到
    m = Matrix(2, 2, mod=1000000007)
    m.build([[1, 1], [1, 0]])
    
    print("使用矩阵快速幂计算 Fibonacci 数列:")
    for n in [1, 2, 5, 10, 20]:
        result = m.matrix_power(n)
        fib_n = result[0, 1]
        print(f"F({n}) = {fib_n}")
    print()


if __name__ == "__main__":
    test_init_and_build()
    test_getitem_setitem()
    test_copy_and_transpose()
    test_iter()
    test_build_identity()
    test_matrix_addition()
    test_matrix_subtraction()
    test_matrix_multiplication()
    test_matrix_power()
    test_gauss_float()
    test_gauss_jordan_mod()
    test_get_inverse_mod()
    test_determinant_float()
    test_determinant_mod()
    test_determinant_general_mod()
    test_set_mod()
    test_comprehensive()
    
    print("=" * 50)
    print("所有测试完成！")
    print("=" * 50)
