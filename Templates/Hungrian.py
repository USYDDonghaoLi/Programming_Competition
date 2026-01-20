'''
二分图最大匹配，最小点覆盖
'''

class Hungarian:

    def __init__(self, m, n) -> None:
        '''
        m: 左侧点数量
        n: 右侧点数量
        Map: 邻接矩阵
        p: 记录当前右侧元素对应的左侧元素
        vis: 记录右侧元素是否被访问过
        下标从1开始
        '''
        self.m, self.n = m, n
        #TODO: 数据范围大就换邻接表
        self.Map = [[0 for _ in range(self.n + 1)] for _ in range(self.m + 1)]
        self.p = [0 for _ in range(self.n + 1)]
        self.vis = [False for _ in range(self.n + 1)]
    
    def add(self, row, col):
        self.Map[row][col] = 1
    
    def match(self, i):
        for j in range(1, self.n + 1):
            if self.Map[i][j] and not self.vis[j]:
                self.vis[j] = True
                if (not self.p[j]) or self.match(self.p[j]):
                    self.p[j] = i
                    return True
        return False
    
    def go(self):
        cnt = 0
        for i in range(1, self.m + 1):
            for j in range(1, self.n + 1):
                self.vis[j] = False
            if self.match(i):
                cnt += 1
        return cnt