import numpy as np
import time

# Function to measure read latency
def measureReadLatency(arr):
    startTime = time.time()
    # Perform read operations across the array
    for i in range(len(arr)):
        i = arr[i]
    endTime = time.time()
    return (endTime - startTime) * 1e6  # Convert to microseconds

# Function to measure write latency
def measureWriteLatency(arr):
    startTime = time.time()
    # Perform write operations across the array
    for i in range(len(arr)):
        arr[i] = i
    endTime = time.time()
    return (endTime - startTime) * 1e6  # Convert to microseconds

# Test with different array sizes
def testLatency():
    sizes = [2**10, 2**15, 2**20, 2**25]  # Sizes in elements (Bytes depends on type)
    print(f"{'Size (Bytes)':<15} {'Read Latency (µs)':<20} {'Write Latency (µs)':<20}")
    
    for size in sizes:
        arr = np.zeros(size, dtype=np.int32)  # Use int32 (4 Bytes per element)
        arraySizeBytes = arr.nbytes
        
        # Measure read latency
        readLatency = measureReadLatency(arr)
        
        # Measure write latency
        writeLatency = measureWriteLatency(arr)
        
        print(f"{arraySizeBytes:<15} {readLatency:<20.2f} {writeLatency:<20.2f}")

if __name__ == "__main__":
    testLatency()