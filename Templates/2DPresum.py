"""
2D 前缀和

二维数组的前缀和（累积和）算法。

原理：
- presum[i][j] = sum of A[0..i-1][0..j-1]
- 矩形区域和 = presum[x2][y2] - presum[x1][y2] - presum[x2][y1] + presum[x1][y1]

复杂度：
- 预处理：O(n*m)
- 单次查询：O(1)

应用：
- 二维数组区间和查询
- 图像处理中的积分图
- 动态规划加速
"""

class Presum2D:
    
    def __init__(self, grid) -> None:
        self.grid = grid
        self.n, self.m = len(grid), len(grid[0])
        self.ps = [[0 for _ in range(self.m + 1)] for _ in range(self.n + 1)]
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                self.ps[i][j] = self.ps[i - 1][j] + self.ps[i][j - 1] - self.ps[i - 1][j - 1] + grid[i - 1][j - 1]
    
    def query(self, x1, y1, x2, y2):
        x2 += 1
        y2 += 1
        return self.ps[x2][y2] - self.ps[x1][y2] - self.ps[x2][y1] + self.ps[x1][y1]