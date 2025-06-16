# AtCoder Contest

## A. Horse Races

### Problem Statement

In AtCoder Kingdom, there are $N$ horse races being held. Horses aged $A_i$ or younger can participate in the $i$-th race. Among the $N$ races, how many races can a $K$-year-old horse participate in?

### Constraints

- All input values are integers.
- $1 \leq N \leq 100$
- $1 \leq A_i \leq 100$
- $1 \leq K \leq 100$

### Input

The input is given from Standard Input in the following format:

N $A_1$ $A_2$ $\vdots$ $A_N$ K


### Output

Output the answer as an integer.

### Sample Input 1

5 3 1 4 1 5 4


### Sample Output 1

2


### Explanation for Sample 1

- Horses aged $3$ or younger can participate in the 1st race.
- Horses aged $1$ or younger can participate in the 2nd race.
- Horses aged $4$ or younger can participate in the 3rd race.
- Horses aged $1$ or younger can participate in the 4th race.
- Horses aged $5$ or younger can participate in the 5th race.
- Among the 5 races, a 4-year-old horse can participate in the 3rd and 5th races, which is $2$ races.

### Sample Input 2

1 1 100


### Sample Output 2

0


### Explanation for Sample 2

There may be no races that a $K$-year-old horse can participate in.

### Sample Input 3

15 18 89 31 2 15 93 64 78 58 19 79 59 24 50 30 38


### Sample Output 3

8


---

## B. Reverse Proxy

### Problem Statement

There are $N$ boxes numbered $1, 2, \ldots, N$. Initially, all boxes are empty.

$Q$ balls will come in order. Takahashi will put the balls into the boxes according to the sequence $X = (X_1, X_2, \ldots, X_Q)$. Specifically, he performs the following process for the $i$-th ball:

- If $X_i \geq 1$: Put this ball into box $X_i$.
- If $X_i = 0$: Put this ball into the box with the smallest number among those containing the fewest balls.

Find which box each ball was put into.

### Constraints

- All input values are integers.
- $1 \leq N \leq 100$
- $1 \leq Q \leq 100$
- $0 \leq X_i \leq N$

### Input

The input is given from Standard Input in the following format:

N Q X_1 X_2 \ldots X_Q


### Output

If the $i$-th ball was put into box $B_i$, output in the following format:

B_1 B_2 \ldots B_Q


### Sample Input 1

4 5 2 0 3 0 0


### Sample Output 1

2 1 3 4 1


### Explanation for Sample 1

- There are $4$ boxes, and $5$ balls come.
- Initially, all boxes are empty. The numbers of balls in box $1, 2, 3, 4$ are $0, 0, 0, 0$, respectively.
- Since $X_1 = 2$, put the 1st ball into box $2$. The numbers of balls in box $1, 2, 3, 4$ are $0, 1, 0, 0$, respectively.
- Since $X_2 = 0$, put the 2nd ball into box $1$, which has the smallest number among those containing the fewest balls. The numbers of balls in box $1, 2, 3, 4$ are $1, 1, 0, 0$, respectively.
- Since $X_3 = 3$, put the 3rd ball into box $3$. The numbers of balls in box $1, 2, 3, 4$ are $1, 1, 1, 0$, respectively.
- Since $X_4 = 0$, put the 4th ball into box $4$, which has the smallest number among those containing the fewest balls. The numbers of balls in box $1, 2, 3, 4$ are $1, 1, 1, 1$, respectively.
- Since $X_5 = 0$, put the 5th ball into box $1$, which has the smallest number among those containing the fewest balls. The numbers of balls in box $1, 2, 3, 4$ are $2, 1, 1, 1$, respectively.
- The balls were put into boxes $2, 1, 3, 4, 1$ in order. Thus, output $2 1 3 4 1$.

### Sample Input 2

3 7 1 1 0 0 0 0 0


### Sample Output 2

1 1 2 3 2 3 1


### Sample Input 3

6 20 4 6 0 3 4 2 6 5 2 3 0 3 2 5 0 3 5 0 2 0


### Sample Output 3

4 6 1 3 4 2 6 5 2 3 1 3 2 5 1 3 5 4 2 6


---

## C. Rotatable Array

### Problem Statement

There is an integer sequence $A$ of length $N$, initially $A_i = i$. Process a total of $Q$ queries of the following types:

- **Type 1**: Change $A_p$ to $x$.
- **Type 2**: Output $A_p$.
- **Type 3**: Repeat the operation "move the first element of $A$ to the end" $k$ times. Formally, replace $A$ with $(A_2, A_3, \ldots, A_N, A_1)$ $k$ times.

### Constraints

- All input values are integers.
- $1 \leq N \leq 10^6$
- $1 \leq Q \leq 3 \times 10^5$
- All queries satisfy the following constraints:
  - $1 \leq p \leq N$
  - $1 \leq x \leq 10^6$
  - $1 \leq k \leq 10^9$

### Input

The input is given from Standard Input in the following format:

N Q Query_1 Query_2 \vdots Query_Q


Here, $Query_i$ represents the $i$-th query.

Type 1 queries are given in the following format:

1 p x


Type 2 queries are given in the following format:

2 p


Type 3 queries are given in the following format:

3 k


### Output

For each Type 2 query, output the answer on a line.

### Sample Input 1

5 5 2 3 1 2 1000000 3 4 2 2 2 3


### Sample Output 1

3 1 1000000


### Explanation for Sample 1

- Initially, $A = (1, 2, 3, 4, 5)$.
- The 1st query is Type 2: output $A_3 = 3$.
- The 2nd query is Type 1: replace $A_2$ with $1000000$. After the query, $A = (1, 1000000, 3, 4, 5)$.
- The 3rd query is Type 3: repeat the operation "move the first element of $A$ to the end" $4$ times. After the query, $A = (5, 1, 1000000, 3, 4)$.
- The 4th query is Type 2: output $A_2 = 1$.
- The 5th query is Type 2: output $A_3 = 1000000$.

### Sample Input 2

1000000 2 1 1000000 999999 3 1000000000


### Sample Output 2


### Explanation for Sample 2

The output may be empty.

---

## D. XOR Shortest Walk

### Problem Statement

There is a directed graph with $N$ vertices and $M$ edges, where vertices are numbered from $1$ to $N$ and edges are numbered from $1$ to $M$. Edge $i$ is a directed edge from vertex $A_i$ to vertex $B_i$ with weight $W_i$.

Find the minimum value of the bitwise XOR of the weights of edges included in a walk from vertex $1$ to vertex $N$.

**What is a walk from vertex 1 to vertex N?**  
**What is the bitwise XOR operation?**

### Constraints

- $2 \leq N \leq 1000$
- $0 \leq M \leq 1000$
- $1 \leq A_i, B_i \leq N$
- $0 \leq W_i < 2^{10}$
- All input values are integers.

### Input

The input is given from Standard Input in the following format:

N M A_1 B_1 W_1 A_2 B_2 W_2 \vdots A_M B_M W_M


### Output

If there is no walk from vertex $1$ to vertex $N$, output $-1$.

If there is a walk from vertex $1$ to vertex $N$, output the minimum value of the bitwise XOR of the weights of edges included in such a walk.

### Sample Input 1

3 3 1 2 4 2 3 5 1 3 2


### Sample Output 1

1


### Explanation for Sample 1

The bitwise XOR of the weights of edges included in the walk (edge 1, edge 2) is $1$.

### Sample Input 2

4 4 1 4 7 4 2 2 2 3 4 3 4 1


### Sample Output 2

0


### Explanation for Sample 2

The bitwise XOR of the weights of edges included in the walk (edge 1, edge 2, edge 3, edge 4) is $0$.

Note that the walk may include vertex $N$ in the middle.

### Sample Input 3

999 4 1 2 9 2 1 8 1 2 7 1 1 6


### Sample Output 3

-1


### Explanation for Sample 3

If there is no walk from vertex $1$ to vertex $N$, output $-1$.

---

## E. Battles in a Row

### Problem Statement

Takahashi is about to play a game where he fights $N$ monsters in order. Initially, Takahashi's health is $H$ and his magic power is $M$.

For the $i$-th monster he fights, he can choose one of the following actions:

- **Fight without using magic**: This can only be chosen when his health is at least $A_i$, and his health decreases by $A_i$ and the monster is defeated.
- **Fight using magic**: This can only be chosen when his magic power is at least $B_i$, and his magic power decreases by $B_i$ and the monster is defeated.

The game ends when all $N$ monsters are defeated or when he cannot take any action. What is the maximum number of monsters he can defeat before the game ends?

### Constraints

- $1 \leq N \leq 3000$
- $1 \leq H, M \leq 3000$
- $1 \leq A_i, B_i \leq 3000$
- All input values are integers.

### Input

The input is given from Standard Input in the following format:

N H M A_1 B_1 A_2 B_2 \vdots A_N B_N


### Output

Output the answer.

### Sample Input 1

4 10 14 5 8 5 6 7 9 99 99


### Sample Output 1

3


### Explanation for Sample 1

By taking the following actions, Takahashi can defeat $3$ monsters before the game ends:

- Initially, his health is $10$ and his magic power is $14$.
- Fight the 1st monster without using magic. His health decreases by $5$, becoming health $5$ and magic power $14$.
- Fight the 2nd monster without using magic. His health decreases by $5$, becoming health $0$ and magic power $14$.
- Fight the 3rd monster using magic. His magic power decreases by $9$, becoming health $0$ and magic power $5$.
- For the 4th monster, he cannot choose either action, so the game ends.

### Sample Input 2

3 3000 3000 3 3 3 3 3 3


### Sample Output 2

3


### Explanation for Sample 2

He may be able to defeat all monsters.

### Sample Input 3

10 8 8 2 2 2 3 2 2 1 2 2 3 1 2 3 3 3 2 3 1 3 2


### Sample Output 3

9


---

## F. Balanced Rectangles

### Problem Statement

You are given an $H \times W$ grid, where each cell contains `#` or `.`. The information about the symbols written in each cell is given as $H$ strings $S_1, S_2, \ldots, S_H$ of length $W$, where the cell in the $i$-th row from the top and $j$-th column from the left contains the same symbol as the $j$-th character of $S_i$.

Find the number of rectangular regions in this grid that satisfy all of the following conditions:

- The number of cells containing `#` and the number of cells containing `.` in the rectangular region are equal.

Formally, find the number of quadruples of integers $(u, d, l, r)$ that satisfy all of the following conditions:

- $1 \leq u \leq d \leq H$
- $1 \leq l \leq r \leq W$
- When extracting the part of the grid from the $u$-th through $d$-th rows from the top and from the $l$-th through $r$-th columns from the left, the number of cells containing `#` and the number of cells containing `.` in the extracted part are equal.

You are given $T$ test cases. Find the answer for each of them.

### Constraints

- $1 \leq T \leq 25000$
- $1 \leq H, W$
- The sum of $H \times W$ over all test cases in one input does not exceed $3 \times 10^5$.
- $S_i$ is a string of length $W$ consisting of `#` and `.`.

### Input

The input is given from Standard Input in the following format:

T case_1 case_2 \vdots case_T


`case_i` represents the $i$-th test case. Each test case is given in the following format:

H W S_1 S_2 \vdots S_H


### Output

Output $T$ lines. The $i$-th line should contain the answer for the $i$-th test case.

### Sample Input 1

3 3 2



#. .. 6 6 ..#... ..#..# #.#.#. .###..



.###.. 15 50 .......................#...........###.###.###.### ....................#..#..#..........#.#.#...#.#.. .................#...#####...#.....###.#.#.###.### ..................#..##.##..#......#...#.#.#.....# ...................#########.......###.###.###.### ....................#.....#....................... .###........##......#.....#..#...#.####.####.##..# #..#.........#......#.....#..#...#.#....#....##..# #..#.........#......#.....#..#...#.#....#....##..# #.....##...###..##..#.....#..#...#.#....#....#.#.# #....#..#.#..#.#..#.#..##.#..#...#.####.####.#.#.# #....#..#.#..#.####.#....##..#...#.#....#....#.#.# #....#..#.#..#.#....#.....#..#...#.#....#....#..## #..#.#..#.#..#.#..#.#....#.#.#...#.#....#....#..## .##...##...####.##...####..#..###..####.####.#..##


### Sample Output 1

4 79 4032


### Explanation for Sample 1

- For the 1st case, the following $4$ rectangular regions satisfy the conditions in the problem statement:
  - From the 1st to 2nd rows from the top, from the 2nd to 2nd columns from the left.
  - From the 2nd to 3rd rows from the top, from the 1st to 1st columns from the left.
  - From the 2nd to 2nd rows from the top, from the 1st to 2nd columns from the left.
  - From the 1st to 3rd rows from the top, from the 1st to 2nd columns from the left.

---

## G. Longest Chord Chain

### Problem Statement

There are $2N$ pairwise distinct points, numbered from $1$ to $2N$, on a circle. Starting from point $1$ and going clockwise, the points are arranged as point $2$, point $3$, ..., point $2N$.

You are given $N$ chords on this circle. The endpoints of the $i$-th chord are points $A_i$ and $B_i$, and the $2N$ values $A_1, \ldots, A_N, B_1, \ldots, B_N$ are all distinct.

Perform the following operations on this circle once each in order:

1. Among the $N$ chords on the circle, choose any number of chords such that no two chosen chords intersect, and delete the remaining chords.
2. Add one chord freely to the circle.

Find the maximum possible number of intersection points between chords after the operations are completed.

### Constraints

- $1 \leq N \leq 2 \times 10^5$
- $1 \leq A_i, B_i \leq 2N$
- The $2N$ values $A_1, \ldots, A_N, B_1, \ldots, B_N$ are pairwise distinct.
- All input values are integers.

### Input

The input is given from Standard Input in the following format:

N A_1 B_1 A_2 B_2 \vdots A_N B_N


### Output

Output the answer.

### Sample Input 1

3 1 5 6 3 4 2


### Sample Output 1

2


### Explanation for Sample 1

- Initially, there are $3$ chords on the circle.
- After deleting the chord connecting points $3$ and $6$ and adding a new chord through the operations, the number of intersection points between chords is $2$.
- It is impossible to make the number of intersection points between chords $3$ or more, so the answer is $2$.
- The endpoints of the chord added at the end do not need to be any of the points $1, \ldots, 2N$.

### Sample Input 2

4 1 8 2 7 3 6 4 5


### Sample Output 2

4


### Sample Input 3

3 1 2 3 4 5 6


### Sample Output 3

2

