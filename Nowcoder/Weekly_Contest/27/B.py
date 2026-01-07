class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
# 
# @param tree TreeNode类 
# @return int整型
#
import sys
sys.setrecursionlimit(100010)

from typing import *

class Solution:
    def getTreeSum(self , tree: TreeNode) -> int:
        mod = 10 ** 9 + 7
        
        def dfs(node):
            if node.left != None:
                L = dfs(node.left)
                R = dfs(node.right)
                return max(L, R) * 2 + 1
            else:
                return 1
        
        return dfs(tree) % mod
        # write code here