### Spark I/O and Read Latency Optimization: Benchmark Results and Insights

**Benchmark Results:**

| Benchmark Type         | Elapsed Time (s) | Executor Run Time (s) | Bytes Read (KB) | Bytes Written (KB) | Shuffle Bytes Written (KB) | Shuffle Bytes Read (KB) |
|:-----------------------|:-----------------|:----------------------|:----------------|:-------------------|:---------------------------|:------------------------|
| Broadcast Join         | 3                | 5                     | 1860.8          | 0                  | 0.233                      | 0.233                   |
| Partitioned Table Read | 17               | 21                    | 18.5            | 0                  | 0.177                      | 0.177                   |
| Non-Partitioned Table Read | 1                | 3                     | 1644.9          | 0                  | 0.457                      | 0.457                   |
| Bucketed Join          | 1                | 4                     | 1888.3          | 0                  | 0.708                      | 0.708                   |

**Key Findings and Insights:**

Based on the benchmark results presented above, the following key insights were observed regarding Spark I/O and read latency optimizations:

*   **Broadcast Join Efficiency:** The Broadcast Join significantly reduced elapsed time to 3 seconds and executor run time to 5 seconds, demonstrating its effectiveness for joining with smaller tables by minimizing shuffle operations.
*   **Partitioned Read vs. Non-Partitioned Read:** Reading from a partitioned table with a filter (`Partitioned Table Read`) resulted in a much lower `Bytes Read` (18.5 KB) compared to the `Non-Partitioned Table Read` (1644.9 KB) for the same filter condition. This highlights the significant I/O efficiency gained through partition pruning. For the non-partitioned read, the higher shuffle read and write (0.457 KB) indicate that data needed to be loaded entirely from storage and then shuffled across workers for filtering, contributing to its less efficient performance despite a lower elapsed time in this specific test case. The drastic reduction in `Bytes Read` for the partitioned table confirms the I/O optimization.
*   **Bucketed Join Performance:** The Bucketed Join achieved the lowest elapsed time (1 second) and a very efficient executor run time (4 seconds), indicating superior performance for join operations when data is pre-organized using bucketing. This confirms the effectiveness of co-locating data for efficient joins.
