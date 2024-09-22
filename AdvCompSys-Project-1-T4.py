import numpy as np
import time

# Function to measure execution time for simple computation (multiplication)
def measureExecutionTime(arr):
    startTime = time.time()
    
    # Perform element-wise multiplication (light computation)
    result = arr * 2
    
    endTime = time.time()
    return (endTime - startTime) * 1e6  # Return time in microseconds

# Test function to simulate impact of cache miss ratio on performance
def testCacheMissImpact():
    sizes = [2**10, 2**15, 2**20, 2**25]  # Array sizes in elements
    dTypeSize = 4  # Each int32 element is 4 bytes

    print(f"{'Array Size (Bytes)':<20} {'Execution Time (µs)':<25}")
    
    for size in sizes:
        arr = np.ones(size, dtype=np.int32)  # Create an array of int32
        arraySizeBytes = arr.nbytes
        
        # Measure execution time of the computation (simulating light work)
        execTime = measureExecutionTime(arr)
        
        # Print the results
        print(f"{arraySizeBytes:<20} {execTime:<25.2f}")

if __name__ == "__main__":
    testCacheMissImpact()
