class UnionFind:
    def __init__(self, n: int):
        self.parent = [x for x in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n
        self.setCount = n
    
    def Find(self, x: int):
        if self.parent[x] != x:
            self.parent[x] = self.Find(self.parent[x])
        return self.parent[x]
    
    def Union(self, x: int, y: int):
        root_x = self.Find(x)
        root_y = self.Find(y)
        if root_x == root_y:
            return False
        if self.size[root_x] > self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_x] = root_y
        self.size[root_y] += self.size[root_x]
        self.setCount -=1
        return True

    def connected(self, x: int, y: int):
        return self.Find(x) == self.Find(y)

def solve():
    n = int(input())
    uf = UnionFind(n + 10)
    sx, sy, tx, ty = map(int, input().split())

    circles = []
    for _ in range(n):
        x, y, r = map(int, input().split())
        circles.append((x, y, r))
    
    for i in range(n):
        for j in range(i + 1, n):
            if uf.connected(i, j):
                continue
            else:
                if (circles[i][2] - circles[j][2]) ** 2 <= (circles[i][0] - circles[j][0]) ** 2 + (circles[i][1] - circles[j][1]) ** 2 and (circles[i][0] - circles[j][0]) ** 2 + (circles[i][1] - circles[j][1]) ** 2 <= (circles[i][2] + circles[j][2]) ** 2:
                    uf.Union(i, j)
    
    s, t = -1, -1
    for i in range(n):
        x, y, r = circles[i]
        if (x - sx) ** 2 + (y - sy) ** 2 == r ** 2:
            s = i
        if (x - tx) ** 2 + (y - ty) ** 2 == r ** 2:
            t = i
    
    print('Yes' if uf.connected(s, t) else 'No')
solve()