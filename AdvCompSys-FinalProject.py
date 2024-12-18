import heapq

#rudimentary process class
class Process:
    def __init__(self, pid, arriveTime, burstTime):
        self.pid = pid
        self.arriveTime = arriveTime
        self.burstTime = burstTime
        self.remainingTime = burstTime
        self.completionTime = 0
        self.waitingTime = 0
        self.turnaroundTime = 0

    def __lt__(self, other):
        return self.burstTime < other.burstTime

def firstComeFirstServe(processList):
    #sorts the list by the arrival time
    processList.sort(key=lambda x: x.arriveTime)
    currentTime = 0
    #iterates through the list of processes, advancing time as it does so
    for p in processList:
        #checks if the current time is less than the arrival time, setting the former equal to the later if true
        if (currentTime < p.arriveTime):
            currentTime = p.arriveTime
        p.completionTime = currentTime + p.burstTime
        currentTime = p.completionTime
        p.turnaroundTime = p.completionTime - p.arriveTime
        p.waitingTime = p.turnaroundTime - p.burstTime

def shortestJobNext(processes):
    #copies and sorts the processes by their arrival time
    processes_copy = sorted(processes, key=lambda x: x.arriveTime)
    ready_queue = []
    currentTime = 0

    while processes_copy or ready_queue:
        #adds all the processes that have arrived by the current time to the ready queue
        while processes_copy and processes_copy[0].arriveTime <= currentTime:
            heapq.heappush(ready_queue, processes_copy.pop(0))

        if (ready_queue):
            #executes the shortest job in the ready queue
            p = heapq.heappop(ready_queue)
            currentTime = max(currentTime, p.arriveTime) + p.burstTime
            p.completionTime = currentTime
            p.turnaroundTime = p.completionTime - p.arriveTime
            p.waitingTime = p.turnaroundTime - p.burstTime
        else:
            #if there is no process is ready, it advances time to the next arrival
            currentTime = processes_copy[0].arriveTime

# function to perform round robin algorithm
def roundRobin(processList, timeQuantum):
    readyQueue = []
    currentTime = 0
    processList.sort(key=lambda x: x.arriveTime)
    processesLeft = len(processList)
    # iterates through every process
    while processesLeft > 0:
        #iterates through processList and adds non-expired processes to a queue
        for p in processList:
            if (p.arriveTime <= currentTime and p.remainingTime > 0):
                readyQueue.append(p)
        #checks if there are processes that still need to be run
        if (readyQueue):
            p = readyQueue.pop(0)
            #checks if the remaining time is less than quantum time and advances current time
            if (p.remainingTime > timeQuantum):
                currentTime += timeQuantum
                p.remainingTime -= timeQuantum
            #advances time and sets remaining time to 0, sets values of other time variables
            else:
                currentTime += p.remainingTime
                p.remainingTime = 0
                p.completionTime = currentTime
                p.turnaroundTime = p.completionTime - p.arriveTime
                p.waitingTime = p.turnaroundTime - p.burstTime
                processesLeft -= 1
        else:
            currentTime += 1


#prints all the member variables of each process in a list of processes
def displayResults(processList):
    print(f"{'PID':<10}{'Arrival':<10}{'Burst':<10}{'Completion':<15}{'Turnaround':<15}{'Waiting':<10}")
    for p in processList:
        print(f"{p.pid:<10}{p.arriveTime:<10}{p.burstTime:<10}"
              f"{p.completionTime:<15}{p.turnaroundTime:<15}{p.waitingTime:<10}")

#main code
if __name__ == "__main__":
    processList = [Process(1, 0, 8), Process(2, 1, 4), Process(3, 2, 9), Process(4, 3, 5), Process(5, 2, 6), Process(6, 9, 7)]
    print("Choose CPU Scheduling Algorithm:")
    print("1. First-Come-First-Serve (FCFS)")
    print("2. Shortest Job Next (SJN)")
    print("3. Round Robin (RR)")
    choice = int(input("Enter your choice: "))
    
    if (choice == 1):
        firstComeFirstServe(processList)
        print("\n--- FCFS Results ---")
        displayResults(processList)
    elif (choice == 2):
        shortestJobNext(processList)
        print("\n--- SJN Results ---")
        displayResults(processList)
    elif (choice == 3):
        timeQuantum = int(input("Enter the time quantum: "))
        roundRobin(processList, timeQuantum)
        print("\n--- Round Robin Results ---")
        displayResults(processList)

    