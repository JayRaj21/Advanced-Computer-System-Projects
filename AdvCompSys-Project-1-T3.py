import numpy as np
import time

# Function to measure read latency and throughput for a given array size
def measureLatencyAndThroughput(arr, numAccesses):
    startTime = time.time()

    # Perform read operations on the array to simulate load
    for i in range(numAccesses):
        i = arr[:]

    end_time = time.time()
    elapsedTime = end_time - startTime
    
    # Calculate latency and throughput
    latencyPerAccess = elapsedTime / numAccesses  # Time per access
    totalDataAccessed = arr.nbytes * numAccesses   # Total data accessed in bytes
    throughput = totalDataAccessed / elapsedTime / (1024 ** 3)  # Convert to GB/s
    
    return latencyPerAccess * 1e6, throughput  # Latency in microseconds, throughput in GB/s

# Test function to simulate increasing memory load
def testLatencyVsThroughput():
    sizes = [2**10, 2**15, 2**20, 2**25]  # Array sizes in elements (bytes based on dtype)
    numAccesses = 1000  # Number of times each array is accessed
    dTypeSize = 4  # For int32 (4 bytes per element)

    print(f"{'Array Size (Bytes)':<20} {'Latency per Access (µs)':<30} {'Throughput (GB/s)':<25}")

    for size in sizes:
        arr = np.zeros(size, dtype=np.int32)  # Creating array of int32
        arraySizeBytes = arr.nbytes
        
        # Measure latency and throughput
        latency, throughput = measureLatencyAndThroughput(arr, numAccesses)
        
        # Print results
        print(f"{arraySizeBytes:<20} {latency:<30.2f} {throughput:<25.2f}")

if __name__ == "__main__":
    testLatencyVsThroughput()
