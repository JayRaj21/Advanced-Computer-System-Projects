import numpy as np
import time

# Function to measure memory bandwidth for read operations
def measurReadBandwidth(arr, numAccesses):
    startTime = time.time()
    # Perform read operations over the array multiple times
    for i in range(numAccesses):
        i = arr[:]
    endTime = time.time()
    elapsedTime = endTime - startTime
    dataSizeBytes = arr.nbytes * numAccesses
    bandwidth = dataSizeBytes / elapsedTime / (1024 ** 3)  # Convert to GB/s
    return bandwidth

# Function to measure memory bandwidth for write operations
def measureWriteBandwidth(arr, numAccesses):
    startTime = time.time()
    # Perform write operations over the array multiple times
    for i in range(numAccesses):
        arr[:] = np.random.randint(0, 100, size=len(arr))  # Writing random data
    endTime = time.time()
    elapsedTime = endTime - startTime
    dataSizeBytes = arr.nbytes * numAccesses
    bandwidth = dataSizeBytes / elapsedTime / (1024 ** 3)  # Convert to GB/s
    return bandwidth

# Function to test bandwidth under different conditions
def testBandwidth(granularity, readWriteRatio, numAccesses):
    sizeMap = {64: 64 // 4, 256: 256 // 4, 1024: 1024 // 4}  # Elements in int32 for 64B, 256B, 1024B
    arr = np.zeros(sizeMap[granularity], dtype=np.int32)
    
    readFraction = readWriteRatio[0] / 100
    writeFraction = readWriteRatio[1] / 100
    readBandwidth = 0
    writeBandwidth = 0
    
    # Measure read bandwidth
    if readFraction > 0:
        readBandwidth = measurReadBandwidth(arr, int(numAccesses * readFraction))
    
    # Measure write bandwidth
    if writeFraction > 0:
        writeBandwidth = measureWriteBandwidth(arr, int(numAccesses * writeFraction))
    
    return readBandwidth, writeBandwidth

# Test different granularities and read/write ratios
def main():
    granularities = [64, 256, 1024]  # Access sizes in bytes
    readWriteRatios = [(100, 0), (0, 100), (70, 30), (50, 50)]  # Read:Write ratios
    numAccesses = 10000  # Number of read/write accesses to perform
    
    print(f"{'Granularity (Bytes)':<20} {'Read:Write Ratio':<20} {'Read Bandwidth (GB/s)':<25} {'Write Bandwidth (GB/s)':<25}")
    
    for granularity in granularities:
        for ratio in readWriteRatios:
            read_bw, write_bw = testBandwidth(granularity, ratio, numAccesses)
            print(f"{granularity:<20} {f'{ratio[0]}:{ratio[1]}':<20} {read_bw:<25.2f} {write_bw:<25.2f}")

if __name__ == "__main__":
    main()
