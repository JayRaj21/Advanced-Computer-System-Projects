# Advanced-Computer-System-Projects

## Brief Description of Each Project:
Project 1: Testing the various properties related to caching and memory hierarchy.

## Project 1 Experiment 1

### Execution
I accessed data from progressively larger arrays (representing different levels of the cache hierarchy). Smaller arrays fit within the L1 cache, and read/write operations were extremely fast. Larger arrays (e.g., 1MB, 10MB) progressively moved data to the L2, L3 cache, and ultimately to main memory, which resulted in increased latency. Read and write latencies were measured for each case to show how memory access times increase as data size surpasses cache capacity.

### Results
Reads/writes within the L1 cache were very fast (in nanoseconds), but latency increased as the array size exceeded L1 and L2 cache capacities. Also, as soon as the array size exceeded the total cache capacity, memory accesses were much slower due to main memory being accessed. Latency in main memory was significantly higher, reflecting the slower speed of DRAM compared to cache.

## Project 1 Experiment 2

### Execution
The program varied the data access granularity (64B, 256B, 1024B) and tested read-only, write-only, and mixed read/write intensity ratios. By measuring the total time to complete memory operations, it is possible to calculate the effective memory bandwidth for each combination of access granularity and read/write ratio.

### Results
Data access with larger granularity (e.g., 1024B) resulted in higher bandwidth utilization. This is because accessing larger chunks of data at once reduces the number of memory transactions, allowing for more efficient use of memory bandwidth. Additionally, write-only operations had lower bandwidth utilization compared to read-only or mixed operations due to additional overhead (e.g., write-back policies). Mixed workloads (70:30 and 50:50) generally balanced the bandwidth demands.

## Project 1 Experiment 3

### Execution
The experiment progressively increased the number of memory accesses on arrays of varying sizes, simulating high load scenarios. Latency per access and throughput were measured to observe the queuing effect—where increased memory load causes requests to pile up, leading to longer latencies.

### Results
With a small number of memory accesses, latency was low, and throughput was high as there was minimal contention for memory. Also, as the memory load increased (more requests), latency per memory access increased due to queuing. Throughput initially increased, but at higher loads, it plateaued or even decreased as memory contention grew, reflecting the limitations predicted by queuing theory.

## Project 1 Experiment 4

### Execution
Arrays of different sizes were used to simulate varying cache miss ratios. Arrays small enough to fit within the cache resulted in low miss ratios, while larger arrays caused higher miss ratios due to cache evictions. Execution time of a simple multiplication (light computation) was measured across different array sizes to quantify the performance impact of cache misses.

### Results
When the entire array fit in cache, cache misses were minimal, and execution times were low, as memory access was fast. Additionally, as the array size increased beyond the cache size, cache misses occurred more frequently, and execution times increased substantially. This is because the CPU had to access slower main memory for the data.

## Project 1 Experiment 5

### Execution
The program used arrays of different sizes and accessed memory using various strides to simulate different TLB miss ratios. Smaller strides result in more contiguous memory access, while larger strides cause non-contiguous access, increasing the likelihood of TLB misses. Execution times were measured for each stride and array size to demonstrate the effect of TLB misses on software performance.

### Results
When using small strides, memory accesses were mostly contiguous, resulting in fewer TLB misses. Performance was good, as there was minimal TLB-related overhead. Also, as the stride size increased, TLB misses became more frequent, and execution time increased significantly. This is because accessing non-contiguous memory pages forced the CPU to perform more page table lookups, adding latency.

## Project 1 Conclusion
The experiments demonstrated the critical role that cache and memory hierarchy play in software performance. Caches significantly reduce memory latency for frequently accessed, small data sets, but as data size increases, both cache and TLB misses introduce considerable performance penalties. The trade-off between memory throughput and latency became evident, as increasing memory load led to queuing effects, where throughput eventually plateaued and latency grew due to memory contention. TLB and cache misses were found to have substantial impacts on performance, especially for large data sets or when memory access patterns were irregular. The experiments highlighted that optimizing for contiguous memory access, keeping working sets small enough to fit within cache, and balancing read/write operations to maximize memory bandwidth are all effective strategies for improving software performance. Overall, the findings underscore the importance of understanding memory hierarchy when designing high-performance applications, as minimizing memory-related overhead is crucial for efficiency in modern computing systems.

## Project 2

### Execution


### Results
The performance analysis of this matrix-matrix multiplication code highlights the impact of three key optimization techniques: multi-threading, SIMD (Single Instruction Multiple Data) instructions, and cache blocking. Multi-threading significantly improves computation speed by distributing the workload across multiple CPU cores. As the matrix size increases, the benefit of multi-threading becomes more evident, particularly when using multiple threads to handle the multiplication. However, there is a point where increasing the number of threads is actually less efficient, especially when the thread count exceeds the number of physical CPU cores, and overhead begins to impact performance.

SIMD instructions provide another layer of optimization by exploiting data-level parallelism. SIMD allows multiple matrix elements to be processed simultaneously, which results in faster computation, particularly for large matrices. The benefit of SIMD is most obvious when working with dense data sets, as it efficiently handles operations on blocks of data. However, for smaller matrices, the overhead of setting up SIMD operations may not justify the performance gains.

Cache blocking addresses memory access patterns by improving cache efficiency. For large matrices that exceed the CPU's on-chip cache capacity, cache misses can significantly slow down performance. Blocking mitigates this issue by dividing the matrices into smaller sub-blocks that fit into the cache, reducing cache misses and improving the overall speed. This optimization is especially beneficial when handling very large matrices, where cache bottlenecks would otherwise hinder performance.

When these optimizations—multi-threading, SIMD, and cache blocking—are combined, they provide the greatest performance improvements. Together, they leverage CPU cores more effectively, exploit parallelism at the data level, and minimize cache misses, resulting in substantial speedups for large matrix sizes. The program allows users to experiment with different configurations of matrix size, number of threads, and optimization techniques, providing insights into the impact of each method on execution time and overall efficiency.

### Conclusion
From the results of the matrix-matrix multiplication implementation, several key conclusions can be drawn about the impact of optimization techniques on performance. First, multi-threading is highly effective in reducing execution time for large matrices by distributing the workload across multiple CPU cores. However, the performance gains from multi-threading plateau as the number of threads approaches or exceeds the number of available physical cores, due to overhead and thread contention. SIMD optimization further accelerates the computation by enabling simultaneous processing of multiple data elements, making it particularly valuable for dense matrices. However, the benefit of SIMD diminishes for smaller matrices where setup costs outweigh the advantages. Cache blocking proves to be crucial in maintaining high performance for large matrices by improving cache utilization and reducing the penalty from cache misses, especially when the matrices are too large to fit in the CPU's cache.

When combined, these three optimization techniques: multi-threading, SIMD, and cache blocking, provide the greatest overall performance boost. Their synergistic effect allows for efficient use of computational resources, minimizing bottlenecks related to memory access and maximizing throughput. These findings show the importance of considering both hardware capabilities (i.e core count and cache size) and data characteristics (i.e. size and sparsity) when optimizing algorithms for high-performance computing tasks.

## Any resources used in the projects will be state below:
* ChatGPT
* VSCode
* Numpy
* OpenMP
* SIMD Intrinsincs (AVX)
