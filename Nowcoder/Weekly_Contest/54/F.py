'''
Hala Madrid!
https://github.com/USYDDonghaoLi/Programming_Competition
'''
import sys
import os
from io import BytesIO, IOBase
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

def I(): return input()
def II(): return int(input())
def MI(): return map(int, input().split())
def LII(): return list(map(int, input().split()))

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

# sys.setrecursionlimit(2000000)

'''
【圆方树常见考点 + 解题思路总结】

一、基本结构
- 圆点：原图顶点（每个点一个）
- 方点：每个点双连通分量（BCC）一个
- 建法：Tarjan求点双 → 每个BCC建方点，BCC内所有圆点连向该方点
- 结果：一棵树（原图连通时），节点数 ≤ 2N

二、核心性质（必记）
1. 原图简单路径 ↔ 圆方树上路径
2. 点v在某条S-T简单路径上 
   ⟺ v属于S到T路径上某个方点对应的BCC
3. 割点可属于多个BCC（成员列表有重复，用set去重）
4. 桥的BCC只含两个点
5. 路径上的方点 = 路径经过的所有BCC

三、常见考点与解题思路

【考点1】统计所有S-T简单路径并集的点权之和
思路：
1. 建圆方树
2. 求S到T的树上路径
3. 收集路径上所有方点包含的圆点（取并集）
4. 对并集点权求和
（本题就是这个模型）

【考点2】询问路径上经过了多少个环
思路：
- 建圆方树后，S到T路径上方点的数量即为经过的环数
- （方点对应BCC，有环的BCC才是真正的环）

【考点3】仙人掌图上的路径问题（最短路/最远点/直径/路径最值）
思路：
1. 对仙人掌建圆方树（只对环建方点，桥直接连圆点）
2. 方点权值设为环长或环上信息
3. 转化为普通树上问题（树DP / LCA / 树链剖分）

【考点4】强制经过某些关键点/边的路径问题
思路：
- 把关键点/边对应的圆点或方点强制放在路径上
- 利用树上路径必须经过某点的性质进行约束或计数

【考点5】点双连通相关的连通性、割点处理
思路：
- 圆方树天然分离了割点与BCC
- 删点、缩点、连通块计数等问题可直接在树上操作

【考点6】把一般带环图转化为树
思路：
- 任何需要“消除环的影响、保留简单路径结构”的问题
- 优先考虑建圆方树，再上树DP、虚树、LCA等工具

四、实现提醒
- 必须用【点双】，不是边双
- Tarjan注意根节点、孤立点、桥的处理
- 收集答案时一定取路径上方点的成员并集（不是只取路径上的圆点）
- 网格图注意Python递归深度问题
'''

def build_round_square_tree(n, g, start):
    """
    返回:
        tree: 圆方树邻接表
        members: list，members[sq - n] = 该方点对应的 BCC 圆点列表
        dfn: 时间戳（用于判断可达）
        sq_cnt: 方点数量
    圆点：每个原图顶点只对应一个圆点（编号唯一）。
    方点：每个点双连通分量（BCC）对应一个方点，这个方点会连接（包含）该 BCC 里的所有顶点。

    一个顶点如果是割点，它会同时属于多个 BCC，因此会出现在多个方点的成员列表里。
    """
    dfn = [0] * n
    low = [0] * n
    timer = 0
    stk = []
    bccs = []

    @bootstrap
    def dfs(u, fa):
        nonlocal timer
        timer += 1
        dfn[u] = low[u] = timer
        stk.append(u)
        for v in g[u]:
            if v == fa:
                continue
            if dfn[v] == 0:
                yield dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] >= dfn[u]:
                    comp = []
                    while True:
                        x = stk.pop()
                        comp.append(x)
                        if x == v:
                            break
                    comp.append(u)
                    bccs.append(comp)
            elif dfn[v] < dfn[u]:
                low[u] = min(low[u], dfn[v])
        yield

    dfs(start, -1)

    if stk:
        if not bccs:
            bccs.append(list(stk))
        stk.clear()

    total = n + len(bccs) + 5
    tree = [[] for _ in range(total)]
    members = [None] * len(bccs)
    sq = n
    for idx, comp in enumerate(bccs):
        members[idx] = comp
        for x in comp:
            tree[x].append(sq)
            tree[sq].append(x)
        sq += 1

    return tree, members, dfn, len(bccs)


def solve():
    n, m = MI()
    a = [LII() for _ in range(n)]
    N = n * m
    val = [0] * N
    g = [[] for _ in range(N)]

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(m):
            u = i * m + j
            if a[i][j] == -1:
                continue
            val[u] = a[i][j]
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m and a[ni][nj] != -1:
                    v = ni * m + nj
                    if u < v:
                        g[u].append(v)
                        g[v].append(u)

    S, T = 0, N - 1
    tree, members, dfn, sq_cnt = build_round_square_tree(N, g, S)

    if dfn[T] == 0:
        print(0)
        return

    from collections import deque
    parent = [-1] * (N + sq_cnt + 5)
    vis = [False] * (N + sq_cnt + 5)
    q = deque([S])
    vis[S] = True
    parent[S] = S

    while q:
        u = q.popleft()
        if u == T:
            break
        for v in tree[u]:
            if not vis[v]:
                vis[v] = True
                parent[v] = u
                q.append(v)

    if not vis[T]:
        print(0)
        return

    # 收集路径上所有方点包含的圆点
    rounds = set()
    cur = T
    while True:
        if cur >= N:                    # 方点
            idx = cur - N
            for x in members[idx]:
                rounds.add(x)
        if cur == S:
            break
        cur = parent[cur]

    ans = sum(val[x] for x in rounds)
    print(ans)


solve()