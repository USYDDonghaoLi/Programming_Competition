#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
# 
# @param n int整型 
# @param m int整型 
# @param x int整型 
# @return int整型
#
mod = 10 ** 9 + 7
# def mul(a, b):
# #     print(a, b)
#     res = [[0 for _ in range(2)] for _ in range(2)]
#     for i in range(2):
#         for j in range(2):
#             for k in range(2):
#                 res[i][j] += a[i][k] * b[k][j] % mod
                
#             res[i][j] %= mod
#     return res

# def qp(a, p):
#     res = [[0 for _ in range(2)] for _ in range(2)]
#     for i in range(2):
#         res[i][i] = 1
        
#     while p:
#         if p & 1:
#             res = mul(res, a)
#         a = mul(a, a)
#         p >>= 1
#     return res

class Solution:
    def numsOfGoodMatrix(self , n: int, m: int, x: int) -> int:
        # write code here
        return (pow(x, n + m - 1, mod) * pow(x // 2, (n - 1) * (m - 1), mod) % mod)