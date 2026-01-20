from collections import defaultdict

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

class TarjanSCC:

    def __init__(self, n: int) -> None:
        self.adj = defaultdict(list)
        self.n = n
        self.dfn = [0 for _ in range(self.n + 1)]
        self.low = [0 for _ in range(self.n + 1)]
        self.dfncnt = 0
        self.s = [0 for _ in range(self.n + 1)]
        self.in_stack = [0 for _ in range(self.n + 1)]
        self.tp = 0
        self.scc = [0 for _ in range(self.n + 1)]
        self.sc = 0
        self.sz = [0 for _ in range(self.n + 1)]
        self.SCC = []
    
    def add(self, u: int, v: int):
        self.adj[u].append(v)
    
    @bootstrap
    def process(self, node: int):
        self.dfncnt += 1
        self.tp += 1

        self.low[node] = self.dfn[node] = self.dfncnt
        self.s[self.tp] = node
        self.in_stack[node] = 1

        for o in self.adj[node]:
            if not self.dfn[o]:
                yield self.process(o)
                self.low[node] = min(self.low[node], self.low[o])
            elif self.in_stack[o]:
                self.low[node] = min(self.low[node], self.dfn[o])

        if self.dfn[node] == self.low[node]:
            points = set()
            self.sc += 1
            while self.s[self.tp] != node:
                self.scc[self.s[self.tp]] = self.sc
                points.add(self.s[self.tp])
                self.sz[self.sc] += 1
                self.in_stack[self.s[self.tp]] = 0
                self.tp -= 1
            self.scc[self.s[self.tp]] = self.sc
            points.add(self.s[self.tp])
            self.sz[self.sc] += 1
            self.in_stack[self.s[self.tp]] = 0
            self.tp -= 1
            self.SCC.append(points)
        yield None
    
    def go(self):
        for i in range(1, self.n + 1):
            if not self.dfn[i]:
                self.process(i)