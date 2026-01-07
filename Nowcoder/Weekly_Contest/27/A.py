#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
# 
# @param s string字符串 
# @return int整型
#
class Solution:
    def minCnt(self , s: str) -> int:
        return s.count('1') - 1
        # write code here