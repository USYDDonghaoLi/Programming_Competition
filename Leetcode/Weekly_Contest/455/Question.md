## Q1. Check if Any Element Has Prime Frequency

You are given an integer array ```nums```.

Return ```true``` if the frequency of any element of the array is **prime**, otherwise, return ```false```.

The **frequency** of an element ```x``` is the number of times it occurs in the array.

A prime number is a natural number greater than $1$ with only two factors, $1$ and itself.

**Example 1**:

Input: nums = [1,2,3,4,5,4]

Output: true

Explanation:

4 has a frequency of two, which is a prime number.

**Example 2**:

Input: nums = [1,2,3,4,5]

Output: false

Explanation:

All elements have a frequency of one.

**Example 3**:

Input: nums = [2,2,2,4,4]

Output: true

Explanation:

Both 2 and 4 have a prime frequency.

 
**Constraints**:

```1 <= nums.length <= 100```
```0 <= nums[i] <= 100```

## Q2. Inverse Coin Change

You are given a **1-indexed** integer array ```numWays```, where ```numWays[i]``` represents the number of ways to select a total amount ```i``` using an **infinite** supply of some *fixed* coin denominations. Each denomination is a **positive** integer with value **at most** ```numWays.length```.

However, the exact coin denominations have been *lost*. Your task is to recover the set of denominations that could have resulted in the given ```numWays``` array.

Return a **sorted** array containing **unique** integers which represents this set of denominations.

If no such set exists, return an **empty** array.

 

**Example 1**:

Input: numWays = [0,1,0,2,0,3,0,4,0,5]

Output: [2,4,6]

Explanation:

$$
\begin{pmatrix}
Amount 	&Number of ways	&Explanation \\
1	&0	&\text{There is no way to select coins with total value 1.} \\
2	&1	&\text{The only way is [2].}\\
3	&0	&\text{There is no way to select coins with total value 3.}\\
4	&2	&\text{The ways are [2, 2] and [4].}\\
5	&0	&\text{There is no way to select coins with total value 5.}\\
6	&3	&\text{The ways are [2, 2, 2], [2, 4], and [6].}\\
7	&0	&\text{There is no way to select coins with total value 7.}\\
8	&4	&\text{The ways are [2, 2, 2, 2], [2, 2, 4], [2, 6], and [4, 4].}\\
9	&0	&\text{There is no way to select coins with total value 9.}\\
10	&5	&\text{The ways are [2, 2, 2, 2, 2], [2, 2, 2, 4], [2, 4, 4], [2, 2, 6], and [4, 6].}\\
\end{pmatrix}
$$

**Example 2**:
Input: numWays = [1,2,2,3,4]

Output: [1,2,5]

Explanation:

$$
\begin{pmatrix}
Amount	&Number of ways	&Explanation\\
1	&1	&\text{The only way is [1].}\\
2	&2	&\text{The ways are [1, 1] and [2].}\\
3	&2	&\text{The ways are [1, 1, 1] and [1, 2].}\\
4	&3	&\text{The ways are [1, 1, 1, 1], [1, 1, 2], and [2, 2].}\\
5	&4	&\text{The ways are [1, 1, 1, 1, 1], [1, 1, 1, 2], [1, 2, 2], and [5].}\\
\end{pmatrix}
$$

## Example 3:

Input: numWays = [1,2,3,4,15]

Output: []

Explanation:

No set of denomination satisfies this array.

 

Constraints:

```
1 <= numWays.length <= 100
0 <= numWays[i] <= 2 * 108
```

## Q3. Minimum Increments to Equalize Leaf Paths

You are given an integer ```n``` and an undirected tree rooted at node $0$ with ```n``` nodes numbered from 0 to ```n - 1```. This is represented by a 2D array ```edges``` of length ```n - 1```, where ```edges[i] = [ui, vi]``` indicates an edge from node $u_i$ to $v_i$ .

Each node ```i``` has an associated cost given by ```cost[i]```, representing the cost to traverse that node.

The **score** of a path is defined as the sum of the costs of all nodes along the path.

Your goal is to make the scores of all **root-to-leaf** paths **equal** by **increasing** the cost of any number of nodes by **any non-negative** amount.

Return the **minimum** number of nodes whose cost must be increased to make all root-to-leaf path scores equal.

 

**Example 1**:

Input: n = 3, edges = [[0,1],[0,2]], cost = [2,1,3]

Output: 1

Explanation:



There are two root-to-leaf paths:

Path 0 → 1 has a score of 2 + 1 = 3.
Path 0 → 2 has a score of 2 + 3 = 5.
To make all root-to-leaf path scores equal to 5, increase the cost of node 1 by 2.
Only one node is increased, so the output is 1.

**Example 2**:

Input: n = 3, edges = [[0,1],[1,2]], cost = [5,1,4]

Output: 0

Explanation:



There is only one root-to-leaf path:

Path 0 → 1 → 2 has a score of 5 + 1 + 4 = 10.

Since only one root-to-leaf path exists, all path costs are trivially equal, and the output is 0.

**Example 3**:

Input: n = 5, edges = [[0,4],[0,1],[1,2],[1,3]], cost = [3,4,1,1,7]

Output: 1

Explanation:



There are three root-to-leaf paths:

Path 0 → 4 has a score of 3 + 7 = 10.
Path 0 → 1 → 2 has a score of 3 + 4 + 1 = 8.
Path 0 → 1 → 3 has a score of 3 + 4 + 1 = 8.
To make all root-to-leaf path scores equal to 10, increase the cost of node 1 by 2. Thus, the output is 1.

 

**Constraints**:

$$
2 <= n <= 10^5 \\
edges.length == n - 1 \\
edges[i] == [u_i, v_i] \\
0 <= u_i, v_i < n \\
cost.length == n \\
1 <= cost[i] <= 10^9 \\
\text{The input is generated such that edges represents a valid tree.}
$$

## Q4. Minimum Time to Transport All Individuals

You are given ```n``` individuals at a base camp who need to cross a river to reach a destination using a single boat. The boat can carry at most ```k``` people at a time. The trip is affected by environmental conditions that vary **cyclically** over ```m``` stages.

Each stage ```j``` has a speed multiplier ```mul[j]```:

If ```mul[j] > 1```, the trip slows down.
If ```mul[j] < 1```, the trip speeds up.
Each individual ```i``` has a rowing strength represented by ```time[i]```, the time (in minutes) it takes them to cross alone in neutral conditions.

Rules:

A group ```g``` departing at stage ```j``` takes time equal to the **maximum** ```time[i]``` among its members, multiplied by ```mul[j]``` minutes to reach the destination.
After the group crosses the river in time ```d```, the stage advances by ```floor(d) % m``` steps.
If individuals are left behind, one person must return with the boat. Let ```r``` be the index of the returning person, the return takes ```time[r] × mul[current_stage]```, defined as ```return_time```, and the stage advances by ```floor(return_time) % m```.
Return the **minimum** total time required to transport all individuals. If it is not possible to transport all individuals to the destination, return ```-1```.

 

**Example 1**:

Input: n = 1, k = 1, m = 2, time = [5], mul = [1.0,1.3]

Output: 5.00000

Explanation:

Individual 0 departs from stage 0, so crossing time = 5 × 1.00 = 5.00 minutes.
All team members are now at the destination. Thus, the total time taken is 5.00 minutes.

**Example 2**:

Input: n = 3, k = 2, m = 3, time = [2,5,8], mul = [1.0,1.5,0.75]

Output: 14.50000

Explanation:

The optimal strategy is:

Send individuals 0 and 2 from the base camp to the destination from stage 0. The crossing time is max(2, 8) × mul[0] = 8 × 1.00 = 8.00 minutes. The stage advances by floor(8.00) % 3 = 2, so the next stage is (0 + 2) % 3 = 2.
Individual 0 returns alone from the destination to the base camp from stage 2. The return time is 2 × mul[2] = 2 × 0.75 = 1.50 minutes. The stage advances by floor(1.50) % 3 = 1, so the next stage is (2 + 1) % 3 = 0.
Send individuals 0 and 1 from the base camp to the destination from stage 0. The crossing time is max(2, 5) × mul[0] = 5 × 1.00 = 5.00 minutes. The stage advances by floor(5.00) % 3 = 2, so the final stage is (0 + 2) % 3 = 2.
All team members are now at the destination. The total time taken is 8.00 + 1.50 + 5.00 = 14.50 minutes.

**Example 3**:

Input: n = 2, k = 1, m = 2, time = [10,10], mul = [2.0,2.0]

Output: -1.00000

Explanation:

Since the boat can only carry one person at a time, it is impossible to transport both individuals as one must always return. Thus, the answer is -1.00.
 

**Constraints**:

$$
1 <= n == time.length <= 12 \\
1 <= k <= 5 \\
1 <= m <= 5 \\
1 <= time[i] <= 100 \\
m == mul.length \\
0.5 <= mul[i] <= 2.0 \\
$$