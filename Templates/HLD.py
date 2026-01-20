from types import GeneratorType

def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc

class HLD:
    
    def __init__(self, n) -> None:
        '''
        下标从1开始
        G: 邻接表
        DFN: 每个节点dfs的时间戳
        NFD: 每个时间戳对应的节点
        DEP: 每个结点的深度
        F: 每个结点的父节点
        SIZ: 每个节点为根的子树大小
        HC: 每个结点的重儿子
        TOP: 每个节点所在链子的顶点
        ID: 时间戳
        '''
        self.n = n
        self.G = [[] for _ in range(self.n)]
        self.DFN = [0 for _ in range(self.n)]
        self.NFD = [0 for _ in range(self.n)]
        self.DEP = [0 for _ in range(self.n)]
        self.F = [0 for _ in range(self.n)]
        self.SIZ = [0 for _ in range(self.n)]
        self.HC = [0 for _ in range(self.n)]
        self.TOP = [0 for _ in range(self.n)]
        self.ID = 0
    
    def addEdge(self, u, v):
        self.G[u].append(v)
        self.G[v].append(u)
    
    @bootstrap
    def dfs1(self, u):
        self.SIZ[u] = 1
        for v in self.G[u]:
            if v != self.F[u]:
                self.F[v] = u
                self.DEP[v] = self.DEP[u] + 1
                yield self.dfs1(v)
                self.SIZ[u] += self.SIZ[v]
                if self.SIZ[v] > self.SIZ[self.HC[u]]:
                    self.HC[u] = v
        yield None
    
    @bootstrap
    def dfs2(self, u):
        self.ID += 1
        self.DFN[u] = self.ID
        self.NFD[self.ID] = u
        if self.HC[u]:
            self.TOP[self.HC[u]] = self.TOP[u]
            yield self.dfs2(self.HC[u])
            for v in self.G[u]:
                if v != self.HC[u] and v != self.F[u]:
                    self.TOP[v] = v
                    yield self.dfs2(v)
        yield None
    
    def lca(self, u, v):
        while self.TOP[u] != self.TOP[v]:
            if self.DEP[self.TOP[u]] < self.DEP[self.TOP[v]]:
                u, v = v, u
            u = self.F[self.TOP[u]]
        if self.DEP[u] > self.DEP[v]:
            u, v = v, u
        return u
    
    def dis(self, u, v):
        return self.DEP[u] + self.DEP[v] - 2 * self.DEP[self.lca(u, v)]
    
    def fun(self, root):
        self.DEP[root] = 1
        self.dfs1(root)
        self.TOP[root] = root
        self.dfs2(root)
    
    def get_path(self, u, v):
        v1, v2 = [], []
        while self.TOP[u] != self.TOP[v]:
            if self.DEP[self.TOP[u]] > self.DEP[self.TOP[v]]:
                v1.append((self.DFN[u], self.DFN[self.TOP[u]]))
                u = self.F[self.TOP[u]]
            else:
                v2.append((self.DFN[self.TOP[v]], self.DFN[v]))
                v = self.F[self.TOP[v]]
        v1.append((self.DFN[u], self.DFN[v]))
        v1.extend(reversed(v2))
        return v1