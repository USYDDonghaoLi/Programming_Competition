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