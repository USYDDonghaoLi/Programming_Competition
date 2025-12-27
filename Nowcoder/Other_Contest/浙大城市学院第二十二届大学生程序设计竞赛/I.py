import sys

MAXN = 4000010
nodes = []
node_cnt = 0
vis = [0] * MAXN
timestamp = 0

def create():
    global node_cnt
    nodes.append({'len': 0, 'link': -1, 'trans': [None] * 26, 'count': 0})
    ret = node_cnt
    node_cnt += 1
    return ret

def insert_to_sam(str_):
    terminals = []
    last = root
    for ch in str_:
        c = ord(ch) - ord('a')
        p = last
        if nodes[p]['trans'][c] is not None:
            q = nodes[p]['trans'][c]
            if nodes[q]['len'] == nodes[p]['len'] + 1:
                last = q
            else:
                clone = create()
                nodes[clone]['len'] = nodes[p]['len'] + 1
                nodes[clone]['link'] = nodes[q]['link']
                nodes[clone]['trans'] = nodes[q]['trans'][:]
                nodes[clone]['count'] = nodes[q]['count']
                nodes[q]['link'] = clone
                last = clone
                while p != -1 and nodes[p]['trans'][c] == q:
                    nodes[p]['trans'][c] = clone
                    p = nodes[p]['link']
        else:
            u = create()
            nodes[u]['len'] = nodes[p]['len'] + 1
            last = u
            pp = p
            while pp != -1 and nodes[pp]['trans'][c] is None:
                nodes[pp]['trans'][c] = u
                pp = nodes[pp]['link']
            if pp == -1:
                nodes[u]['link'] = root
            else:
                q = nodes[pp]['trans'][c]
                if nodes[pp]['len'] + 1 == nodes[q]['len']:
                    nodes[u]['link'] = q
                else:
                    clone = create()
                    nodes[clone]['len'] = nodes[pp]['len'] + 1
                    nodes[clone]['trans'] = nodes[q]['trans'][:]
                    nodes[clone]['link'] = nodes[q]['link']
                    nodes[clone]['count'] = nodes[q]['count']
                    nodes[q]['link'] = clone
                    nodes[u]['link'] = clone
                    while pp != -1 and nodes[pp]['trans'][c] == q:
                        nodes[pp]['trans'][c] = clone
                        pp = nodes[pp]['link']
        terminals.append(last)
    return terminals

data = sys.stdin.read().split()
idx = 0
init_str = data[idx]
idx += 1
q = int(data[idx])
idx += 1

S = list(init_str)
root = create()

total_versions = 0
answer = 0

terminals = insert_to_sam(S)
old_total = total_versions
total_versions += 1
new_answer = 0
timestamp += 1
for t in terminals:
    p = t
    while p != -1 and vis[p] != timestamp:
        vis[p] = timestamp
        if nodes[p]['count'] == old_total:
            llink = nodes[p]['link']
            prev_len = 0 if llink == -1 else nodes[llink]['len']
            new_answer += nodes[p]['len'] - prev_len
        nodes[p]['count'] += 1
        p = nodes[p]['link']
answer = new_answer

for _ in range(q):
    op = data[idx]
    idx += 1
    if op == 'I':
        i = int(data[idx])
        c = data[idx + 1]
        idx += 2
        S.insert(i, c)
        terminals = insert_to_sam(S)
        old_total = total_versions
        total_versions += 1
        new_answer = 0
        timestamp += 1
        for t in terminals:
            p = t
            while p != -1 and vis[p] != timestamp:
                vis[p] = timestamp
                if nodes[p]['count'] == old_total:
                    llink = nodes[p]['link']
                    prev_len = 0 if llink == -1 else nodes[llink]['len']
                    new_answer += nodes[p]['len'] - prev_len
                nodes[p]['count'] += 1
                p = nodes[p]['link']
        answer = new_answer
    elif op == 'D':
        i = int(data[idx])
        idx += 1
        del S[i]
        terminals = insert_to_sam(S)
        old_total = total_versions
        total_versions += 1
        new_answer = 0
        timestamp += 1
        for t in terminals:
            p = t
            while p != -1 and vis[p] != timestamp:
                vis[p] = timestamp
                if nodes[p]['count'] == old_total:
                    llink = nodes[p]['link']
                    prev_len = 0 if llink == -1 else nodes[llink]['len']
                    new_answer += nodes[p]['len'] - prev_len
                nodes[p]['count'] += 1
                p = nodes[p]['link']
        answer = new_answer
    elif op == 'Q':
        print(answer)