
from collections import deque

class SPFA:
    def __init__(self, start_node, edges, max_node_num):
        self.edges = edges[::]
        self.start_node = start_node
        self.max_node_num = max_node_num
        self.link = {}
        for a, b, w, idx in edges:
            if a not in self.link:
                self.link[a] = []
            self.link[a].append((b, w, idx))

    def getMinPathLen(self, pre, f):
        return self.getInfo(pre, f, min_path=True)

    def getMaxPathLen(self, pre, f):
        return self.getInfo(pre, f, min_path=False)

    def getInfo(self, pre, f, min_path = True):
        link = self.link
        dis = [0x7fffffff] * (self.max_node_num+1) if min_path else [-0x7fffffff] * (self.max_node_num+1)
        dis[self.start_node] = 0

        updated_nodes = deque()
        updated_nodes.append(self.start_node)
        in_que = [0] * (self.max_node_num + 1)
        in_que[self.start_node] = 1

        for _ in range(self.max_node_num-1):
            update_flag = False
            node_num = len(updated_nodes)
            for _ in range(node_num):
                a = updated_nodes.popleft()
                in_que[a] = 0
                if a not in link:
                    continue

                for b, w, edge_idx in link[a]:
                    if f[edge_idx] == 0:
                        continue

                    if dis[a] == 0x7fffffff:
                        if w == -0x7fffffff:
                            new_dis = 0
                        else:
                            new_dis = 0x7fffffff

                    elif dis[a] == -0x7fffffff:
                        if w == 0x7fffffff:
                            new_dis = 0
                        else:
                            new_dis = -0x7fffffff
                    else:
                        new_dis = dis[a] + w

                    if (min_path == True and new_dis < dis[b]) or (min_path == False and new_dis > dis[b]):
                        dis[b] = new_dis
                        pre[b] = (a, edge_idx)
                        update_flag = True

                        if in_que[b] == 0:
                            in_que[b] = 1
                            updated_nodes.append(b)

            if not update_flag:
                break

        return None

class FordFulkerson:
    def __init__(self, edges, source_node, end_node, max_node_num, max_edge_num):
        self.edges = edges[::]
        self.source_node = source_node
        self.end_node = end_node
        self.max_edge_num = max_edge_num
        self.max_node_num = max_node_num

    def getCostFlow(self, min_cost = True):
        e = [-1] * (self.max_edge_num * 2 + 1)
        f = [-1] * (self.max_edge_num * 2 + 1)
        c = [-1] * (self.max_edge_num * 2 + 1)
        ne = [-1] * (self.max_edge_num * 2 + 1)
        h = [-1] * (self.max_node_num + 1)
        orig_flow = [0] * (self.max_edge_num + 1)

        idx = 0
        for a, b, w, cost in self.edges:
            e[idx], f[idx], c[idx], ne[idx], h[a] = b, w, cost, h[a], idx
            idx += 1
            e[idx], f[idx], c[idx], ne[idx], h[b] = a, 0, -cost, h[b], idx
            idx += 1

        max_flow_val, cost_val = 0, 0
        e1 = [(a, b, c, idx * 2) for idx, (a, b, _, c) in enumerate(self.edges)]
        e2 = [(b, a, -c, idx * 2 + 1) for idx, (a, b, _, c) in enumerate(self.edges)]
        e = e1 + e2
        algo = SPFA(self.source_node, e, self.max_node_num)

        while True:
            pre = [(None, None)] * (self.max_node_num + 1)
            if min_cost:
                algo.getMinPathLen(pre, f)
            else:
                algo.getMaxPathLen(pre, f)

            if pre[self.end_node][0] is None:
                break

            min_w = 0x7fffffff
            path_len = 0
            cur, edge_idx, next = self.end_node, 0, None
            while cur is not None:
                if next:
                    min_w = min(min_w, f[edge_idx])
                    path_len += c[edge_idx]
                cur, edge_idx, next = pre[cur][0], pre[cur][1], cur

            max_flow_val += min_w
            cost_val += path_len * min_w

            cur, edge_idx, next = self.end_node, 0, None
            while cur is not None:
                if next:
                    f[edge_idx], f[edge_idx ^ 1] = f[edge_idx] - min_w, f[edge_idx ^ 1] + min_w

                    if idx & 1:
                        orig_flow[edge_idx >> 1] -= min_w
                    else:
                        orig_flow[edge_idx >> 1] += min_w

                cur, edge_idx, next = pre[cur][0], pre[cur][1], cur

        return max_flow_val, cost_val, [(self.edges[i][0], self.edges[i][1], orig_flow[i], self.edges[i][2], self.edges[i][3]) for i in range(len(self.edges))]