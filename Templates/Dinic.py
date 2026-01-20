from collections import *

class DinicWithLowerBound:
    """
    使用方法:
      初始化
       mf = Dinic(n, S, T)
       ※ n为包含（虚拟）源点，汇点的点的个数
          给出S（虚拟源点）,T（虚拟汇点）的编号
 
      添加边
       仅给出S,T以及原始图的顶点间的边即可
       mf.add_link(from, to, capacity)
       mf.add_bound_link(from, to, lower_bound, capacity)
 
      求解最大流
       mf.max_flow()
    """
 
    def __init__(self, n: int, S: int, T: int):
        self.n = n
        self.S = S
        self.T = T
        self.links = [[] for _ in range(n)]
        # links[u] = [ [ v, capacity, index of rev-edge in links[v], is_original_edge ], ]
 
    def add_link(self, from_: int, to: int, capacity: int) -> None:
        fwd = [to, capacity, len(self.links[to]), True]
        bwd = [from_, 0, len(self.links[from_]), False]
        self.links[from_].append(fwd)
        self.links[to].append(bwd)
 
    def add_bounded_link(self, from_: int, to: int, lower_bound: int, capacity: int) -> None:
        assert capacity >= lower_bound
        if lower_bound > 0:
            self.add_link(self.S, to, lower_bound)
            self.add_link(from_, self.T, lower_bound)
        if capacity > lower_bound:
            self.add_link(from_, to, capacity - lower_bound)
 
    def bfs(self, s: int, t: int) -> bool:
        links = self.links
        INF = 1 << 60
        self.level = level = [INF] * self.n
        level[s] = 0
        q = deque([s])
        lim_level = 1 << 60
        while q:
            u = q.popleft()
            if level[u] >= lim_level:
                break
            nd = level[u] + 1
            for to, cap, _, _ in links[u]:
                if cap > 0 and level[to] == INF:
                    level[to] = nd
                    q.append(to)
                    if to == t:
                        lim_level = nd
        return level[t] != INF
 
    def dfs(self, s: int, t: int) -> int:
        links = self.links
        level = self.level
        progress = self.progress
        link_counts = self.link_counts
        # 逆から進めた方が速くなることが多いらしい
        stack = [t]
 
        while stack:
            u = stack[-1]
            if u == s:
                break
            for i in range(progress[u], link_counts[u]):
                progress[u] = i
                to, _, rev, _ = links[u][i]
                if level[u] <= level[to] or progress[to] >= link_counts[to]:
                    continue
                _, cap, _, _ = links[to][rev]
                if cap == 0 or progress[to] >= link_counts[to]:
                    continue
                stack.append(to)
                break
            else:
                progress[u] += 1
                stack.pop()
        else:
            return 0
 
        f = 1 << 60
        fwd_links = []
        bwd_links = []
        stack.pop()
        for u in stack:
            to, _, rev, _ = link = links[u][progress[u]]
            _, cap, _, _ = rev_link = links[to][rev]
            f = min(f, cap)
            fwd_links.append(rev_link)
            bwd_links.append(link)
 
        for link in fwd_links:
            link[1] -= f
 
        for link in bwd_links:
            link[1] += f
 
        return f
 
    def _max_flow(self, s: int, t: int) -> int:
        flow = 0
        while self.bfs(s, t):
            self.progress = [0] * self.n
            current_flow = 1  # Anything > 0 is ok
            while current_flow > 0:
                current_flow = self.dfs(s, t)
                flow += current_flow
        return flow
 
    def max_flow(self, s: int, t: int) -> int:
        self.link_counts = list(map(len, self.links))
        self._max_flow(self.S, self.T)
        self._max_flow(self.S, t)
        self._max_flow(s, self.T)
        result = self._max_flow(s, t)
        if not self.check_lower_bound():
            return -1
        return result
 
    def exists_fulfill_flow(self, s: int, t: int) -> bool:
        self.add_link(t, s, 1 << 60)
        self.link_counts = list(map(len, self.links))
        self._max_flow(self.S, self.T)
        return self.check_lower_bound()
 
    def check_lower_bound(self) -> bool:
        for _, cap, _, is_orig in self.links[self.S]:
            if is_orig and cap > 0:
                return False
        for to, _, rev, is_orig in self.links[self.T]:
            if is_orig:
                continue
            _, cap, _, _ = self.links[to][rev]
            if cap > 0:
                return False
        return True
 
    def cut_edges(self, s: int):
        """ max_flowしたあと、最小カットにおいてカットすべき辺を復元する """
        q = [s]
        reachable = [0] * self.n
        reachable[s] = 1
        while q:
            v = q.pop()
            for to, cap, _, _ in self.links[v]:
                if cap == 0 or reachable[to]:
                    continue
                reachable[to] = 1
                q.append(to)
        edges = []
        for v in range(self.n):
            if reachable[v] == 0:
                continue
            for to, cap, _, is_orig in self.links[v]:
                if is_orig and reachable[to] == 0:
                    edges.append((v, to))
        return edges