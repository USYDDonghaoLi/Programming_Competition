#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
# 
# @param a int整型一维数组 
# @param x int整型 
# @return int整型
#
from bisect import *
from typing import *

class Solution:
    def getSubarrayNum(self , a: List[int], x: int) -> int:
        # write code here
        two = [0]
        five = [0]
        zero = [0]
        
        for num in a:
            tmp = 0
            while num % 2 == 0:
                num //= 2
                tmp += 1
            two.append(two[-1] + tmp)
            
            tmp = 0
            while num % 5 == 0:
                num //= 5
                tmp += 1
            five.append(five[-1] + tmp)
            
#             zero.append(min(two[-1], five[-1]))
        
        mod = 10 ** 9 + 7
        res = 0
        for a, b in zip(two, five):
            res += min(bisect_right(two, a - x), bisect_right(five, b - x))
            res %= mod
        
#         print('zero', zero)
        return res