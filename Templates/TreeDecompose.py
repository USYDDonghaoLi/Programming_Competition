from collections import *

'''
手写栈防止recursion limit
注意要用yield 不要用return
函数结尾要写yield None
'''
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

class TreeDecompose:

    def __init__(self, n: int) -> None:
        '''
        fa: 节点在树上的父亲
        dep: 节点在树上的深度
        siz: 节点的子树的节点个数
        son: 节点的重儿子
        top: 节点所在重链的顶部节点
        dfn: 节点的DFS序, 也是其在线段树上的编号
        rnk: DFS序所对应的节点编号, rnk(dfn(x)) = x
        '''
        self.n = n
        self.cnt = 0
        self.adj = defaultdict(list)
        self.fa = [0 for _ in range(self.n + 1)]
        self.dep = [0 for _ in range(self.n + 1)]
        self.siz = [0 for _ in range(self.n + 1)]
        self.son = [0 for _ in range(self.n + 1)]
        self.top = [0 for _ in range(self.n + 1)]
        self.dfn = [0 for _ in range(self.n + 1)]
        self.rnk = [0 for _ in range(self.n + 1)]
        pass
    
    def add(self, u: int, v: int) -> None:
        self.adj[u].append(v)
        self.adj[v].append(u)
    
    '''
    第一遍dfs, 求出fa(x), dep(x), siz(x), son(x)
    '''
    @bootstrap
    def dfs1(self, o: int):
        self.son[o] = -1
        self.siz[o] = 1

        for j in self.adj[o]:
            if not self.dep[j]:
                self.dep[j] = self.dep[o] + 1
                self.fa[j] = o
                yield self.dfs1(j)
                self.siz[o] += self.siz[j]

                if (self.son[o] == -1 or self.siz[j] > self.siz[self.son[o]]):
                    self.son[o] = j

        yield None
    
    '''
    第二遍DFS, 求出top(x), dfn(x), rnk(x)
    '''
    @bootstrap
    def dfs2(self, o: int, t: int):
        self.top[o] = t
        self.cnt += 1
        self.dfn[o] = self.cnt
        self.rnk[self.cnt] = o

        if (self.son[o] == -1):
            return
        
        '''
        优先对重儿子进行DFS, 保证一条重链上的点DFS序连续。
        '''
        yield self.dfs2(self.son[o], t)
        
        for j in self.adj[o]:
            if (j != self.son[o] and j != self.fa[o]):
                yield self.dfs2(j, j)
        
    def go(self):
        self.dfs1(1)
        self.dfs2(1, 1)