class AuxiliaryTree:
    def __init__(self, n, edge, root=0):
        self.n = n
        self.edge = edge
        '''
        eular: dfs时节点的访问顺序
        first: 每个节点在欧拉序列中第一次出现的位置
        '''
        self.eular = [-1] * (2 * n - 1)
        self.first = [-1] * n
        self.depth = [-1] * n
        self.lgs = [0] * (2 * n)
        for i in range(2, 2 * n):
            self.lgs[i] = self.lgs[i >> 1] + 1
        self.st = []
        self.G = [[] for i in range(n)]

        self.dfs(root)
        self.construct_sparse_table()

    def dfs(self, root):
        stc = [root]
        self.depth[root] = 0
        num = 0
        while stc:
            v = stc.pop()
            if v >= 0:
                self.eular[num] = v
                self.first[v] = num
                num += 1
                for u in self.edge[v][::-1]:
                    if self.depth[u] == -1:
                        self.depth[u] = self.depth[v] + 1
                        stc.append(~v)
                        stc.append(u)
            else:
                self.eular[num] = ~v
                num += 1

    def construct_sparse_table(self):
        self.st.append(self.eular)
        sz = 1
        while 2 * sz <= 2 * self.n - 1:
            prev = self.st[-1]
            nxt = [0] * (2 * self.n - 2 * sz)
            for j in range(2 * self.n - 2 * sz):
                v = prev[j]
                u = prev[j + sz]
                if self.depth[v] <= self.depth[u]:
                    nxt[j] = v
                else:
                    nxt[j] = u
            self.st.append(nxt)
            sz *= 2

    def lca(self, u, v):
        x = self.first[u]
        y = self.first[v]
        if x > y : x , y = y , x
        d = self.lgs[y - x + 1]
        return (
            self.st[d][x]
            if self.depth[self.st[d][x]] <= self.depth[self.st[d][y - (1 << d) + 1]]
            else self.st[d][y - (1 << d) + 1]
        )

    def query(self, vs):
        """
        vs: 虚树中包含的顶点集合
        self.G: 虚树
        return: 虚树的根 (sz中所有顶点的lca)
        Time Complexity: O(k * logn)
        """

        k = len(vs)
        if k == 0:
            return -1
        vs.sort(key=self.first.__getitem__)
        stc = [vs[0]]
        self.G[vs[0]] = []

        for i in range(k - 1):
            w = self.lca(vs[i], vs[i + 1])
            if w != vs[i]:
                last = stc.pop()
                while stc and self.depth[w] < self.depth[stc[-1]]:
                    self.G[stc[-1]].append(last)
                    last = stc.pop()

                if not stc or stc[-1] != w:
                    stc.append(w)
                    vs.append(w)
                    self.G[w] = [last]
                else:
                    self.G[w].append(last)
            stc.append(vs[i + 1])
            self.G[vs[i + 1]] = []

        for i in range(len(stc) - 1):
            self.G[stc[i]].append(stc[i + 1])

        return stc[0]