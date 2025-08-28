# Benchmark Results and Insights

This document contains the results and insights from the benchmarks run in this research environment.

## Shuffle Compression Benchmark

| Metric                  | Shuffle Disabled | Shuffle Enabled | Change      |
| ----------------------- | ---------------- | --------------- | ----------- |
| **Total Time (s)**      | 7.15             | 6.98            | **-2.4%**   |
| **Simple Shuffle (s)**  | 1.35             | 1.26            | **-6.7%**   |
| **Complex Shuffle (s)** | 0.89             | 1.03            | +15.7%      |
| **Shuffle Overhead**    | 31.3%            | 32.8%           | +1.5%       |
| **I/O Overhead**        | 39.9%            | 41.6%           | +1.7%       |

**Insights:**

- **Overall Performance**: Enabling shuffle compression resulted in a **2.4% improvement** in the total execution time of this benchmark.
- **Impact on Shuffle Operations**:
    - For the **simple shuffle** operation, performance was actually **6.7% faster** with compression enabled. This is a positive change, indicating that for this specific simple shuffle, the benefits of reduced data size outweighed the compression/decompression overhead.
    - For the **complex shuffle** operation, performance was **15.7% slower** with compression. This suggests that for more complex shuffles, the overhead of compression/decompression might be more significant or the data might not be as compressible, leading to a performance degradation.
- **I/O Performance**: The I/O overhead increased by 1.7% with shuffle compression enabled. This is unexpected and might indicate that the compression/decompression process itself is contributing to the I/O time, or that the data being written/read is not highly compressible, leading to less benefit from reduced data size.

**Conclusion:**

For this specific benchmark, enabling shuffle compression resulted in a modest overall performance improvement. However, the impact on individual shuffle operations varied, with simple shuffles improving and complex shuffles degrading. The increase in I/O overhead is also an area for further investigation. This highlights that the benefits of shuffle compression are highly dependent on the nature of the data and the complexity of the shuffle operations.

### I/O Compression Codec Benchmark

| Metric             | Snappy | Gzip   | Zstd   |
| ------------------ | ------ | ------ | ------ |
| **Total Time (s)** | 7.08   | 7.13   | 7.09   |
| **File Write (s)** | 2.12   | 2.14   | 2.27   |
| **File Read (s)**  | 0.66   | 0.61   | 0.67   |
| **I/O Overhead**   | 39.3%  | 38.7%  | 41.5%  |

**Insights:**

- **Total Time:** The total time for all three benchmarks is very similar, with `Snappy` being slightly faster. However, the differences are very small and likely within the margin of error for this small benchmark.
- **File Write:** `Snappy` was the fastest for writing Parquet files, followed by `Gzip` and then `Zstd`.
- **File Read:** `Gzip` was the fastest for reading Parquet files, followed by `Snappy` and then `Zstd`.
- **I/O Overhead:** `Gzip` had the lowest I/O overhead, followed by `Snappy` and then `Zstd`.

**Conclusion:**

For this particular benchmark, `Gzip` appears to be the best-performing compression codec in terms of I/O overhead and read times, while `Snappy` is slightly faster for writes. `Zstd` performed slightly worse in this specific scenario. However, it's important to note that the differences are small. For a real-world workload with a much larger dataset, the differences in performance between the codecs would likely be more pronounced.

In general:

- **Snappy:** Offers a good balance between compression ratio and performance. It's often the default choice for Parquet files.
- **Gzip:** Provides a higher compression ratio than Snappy, but at the cost of higher CPU usage and slower performance.
- **Zstd:** A modern compression algorithm that often provides better compression ratios than Snappy and faster performance than Gzip. It's a good all-around choice.