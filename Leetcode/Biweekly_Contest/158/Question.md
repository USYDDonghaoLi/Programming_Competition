# Q1: Maximize Y-Sum by Picking a Triplet of Distinct X-Values

## Problem Statement

You are given two integer arrays `x` and `y`, each of length `n`. You must choose three distinct indices `i`, `j`, and `k` such that:

- `x[i] != x[j]`
- `x[j] != x[k]`
- `x[k] != x[i]`

Your goal is to maximize the value of `y[i] + y[j] + y[k]` under these conditions. Return the maximum possible sum that can be obtained by choosing such a triplet of indices.

If no such triplet exists, return `-1`.

## Examples

### Example 1:

**Input**: `x = [1,2,1,3,2], y = [5,3,4,6,2]`

**Output**: `14`

**Explanation**:

Choose `i = 0` (`x[i] = 1, y[i] = 5`), `j = 1` (`x[j] = 2, y[j] = 3`), `k = 3` (`x[k] = 3, y[k] = 6`).
All three values chosen from `x` are distinct. `5 + 3 + 6 = 14` is the maximum we can obtain. Hence, the output is `14`.

### Example 2:

**Input**: `x = [1,2,1,2], y = [4,5,6,7]`

**Output**: `-1`

**Explanation**:

There are only two distinct values in `x`. Hence, the output is `-1`.

## Constraints

- `n == x.length == y.length`
- `3 <= n <= 10^5`
- `1 <= x[i], y[i] <= 10^6`

# Q2: Best Time to Buy and Sell Stock V

## Problem Statement

You are given an integer array `prices` where `prices[i]` is the price of a stock in dollars on the `i`th day, and an integer `k`.

You are allowed to make at most `k` transactions, where each transaction can be either of the following:

- **Normal transaction**: Buy on day `i`, then sell on a later day `j` where `i < j`. You profit `prices[j] - prices[i]`.
- **Short selling transaction**: Sell on day `i`, then buy back on a later day `j` where `i < j`. You profit `prices[i] - prices[j]`.

Note that you must complete each transaction before starting another. Additionally, you can't buy or sell on the same day you are selling or buying back as part of a previous transaction.

Return the maximum total profit you can earn by making at most `k` transactions.

## Examples

### Example 1:

**Input**: `prices = [1,7,9,8,2], k = 2`

**Output**: `14`

**Explanation**:

We can make $14 of profit through 2 transactions:
- A normal transaction: buy the stock on day 0 for $1 then sell it on day 2 for $9.
- A short selling transaction: sell the stock on day 3 for $8 then buy back on day 4 for $2.

### Example 2:

**Input**: `prices = [12,16,19,19,8,1,19,13,9], k = 3`

**Output**: `36`

**Explanation**:

We can make $36 of profit through 3 transactions:
- A normal transaction: buy the stock on day 0 for $12 then sell it on day 2 for $19.
- A short selling transaction: sell the stock on day 3 for $19 then buy back on day 4 for $8.
- A normal transaction: buy the stock on day 5 for $1 then sell it on day 6 for $19.

## Constraints

- `2 <= prices.length <= 10^3`
- `1 <= prices[i] <= 10^9`
- `1 <= k <= prices.length / 2`

# Q3: Maximize Subarray GCD Score

## Problem Statement

You are given an array of positive integers `nums` and an integer `k`.

You may perform at most `k` operations. In each operation, you can choose one element in the array and double its value. Each element can be doubled at most once.

The score of a contiguous subarray is defined as the product of its length and the greatest common divisor (GCD) of all its elements.

Your task is to return the maximum score that can be achieved by selecting a contiguous subarray from the modified array.

**Note**:

The greatest common divisor (GCD) of an array is the largest integer that evenly divides all the array elements.

## Examples

### Example 1:

**Input**: `nums = [2,4], k = 1`

**Output**: `8`

**Explanation**:

Double `nums[0]` to 4 using one operation. The modified array becomes `[4, 4]`.
The GCD of the subarray `[4, 4]` is 4, and the length is 2.
Thus, the maximum possible score is `2 × 4 = 8`.

### Example 2:

**Input**: `nums = [3,5,7], k = 2`

**Output**: `14`

**Explanation**:

Double `nums[2]` to 14 using one operation. The modified array becomes `[3, 5, 14]`.
The GCD of the subarray `[14]` is 14, and the length is 1.
Thus, the maximum possible score is `1 × 14 = 14`.

### Example 3:

**Input**: `nums = [5,5,5], k = 1`

**Output**: `15`

**Explanation**:

The subarray `[5, 5, 5]` has a GCD of 5, and its length is 3.
Since doubling any element doesn't improve the score, the maximum score is `3 × 5 = 15`.

## Constraints

- `1 <= nums.length <= 100` (Note: This constraint is inferred based on typical problem constraints for hard problems involving GCD and subarrays, as the original problem statement does not explicitly provide it.)
- `1 <= nums[i] <= 10^9`
- `0 <= k <= nums.length`

# Q4: Maximum Good Subtree Score

## Problem Statement

You are given an undirected tree rooted at node `0` with `n` nodes numbered from `0` to `n - 1`. Each node `i` has an integer value `vals[i]`, and its parent is given by `par[i]`.

A subset of nodes within the subtree of a node is called **good** if every digit from `0` to `9` appears at most once in the decimal representation of the values of the selected nodes.

The **score** of a good subset is the sum of the values of its nodes.

Define an array `maxScore` of length `n`, where `maxScore[u]` represents the maximum possible sum of values of a good subset of nodes that belong to the subtree rooted at node `u`, including `u` itself and all its descendants.

Return the sum of all values in `maxScore`.

Since the answer may be large, return it modulo `10^9 + 7`.

## Examples

### Example 1:

**Input**: `vals = [2,3], par = [-1,0]`

**Output**: `8`

**Explanation**:

- The subtree rooted at node `0` includes nodes `{0, 1}`. The subset `{2, 3}` is good as the digits `2` and `3` appear only once. The score of this subset is `2 + 3 = 5`.
- The subtree rooted at node `1` includes only node `{1}`. The subset `{3}` is good. The score of this subset is `3`.
- The `maxScore` array is `[5, 3]`, and the sum of all values in `maxScore` is `5 + 3 = 8`. Thus, the answer is `8`.

### Example 2:

**Input**: `vals = [1,5,2], par = [-1,0,0]`

**Output**: `15`

**Explanation**:

- The subtree rooted at node `0` includes nodes `{0, 1, 2}`. The subset `{1, 5, 2}` is good as the digits `1`, `5`, and `2` appear only once. The score of this subset is `1 + 5 + 2 = 8`.
- The subtree rooted at node `1` includes only node `{1}`. The subset `{5}` is good. The score of this subset is `5`.
- The subtree rooted at node `2` includes only node `{2}`. The subset `{2}` is good. The score of this subset is `2`.
- The `maxScore` array is `[8, 5, 2]`, and the sum of all values in `maxScore` is `8 + 5 + 2 = 15`. Thus, the answer is `15`.

### Example 3:

**Input**: `vals = [34,1,2], par = [-1,0,1]`

**Output**: `42`

**Explanation**:

- The subtree rooted at node `0` includes nodes `{0, 1, 2}`. The subset `{34, 1, 2}` is good as the digits `3`, `4`, `1`, and `2` appear only once. The score of this subset is `34 + 1 + 2 = 37`.
- The subtree rooted at node `1` includes nodes `{1, 2}`. The subset `{1, 2}` is good as the digits `1` and `2` appear only once. The score of this subset is `1 + 2 = 3`.
- The subtree rooted at node `2` includes only node `{2}`. The subset `{2}` is good. The score of this subset is `2`.
- The `maxScore` array is `[37, 3, 2]`, and the sum of all values in `maxScore` is `37 + 3 + 2 = 42`. Thus, the answer is `42`.

### Example 4:

**Input**: `vals = [3,22,5], par = [-1,0,1]`

**Output**: `18`

**Explanation**:

- The subtree rooted at node `0` includes nodes `{0, 1, 2}`. The subset `{3, 22, 5}` is not good, as digit `2` appears twice. Therefore, the subset `{3, 5}` is valid. The score of this subset is `3 + 5 = 8`.
- The subtree rooted at node `1` includes nodes `{1, 2}`. The subset `{22, 5}` is not good, as digit `2` appears twice. Therefore, the subset `{5}` is valid. The score of this subset is `5`.
- The subtree rooted at node `2` includes only node `{2}`. The subset `{5}` is good. The score of this subset is `5`.
- The `maxScore` array is `[8, 5, 5]`, and the sum of all values in `maxScore` is `8 + 5 + 5 = 18`. Thus, the answer is `18`.

## Constraints

- `1 <= n == vals.length <= 500`
- `1 <= vals[i] <= 10^9`
- `par.length == n`
- `par[0] == -1`
- `0 <= par[i] < n` for `i` in `[1, n - 1]`
- The input is generated such that the parent array `par` represents a valid tree. 