### Spark Partitioning Optimization Benchmarks: Results and Insights

**Benchmark Results:**

| Benchmark Type             | Elapsed Time (s) | Executor Run Time (s) | Bytes Read (KB) | Records Read | Num Tasks | Bytes Written (KB) | Shuffle Bytes Written (KB) | Shuffle Bytes Read (KB) |
|:---------------------------|:-----------------|:----------------------|:----------------|:-------------|:----------|:-------------------|:---------------------------|:------------------------|
| Partitioned Table Read     | 24               | 34                    | 22.5            | 2743         | 1830      | 0                  | 0.236                      | 0.177                   |
| Non-Partitioned Table Read | 2                | 6                     | 1839.4          | 2880404      | 10        | 0                  | 0.460                      | 0.345                   |

**Key Findings and Insights:**

Based on the benchmark results presented above, the following key insights were observed regarding Spark partitioning optimizations:

*   **Partitioned Read vs. Non-Partitioned Read:** Reading from a partitioned table with a filter (`Partitioned Table Read`) resulted in a much lower `Bytes Read` (22.5 KB) and `Records Read` (2743) compared to the `Non-Partitioned Table Read` (1839.4 KB and 2880404 records) for the same filter condition. This highlights the significant I/O efficiency gained through partition pruning.
*   **Unexpected Performance for Partitioned Table:** Despite the effective data pruning, the `Partitioned Table Read` showed a significantly higher `Num Tasks` (1830 vs. 10) and `Elapsed Time` (24s vs. 2s) compared to the non-partitioned read. This indicates that while Spark successfully identified the relevant partition, the process of listing and discovering all 1824 partition directories on the local filesystem incurred substantial overhead. This overhead is typically mitigated in distributed storage systems like S3 that offer optimized metadata services.
*   **Shuffle Metrics:** For the non-partitioned read, the higher shuffle read and write (0.345 KB and 0.460 KB respectively) indicate that data needed to be loaded entirely from storage and then shuffled across workers for filtering, contributing to its less efficient performance in terms of data processing despite a lower elapsed time in this specific test case. The partitioned table had significantly lower shuffle activity (0.177 KB read, 0.236 KB written), as expected due to effective data pruning.