from time import perf_counter
from threading import Thread, Lock
import zlib

"""
Your implementation should support the following operations:
(1) Put(key, value): Inserts or updates a key-value pair
(2) Get(key): Retrieves the value associated with a given key
(3) Delete(key): Removes a key-value pair from the store
(4) Support for multiple concurrent read and write operations
(5) Optional (as a bonus): Support lossless in-memory data compression at small speed performance loss

You should also write a testbench to test your in-memory key-value store under
(1) different operational concurrency (one user, two users, 4 users, …),
(2) different number of internal working threads (4, 8, 16, …), 
(3) Different read vs. write ratio, and... 
(4) Different value size (8B, 64B, 256B) (you may keep the key size as 8B).

Number of iterations: numUsers*numThreadsPerUser*readWriteRatio*valueSize*8B
"""

encodeMap = dict()
myLock = Lock()
encList = list()

test = [b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12"]

smallData = [b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes"]          

mediumData = [b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes"]

largeData = [b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes",
             b"honda123", b"chevy123", b"toyota12", b"honda123", b"toyota12", b"ford1234", b"chevy123", b"mercedes"]

def dictEncode(data, compressFlag):
    global encodeMap
    global myLock
    global encList
    myLock.acquire()
    counter = len(encodeMap.keys()) + 1
    for i in range(len(data)):
        if (compressFlag):
            if zlib.compress(data[i]) in encodeMap.values():
                tempIndex = (list(encodeMap.values())).index(zlib.compress(data[i]))
                encList.append(list(encodeMap.keys())[tempIndex])
            else:
                encodeMap[counter] = zlib.compress(data[i])
                encList.append(counter)
                counter += 1
        else:
            if data[i] in encodeMap.values():
                tempIndex = (list(encodeMap.values())).index(data[i])
                encList.append(list(encodeMap.keys())[tempIndex])
            else:
                encodeMap[counter] = data[i]
                encList.append(counter)
                counter += 1
    myLock.release()
    return

def dictDecode(data, compressFlag):
    global encodeMap
    global myLock
    decodeList = list()
    myLock.acquire()
    for i in range(len(data)):
        if (compressFlag):
            decodeList.append(zlib.decompress(encodeMap[data[i]]))
        else:
            decodeList.append(encodeMap[data[i]])
    myLock.release()
    #print(f"Decoded Length: {len(decodeList)}")
    #print(f"Decoded Value: {decodeList}\n")
    return

def SingleUsers(data, maxThreads):
    threadList = list()
    for i in range(1,maxThreads+1):
        thread = Thread(target=executeSingleUser, args=(data, ))
        threadList.append(thread)

    startTime = perf_counter()
    for thrd in threadList:
        thrd.start()

    for thred in threadList:
        thred.join()
    
    dictDecode(encList, 0)
    #print(f"Mapping: {encodeMap}\n")

    endTime = perf_counter()
    return f"{endTime - startTime}"

def TwoUsers(data, maxThreads):
    print(f"***Starting Two User Test***")
    userList = list()
    for i in range(1,3):
        thread = Thread(target=SingleUsers, args=(data, maxThreads))
        userList.append(thread)

    startTime = perf_counter()
   
    for thrd in userList:
        thrd.start()
    
    for thred in userList:
        thred.join()

    endTime = perf_counter()
    return f"{endTime - startTime}"

def FourUsers(data, maxThreads):
    print(f"***Four Single User Test***")
    userList = list()
    for i in range(1,5):
        thread = Thread(target=SingleUsers, args=(data, maxThreads))
        userList.append(thread)

    startTime = perf_counter()
    
    for thrd in userList:
        thrd.start()
    
    for thred in userList:
        thred.join()
    endTime = perf_counter()
    return f"{endTime - startTime}"

def executeSingleUser(data):
    dictEncode(data, 0)
    #print(f"Encoded Length:{len(encList)}\n")
    #print(f"Encoded Values:{encList}\n")
    return

def EqualReadWrite(data):
    print("***Start equal read/write ratio test***\n")
    threadList = list()
    for i in range(1,2):
        thread = Thread(target=executeSingleUser, args=(data, ))
        threadList.append(thread)
        thread = Thread(target=dictDecode, args=(encList, 0))
        threadList.append(thread)

    startTime = perf_counter()
    for thrd in threadList:
        thrd.start()

    for thred in threadList:
        thred.join()
    
    #print(f"Mapping: {encodeMap}\n")
    endTime = perf_counter()
    return f"{endTime - startTime}"

def TwoReadsOneWrite(data):
    print("***Start 2R/1W test***\n")
    threadList = list()
    for i in range(1,2):
        thread = Thread(target=executeSingleUser, args=(data, ))
        threadList.append(thread)
        thread = Thread(target=dictDecode, args=(encList, 0))
        threadList.append(thread)
        thread = Thread(target=dictDecode, args=(encList, 0))
        threadList.append(thread)

    startTime = perf_counter()
    for thrd in threadList:
        thrd.start()

    for thred in threadList:
        thred.join()
    
    #print(f"Mapping: {encodeMap}\n")
    endTime = perf_counter()
    return f"{endTime - startTime}"

def OneReadTwoWrites(data):
    print("***Start 1R/2W test***\n")
    threadList = list()
    for i in range(1,2):
        thread = Thread(target=executeSingleUser, args=(data, ))
        threadList.append(thread)
        thread = Thread(target=executeSingleUser, args=(data, ))
        threadList.append(thread)
        thread = Thread(target=dictDecode, args=(encList, 0))
        threadList.append(thread)

    startTime = perf_counter()
    for thrd in threadList:
        thrd.start()

    for thred in threadList:
        thred.join()
    
    #print(f"Mapping: {encodeMap}\n")
    endTime = perf_counter()
    return f"{endTime - startTime}"

def prefixScan(encodedData, text):
    print("*** Starting Prefix Scan ***")
    global encodeMap
    foundValues = list()
    startTime = perf_counter()
    for elem in encodedData:
        if ((encodeMap[elem].decode("utf-8")).startswith(text)):
            foundValues.append(encodeMap[elem].decode("utf-8"))
        else:
            continue

    endTime = perf_counter()
    if (len(foundValues) > 0):
        print(f"Found Values: {foundValues}")
    else:
        print(f"No prefix instances of \"{text}\" are present")
        
    return f"{endTime - startTime}"
        

if __name__ == "__main__":
    #Time values will vary since they are not consistent when redoing tests
    print()
    # 1. Internal threads test
    # print(SingleUsers(smallData, 4))
    # print(SingleUsers(smallData, 8))
    # print(SingleUsers(smallData, 16))

    # 2. User test
    # print(SingleUsers(smallData, 1))
    # print(TwoUsers(smallData, 1))
    # print(FourUsers(smallData, 1))
   
    # 3. Read/Write Tests -> Only test one line at a time, otherwise it breaks
    # print(EqualReadWrite(smallData))
    # print(TwoReadsOneWrite(smallData))
    # print(OneReadTwoWrites(smallData))
    
    # 4. Data Size Test
    # print(SingleUsers(smallData, 1))
    # print(SingleUsers(mediumData, 1))
    # print(SingleUsers(largeData, 1))

    # 5. Prefix Scan Test
    # dictEncode(mediumData, 0)
    # time = prefixScan(encList, "toy")
    # print(time)
    # print()
    # time = prefixScan(encList, "or")
    # print(time)

    # 6. Data Compression test
    # startTime = perf_counter()
    # dictEncode(smallData, 1)
    # print(encList)
    # dictDecode(encList, 1)
    # endTime = perf_counter()
    # print(endTime-startTime)
    
    # startTime = perf_counter()
    # dictEncode(smallData, 0)
    # #print(encList)
    # dictDecode(encList, 0)
    # endTime = perf_counter()
    # print(endTime-startTime)
    # print(encodeMap)

    # Internal Threads Times
    #  4 threads --> 0.0005763880035374314
    #  8 threads --> 0.000879093015100807
    # 16 threads --> 0.0012480900040827692 

    # User Times
    # 1 Users --> 0.00022179502411745489
    # 2 Users --> 0.00035875398316420615
    # 4 Users --> 0.0004780120216310024

    # Read/Write Times
    # Equal r/w --> 0.00028044500504620373
    # 2R/1W ------> 0.00048807798884809017
    # 1R/2W ------> 0.0004117719945497811 

    # Data Size Times
    # 0.00013885300722904503
    # 0.00012462001177482307
    # 0.0001767530047800392

    # Prefix Scan Times
    # Prefix Exists --------> 1.6236997907981277e-05
    # Prefix Doesnt exist --> 9.587995009496808e-06

    # Data Compression Times
    # With compression -----> 0.0006870539800729603
    # Without compression --> 1.235899981111288e-05
    