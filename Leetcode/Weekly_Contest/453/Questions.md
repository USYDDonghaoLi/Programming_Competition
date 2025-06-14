# Q1: Transform Array to All Equal Elements

## Problem Statement

You are given an integer array `nums` of size `n` containing only `1` and `-1`, and an integer `k`.

You can perform the following operation at most `k` times:

- Choose an index `i` (`0 <= i < n - 1`), and multiply both `nums[i]` and `nums[i + 1]` by `-1`.

Note that you can choose the same index `i` more than once in different operations.

Return `true` if it is possible to make all elements of the array equal after at most `k` operations, and `false` otherwise.

## Examples

### Example 1:

**Input**: `nums = [1,-1,1,-1,1], k = 3`

**Output**: `true`

**Explanation**:

We can make all elements in the array equal in 2 operations as follows:

1. Choose index `i = 1`, and multiply both `nums[1]` and `nums[2]` by `-1`. Now `nums = [1,1,-1,-1,1]`.
2. Choose index `i = 2`, and multiply both `nums[2]` and `nums[3]` by `-1`. Now `nums = [1,1,1,1,1]`.

### Example 2:

**Input**: `nums = [-1,-1,-1,1,1,1], k = 5`

**Output**: `false`

**Explanation**:

It is not possible to make all array elements equal in at most 5 operations.

## Constraints

- `1 <= n == nums.length <= 10^5`
- `nums[i]` is either `-1` or `1`.
- `1 <= k <= n`

# Q2: Count the Number of Computer Unlocking Permutations

## Problem Statement

You are given an array `complexity` of length `n`.

There are `n` locked computers in a room with labels from `0` to `n - 1`, each with its own unique password. The password of the computer `i` has a complexity `complexity[i]`.

The password for the computer labeled `0` is already decrypted and serves as the root. All other computers must be unlocked using it or another previously unlocked computer, following this information:

- You can decrypt the password for the computer `i` using the password for computer `j`, where `j` is any integer less than `i` with a lower complexity (i.e., `j < i` and `complexity[j] < complexity[i]`).
- To decrypt the password for computer `i`, you must have already unlocked a computer `j` such that `j < i` and `complexity[j] < complexity[i]`.

Find the number of permutations of `[0, 1, 2, ..., (n - 1)]` that represent a valid order in which the computers can be unlocked, starting from computer `0` as the only initially unlocked one.

Since the answer may be large, return it modulo `10^9 + 7`.

Note that the password for the computer with label `0` is decrypted, and not the computer with the first position in the permutation.

## Examples

### Example 1:

**Input**: `complexity = [1,2,3]`

**Output**: `2`

**Explanation**:

The valid permutations are:

- `[0, 1, 2]`
  - Unlock computer `0` first with root password.
  - Unlock computer `1` with password of computer `0` since `complexity[0] < complexity[1]`.
  - Unlock computer `2` with password of computer `1` since `complexity[1] < complexity[2]`.
- `[0, 2, 1]`
  - Unlock computer `0` first with root password.
  - Unlock computer `2` with password of computer `0` since `complexity[0] < complexity[2]`.
  - Unlock computer `1` with password of computer `0` since `complexity[0] < complexity[1]`.

### Example 2:

**Input**: `complexity = [3,3,3,4,4,4]`

**Output**: `0`

**Explanation**:

There are no possible permutations which can unlock all computers.

## Constraints

- `2 <= complexity.length <= 10^5`
- `1 <= complexity[i] <= 10^9`

# Q3: Count Partitions With Max-Min Difference at Most K

## Problem Statement

You are given an integer array `nums` and an integer `k`. Your task is to partition `nums` into one or more non-empty contiguous segments such that in each segment, the difference between its maximum and minimum elements is at most `k`.

Return the total number of ways to partition `nums` under this condition.

Since the answer may be too large, return it modulo `10^9 + 7`.

## Examples

### Example 1:

**Input**: `nums = [9,4,1,3,7], k = 4`

**Output**: `6`

**Explanation**:

There are 6 valid partitions where the difference between the maximum and minimum elements in each segment is at most `k = 4`:

- `[[9], [4], [1], [3], [7]]`
- `[[9], [4], [1], [3, 7]]`
- `[[9], [4], [1, 3], [7]]`
- `[[9], [4, 1], [3], [7]]`
- `[[9], [4, 1], [3, 7]]`
- `[[9], [4, 1, 3], [7]]`

### Example 2:

**Input**: `nums = [3,3,4], k = 0`

**Output**: `2`

**Explanation**:

There are 2 valid partitions that satisfy the given conditions:

- `[[3], [3], [4]]`
- `[[3, 3], [4]]`

## Constraints

- `2 <= nums.length <= 5 * 10^4`
- `1 <= nums[i] <= 10^9`
- `0 <= k <= 10^9`

# Q4: Minimum Steps to Convert String with Operations

## Problem Statement

You are given two strings, `word1` and `word2`, of equal length. You need to transform `word1` into `word2`.

For this, divide `word1` into one or more contiguous substrings. For each substring `substr` you can perform the following operations:

- **Replace**: Replace the character at any one index of `substr` with another lowercase English letter.
- **Swap**: Swap any two characters in `substr`.
- **Reverse Substring**: Reverse `substr`.

Each of these counts as one operation and each character of each substring can be used in each type of operation at most once (i.e., no single index may be involved in more than one replace, one swap, or one reverse).

Return the minimum number of operations required to transform `word1` into `word2`.

## Examples

### Example 1:

**Input**: `word1 = "abcdf", word2 = "dacbe"`

**Output**: `4`

**Explanation**:

Divide `word1` into `"ab"`, `"c"`, and `"df"`. The operations are:

- For the substring `"ab"`:
  - Perform operation of type 3 on `"ab"` -> `"ba"`.
  - Perform operation of type 1 on `"ba"` -> `"da"`.
- For the substring `"c"`, do no operations.
- For the substring `"df"`:
  - Perform operation of type 1 on `"df"` -> `"bf"`.
  - Perform operation of type 1 on `"bf"` -> `"be"`.

### Example 2:

**Input**: `word1 = "abceded", word2 = "baecfef"`

**Output**: `4`

**Explanation**:

Divide `word1` into `"ab"`, `"ce"`, and `"ded"`. The operations are:

- For the substring `"ab"`:
  - Perform operation of type 2 on `"ab"` -> `"ba"`.
- For the substring `"ce"`:
  - Perform operation of type 2 on `"ce"` -> `"ec"`.
- For the substring `"ded"`:
  - Perform operation of type 1 on `"ded"` -> `"fed"`.
  - Perform operation of type 1 on `"fed"` -> `"fef"`.

### Example 3:

**Input**: `word1 = "abcdef", word2 = "fedabc"`

**Output**: `2`

**Explanation**:

Divide `word1` into `"abcdef"`. The operations are:

- For the substring `"abcdef"`:
  - Perform operation of type 3 on `"abcdef"` -> `"fedcba"`.
  - Perform operation of type 2 on `"fedcba"` -> `"fedabc"`.

## Constraints

- `1 <= word1.length == word2.length <= 100`
- `word1` and `word2` consist only of lowercase English letters.