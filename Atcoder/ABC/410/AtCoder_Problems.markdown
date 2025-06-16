# AtCoder Problems

## A - G1

**Time Limit**: 2 sec  
**Memory Limit**: 1024 MiB  
**Score**: 100 points

### Problem Statement
In AtCoder Kingdom, there are $N$ horse races. Horses aged $A_i$ or younger can participate in the $i$-th race. How many races can a $K$-year-old horse participate in?

### Constraints
- All input values are integers.
- $1 \leq N \leq 100$
- $1 \leq A_i \leq 100$
- $1 \leq K \leq 100$

### Input
Input is given from Standard Input in the following format:
```
N
A_1
A_2
...
A_N
K
```

### Output
Output the answer as an integer.

### Sample Input 1
```
5
3 1 4 1 5
4
```

### Sample Output 1
```
2
```

**Explanation**:  
- 1st race: Horses aged $\leq 3$.
- 2nd race: Horses aged $\leq 1$.
- 3rd race: Horses aged $\leq 4$.
- 4th race: Horses aged $\leq 1$.
- 5th race: Horses aged $\leq 5$.  
A 4-year-old horse can participate in the 3rd and 5th races, so the answer is 2.

### Sample Input 2
```
1
1
100
```

### Sample Output 2
```
0
```

**Explanation**: No races are available for a 100-year-old horse.

### Sample Input 3
```
15
18 89 31 2 15 93 64 78 58 19 79 59 24 50 30
38
```

### Sample Output 3
```
8
```

## B - Reverse Proxy

**Time Limit**: 2 sec  
**Memory Limit**: 1024 MiB  
**Score**: 200 points

### Problem Statement
There are $N$ boxes numbered $1, 2, \ldots, N$, initially empty. $Q$ balls arrive in order, and Takahashi places them into boxes based on sequence $X = (X_1, X_2, \ldots, X_Q)$:
- If $X_i \geq 1$: Put the ball into box $X_i$.
- If $X_i = 0$: Put the ball into the box with the smallest number among those with the fewest balls.  
Find which box each ball was put into.

### Constraints
- All input values are integers.
- $1 \leq N \leq 100$
- $1 \leq Q \leq 100$
- $0 \leq X_i \leq N$

### Input
Input is given from Standard Input in the following format:
```
N Q
X_1
X_2
...
X_Q
```

### Output
For the $i$-th ball placed in box $B_i$, output:
```
B_1
B_2
...
B_Q
```

### Sample Input 1
```
4 5
2 0 3 0 0
```

### Sample Output 1
```
2 1 3 4 1
```

**Explanation**:  
- Initially: Boxes 1,2,3,4 have 0,0,0,0 balls.
- $X_1 = 2$: 1st ball to box 2 (0,1,0,0).
- $X_2 = 0$: 2nd ball to box 1 (1,1,0,0).
- $X_3 = 3$: 3rd ball to box 3 (1,1,1,0).
- $X_4 = 0$: 4th ball to box 4 (1,1,1,1).
- $X_5 = 0$: 5th ball to box 1 (2,1,1,1).  
Output: 2 1 3 4 1.

### Sample Input 2
```
3 7
1 1 0 0 0 0 0
```

### Sample Output 2
```
1 1 2 3 2 3 1
```

### Sample Input 3
```
6 20
4 6 0 3 4 2 6 5 2 3 0 3 2 5 0 3 5 0 2 0
```

### Sample Output 3
```
4 6 1 3 4 2 6 5 2 3 1 3 2 5 1 3 5 4 2 6
```

## C - Rotatable Array

**Time Limit**: 2 sec  
**Memory Limit**: 1024 MiB  
**Score**: 300 points

### Problem Statement
Given an integer sequence $A$ of length $N$, initially $A_i = i$. Process $Q$ queries of the following types:
1. Change $A_p$ to $x$.
2. Output $A_p$.
3. Rotate $A$ by moving the first element to the end $k$ times (i.e., replace $A$ with $(A_2, A_3, \ldots, A_N, A_1)$ $k$ times).

### Constraints
- All input values are integers.
- $1 \leq N \leq 10^6$
- $1 \leq Q \leq 3 \times 10^5$
- For all queries:
  - $1 \leq p \leq N$
  - $1 \leq x \leq 10^6$
  - $1 \leq k \leq 10^9$

### Input
Input is given from Standard Input in the following format:
```
N Q
Query_1
Query_2
...
Query_Q
```
- Type 1: `1 p x`
- Type 2: `2 p`
- Type 3: `3 k`

### Output
For each Type 2 query, output the answer on a new line.

### Sample Input 1
```
5 5
2 3
1 2 1000000
3 4
2 2
2 3
```

### Sample Output 1
```
3
1
1000000
```

**Explanation**:  
- Initially: $A = (1,2,3,4,5)$.
- Query 1 (Type 2): Output $A_3 = 3$.
- Query 2 (Type 1): Set $A_2 = 1000000$, so $A = (1,1000000,3,4,5)$.
- Query 3 (Type 3): Rotate 4 times, so $A = (5,1,1000000,3,4)$.
- Query 4 (Type 2): Output $A_2 = 1$.
- Query 5 (Type 2): Output $A_3 = 1000000$.

### Sample Input 2
```
1000000 2
1 1000000 999999
3 1000000000
```

### Sample Output 2
```
```

**Explanation**: No Type 2 queries, so output is empty.

## D - XOR Shortest Walk

**Time Limit**: 2 sec  
**Memory Limit**: 1024 MiB  
**Score**: 400 points

### Problem Statement
Given a directed graph with $N$ vertices and $M$ edges, where edge $i$ goes from vertex $A_i$ to $B_i$ with weight $W_i$, find the minimum bitwise XOR of edge weights in a walk from vertex 1 to vertex $N$.

### Constraints
- $2 \leq N \leq 1000$
- $0 \leq M \leq 1000$
- $1 \leq A_i, B_i \leq N$
- $0 \leq W_i < 2^{10}$
- All input values are integers.

### Input
Input is given from Standard Input in the following format:
```
N M
A_1 B_1 W_1
A_2 B_2 W_2
...
A_M B_M W_M
```

### Output
- If no walk exists from vertex 1 to $N$, output `-1`.
- Otherwise, output the minimum bitwise XOR of edge weights in such a walk.

### Sample Input 1
```
3 3
1 2 4
2 3 5
1 3 2
```

### Sample Output 1
```
1
```

**Explanation**: The walk (edge 1, edge 2) has XOR $4 \oplus 5 = 1$.

### Sample Input 2
```
4 4
1 4 7
4 2 2
2 3 4
3 4 1
```

### Sample Output 2
```
0
```

**Explanation**: The walk (edge 1, edge 2, edge 3, edge 4) has XOR $7 \oplus 2 \oplus 4 \oplus 1 = 0$.

### Sample Input 3
```
999 4
1 2 9
2 1 8
1 2 7
1 1 6
```

### Sample Output 3
```
-1
```

**Explanation**: No walk exists from vertex 1 to vertex 999.

## E - Battles in a Row

**Time Limit**: 2 sec  
**Memory Limit**: 1024 MiB  
**Score**: 450 points

### Problem Statement
Takahashi fights $N$ monsters in order, starting with health $H$ and magic power $M$. For the $i$-th monster, he can:
- Fight without magic (if health $\geq A_i$): Health decreases by $A_i$, monster defeated.
- Fight with magic (if magic power $\geq B_i$): Magic power decreases by $B_i$, monster defeated.  
The game ends when all monsters are defeated or no action is possible. Find the maximum number of monsters Takahashi can defeat.

### Constraints
- $1 \leq N \leq 3000$
- $1 \leq H, M \leq 3000$
- $1 \leq A_i, B_i \leq 3000$
- All input values are integers.

### Input
Input is given from Standard Input in the following format:
```
N H M
A_1 B_1
A_2 B_2
...
A_N B_N
```

### Output
Output the maximum number of monsters defeated.

### Sample Input 1
```
4 10 14
5 8
5 6
7 9
99 99
```

### Sample Output 1
```
3
```

**Explanation**:  
- Initial: Health = 10, Magic = 14.
- Monster 1: Fight without magic, health -= 5 (5,14).
- Monster 2: Fight without magic, health -= 5 (0,14).
- Monster 3: Fight with magic, magic -= 9 (0,5).
- Monster 4: Cannot fight (health < 99, magic < 99).  
Maximum defeated: 3.

### Sample Input 2
```
3 3000 3000
3 3
3 3
3 3
```

### Sample Output 2
```
3
```

**Explanation**: All monsters can be defeated.

### Sample Input 3
```
10 8 8
2 2
2 3
2 2
1 2
2 3
1 2
3 3
3 2
3 1
3 2
```

### Sample Output 3
```
9
```

## F - Balanced Rectangles

**Time Limit**: 3 sec  
**Memory Limit**: 1024 MiB  
**Score**: 525 points

### Problem Statement
Given an $H \times W$ grid where each cell is `#` or `.`, find the number of rectangular regions where the number of `#` and `.` cells is equal. The grid is represented by $H$ strings $S_1, S_2, \ldots, S_H$ of length $W$. Formally, count quadruples $(u,d,l,r)$ satisfying:
- $1 \leq u \leq d \leq H$
- $1 \leq l \leq r \leq W$
- The extracted rectangle has an equal number of `#` and `.` cells.  
Solve for $T$ test cases.

### Constraints
- $1 \leq T \leq 25000$
- $1 \leq H, W$
- Sum of $H \times W$ across all test cases $\leq 3 \times 10^5$.
- $S_i$ is a string of length $W$ containing `#` or `.`.

### Input
Input is given from Standard Input in the following format:
```
T
case_1
case_2
...
case_T
```
Each test case:
```
H W
S_1
S_2
...
S_H
```

### Output
Output $T$ lines, with the $i$-th line containing the answer for the $i$-th test case.

### Sample Input 1
```
3
3 2
##
#.
..
6 6
..#...
..#..#
#.#.#.
.###..
######
.###..
15 50
... (omitted for brevity)
```

### Sample Output 1
```
4
79
4032
```

**Explanation for Case 1**: The following rectangles satisfy the conditions:
- Rows 1-2, Columns 2-2
- Rows 2-3, Columns 1-1
- Rows 2-2, Columns 1-2
- Rows 1-3, Columns 1-2

## G - Longest Chord Chain

**Time Limit**: 2 sec  
**Memory Limit**: 1024 MiB  
**Score**: 575 points

### Problem Statement
Given $2N$ distinct points on a circle (numbered 1 to $2N$ in clockwise order) and $N$ chords with endpoints $A_i$ and $B_i$, perform:
1. Choose any number of non-intersecting chords and delete the rest.
2. Add one chord freely.  
Find the maximum possible number of intersection points between chords after these operations.

### Constraints
- $1 \leq N \leq 2 \times 10^5$
- $1 \leq A_i, B_i \leq 2N$
- $A_1, \ldots, A_N, B_1, \ldots, B_N$ are pairwise distinct.
- All input values are integers.

### Input
Input is given from Standard Input in the following format:
```
N
A_1 B_1
A_2 B_2
...
A_N B_N
```

### Output
Output the maximum number of intersection points.

### Sample Input 1
```
3
1 5
6 3
4 2
```

### Sample Output 1
```
2
```

**Explanation**: Delete chord (3,6), add a new chord to get 2 intersection points. More than 2 is impossible.

### Sample Input 2
```
4
1 8
2 7
3 6
4 5
```

### Sample Output 2
```
4
```

### Sample Input 3
```
3
1 2
3 4
5 6
```

### Sample Output 3
```
2
```