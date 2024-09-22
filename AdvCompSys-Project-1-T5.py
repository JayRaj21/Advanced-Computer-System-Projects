import numpy as np
import time

# Function to simulate light computation (multiplication) with different stride sizes
def measureExecutionTimeWithStride(arr, stride):
    startTime = time.time()

    # Access elements with the given stride and perform a simple multiplication
    result = 0
    for i in range(0, len(arr), stride):
        result += arr[i] * 2

    endTime = time.time()
    return (endTime - startTime) * 1e6  # Return time in microseconds

# Test function to simulate the impact of TLB miss ratio
def testTlbMissImpact():
    sizes = [2**10, 2**15, 2**20, 2**25]  # Array sizes in elements
    strides = [1, 16, 64, 256, 1024]  # Different stride sizes to increase the likelihood of TLB misses

    print(f"{'Array Size (Bytes)':<20} {'Stride Size':<15} {'Execution Time (µs)':<25}")
    
    for size in sizes:
        arr = np.ones(size, dtype=np.int32)  # Create an array of int32
        arraySizeBytes = arr.nbytes
        
        for stride in strides:
            # Measure execution time with different strides
            exec_time = measureExecutionTimeWithStride(arr, stride)
            
            # Print the results
            print(f"{arraySizeBytes:<20} {stride:<15} {exec_time:<25.2f}")

if __name__ == "__main__":
    testTlbMissImpact()
