import sys,sys
import bisect

def main():
    import sys
    input = sys.stdin.readline

    N, W = map(int, input().split())
    # Lists for block info.
    X = [0]*N
    Y = [0]*N
    for i in range(N):
        x, y = map(int, input().split())
        X[i] = x
        Y[i] = y

    # Group blocks by column (1-indexed)
    cols = [[] for _ in range(W+1)]
    for i in range(N):
        c = X[i]
        cols[c].append((Y[i], i))
    
    # For each column, sort by y (increasing order) and assign order.
    # Also record the count in each column.
    block_order = [0]*N  # block_order[i] will store the order (1-indexed) of block i in its column.
    col_count = [0]*(W+1)
    for c in range(1, W+1):
        if cols[c]:
            cols[c].sort(key=lambda tup: tup[0])
            col_count[c] = len(cols[c])
            for j, (_, block_idx) in enumerate(cols[c]):
                block_order[block_idx] = j+1
        else:
            col_count[c] = 0

    # If some column is empty, then no removal ever occurs.
    global_removal = True
    for c in range(1, W+1):
        if col_count[c] == 0:
            global_removal = False
            break

    if not global_removal:
        # Simply answer "Yes" for every query.
        Q = int(input())
        out_lines = []
        for _ in range(Q):
            input()  # read and ignore query parameters
            out_lines.append("Yes")
        sys.stdout.write("\n".join(out_lines))
        return

    # Global removal is active.
    # R is the maximum number of removals that can ever occur
    R = min(col_count[1:])  # since cols are 1-indexed

    # For each column c, for each i from 1 to len(cols[c]),
    # define candidate = Y_{c,i} + (i-1). (We only need i up to R.)
    # Then for each i = 1,...,R, define T_i = max_{c with |c|>= i} (candidate).
    global_T = [0]*R  # global_T[i-1] will be T_i.
    # Initialize with 0.
    for i in range(R):
        global_T[i] = 0
    for c in range(1, W+1):
        L = col_count[c]
        # Only consider positions up to R.
        upto = min(L, R)
        # For the sorted list cols[c], the block with order i is at index i-1.
        for i in range(1, upto+1):
            candidate = cols[c][i-1][0] + (i-1)
            if candidate > global_T[i-1]:
                global_T[i-1] = candidate
    # Note: global_T is non-decreasing.
    
    # For each query, we need to determine the number r_eff(T)
    # = maximum i in {0,1,...,R} such that T_i <= T.
    # (We set r_eff = 0 if T < T_1.)
    Q = int(input())
    out_lines = []
    for _ in range(Q):
        T_str = input().split()
        if not T_str: 
            break
        T, A = map(int, T_str)
        A -= 1  # convert to 0-index
        # Use binary search in global_T (of length R) to find how many T_i are <= T.
        # bisect_right returns an index in 0..R.
        r_eff = bisect.bisect_right(global_T, T)
        # A block (with order r) survives if and only if r > r_eff.
        if block_order[A] > r_eff:
            out_lines.append("Yes")
        else:
            out_lines.append("No")
    sys.stdout.write("\n".join(out_lines))
    
if __name__ == '__main__':
    main()
