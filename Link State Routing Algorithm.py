# Yash Malik
# 2001CS79
# Tutorial-5 CS359


import fileinput # to take input from files
import threading # using threads in our program
import time # to call sleep function
import heapq
from tabulate import tabulate # to give well formatted tables in output


inputs = [] # List that stores each line of file as input
routername = {} # Dictionary to convert routerindex to routername
routerindex = {} # Dictionary to convert routerindex to routername
routers = [] # List of new thread created for each router
LinkStateTable = [] # Routing Table to be printed
InputGraph = []
CurrentGraph = [] # Graph of network formed for each router
AdjacencyList = []
UpdatedDistance = [] # Distances that were updated
IterationCount = [] # maintains the 

INF = int(1e9) # Infinite Distance
NumRouters = 0 # Number of Routers in the network
    
lock = threading.Lock() # mutex lock

# Taking inputs From File
def TakeinputsFromFile():
    temp = []
    for line in fileinput.input(files = 'topology.txt'):
        temp = line.split() # Taking each line of the file as input
        inputs.append(temp) # Adding each line into the inputs array
    i = 0
    global NumRouters
    NumRouters = int(inputs[0][0])
    for name in inputs[1]:
        routername[i] = name # mapping router index to router names
        routerindex[name] = i # mapping router name to router index
        i += 1

    for i in range(NumRouters): # Resizing all the lists
        InputGraph.append([])
        UpdatedDistance.append([])
        LinkStateTable.append([])
        AdjacencyList.append([])
        CurrentGraph.append([])
        IterationCount.append(0)

    for i in range(2, len(inputs)): # Updating the InputGraph List
        if inputs[i][0] == "EOF":
            break
        router1 = int(routerindex[inputs[i][0]])
        router2 = int(routerindex[inputs[i][1]])
        Weight = int(inputs[i][2])
        InputGraph[router1].append([router2, Weight])
        InputGraph[router2].append([router1, Weight])

# Creating a thread for each router    
def CreateRouter():
    for i in range(NumRouters):
       thread = threading.Thread(target = StartRouterProcess, args = (i,))
       routers.append(thread)
       routers[i].start()
    for router in routers:
        router.join()

# Initialise the routing table for each router
def CreateLinkStateTable(routernumber):
    for i in range(NumRouters): # Initialising to INF distance 
        LinkStateTable[routernumber].append(INF)
        
    LinkStateTable[routernumber][routernumber] = 0 # Distance from A->A = 0
    
    # Adding all the InputGraph to the Routing Table
    for neighbour in InputGraph[routernumber]:
        CurrentGraph[routernumber].append([routernumber, neighbour[0], neighbour[1]])


# Prints the Current Version of the Routing Table of
def PrintLinkStateTable(routernumber):
    # lock.acquire() # mutex lock needed to print
    rname = routername[routernumber]
    ic = IterationCount[routernumber]
    print("\n***************************************************************\n")
    print("Updating Routing Table of Router " + rname+".")
    print("Routing Table for router " + rname + ":\n")
    print("Iteration Count: " + str(ic))
    # Creating the Table to be output
    output=[["Router Name", "Distance from router " + rname, "Next Router"]]
    for i in range(NumRouters):
        temp = []
        Dis = LinkStateTable[routernumber][i] # Distance to node i
        a = routername[i] + ("*" if i in UpdatedDistance[routernumber] else "") # if updated add *
        b = (str(Dis) if Dis != INF else "INF") # if distance = Infinity i.e. node not reachable
        temp.append(a) 
        temp.append(b) 
        output.append(temp)
    print(tabulate(output, headers = "firstrow", tablefmt = "fancy_outline", stralign="center", numalign="center"))    
    UpdatedDistance[routernumber].clear()
    # lock.release()
    
# Sends Distance Vector to all the neighbouring routers
def SendingPackets(routernumber):
    time.sleep(2)   # Send after every 2 seconds
    for router in range(NumRouters):
        if router == routernumber:
            continue  
        lock.acquire() # lock acquired to print
        print("\n***************************************************************\n")
        print("Routing Table send from Router "+routername[routernumber]+" to Router " + routername[router])
        lock.release() # release the lock
        lock.acquire()
        IterationCount[router] += 1
        UpdateLinkStateTable(routernumber, router)
        lock.release() # release the lock

        
def UpdateLinkStateTable(sender, receiver):
    for edge in CurrentGraph[sender]:
        if edge not in CurrentGraph[receiver]:
            CurrentGraph[receiver].append(edge)
    for router in range(NumRouters):
        AdjacencyList[router].clear()
        
    for edge in CurrentGraph[receiver]:
        if [edge[1], edge[2]] not in AdjacencyList[edge[0]]:
                AdjacencyList[edge[0]].append([edge[1],edge[2]])
        if [edge[0], edge[2]] not in AdjacencyList[edge[1]]:
                AdjacencyList[edge[1]].append([edge[0],edge[2]])
    dijkstra(receiver)
    PrintLinkStateTable(receiver)

def dijkstra(routernumber):
    temp = LinkStateTable[routernumber].copy()
    LinkStateTable[routernumber].clear()
    for i in range(NumRouters): # Initialising to INF distance 
        LinkStateTable[routernumber].append(INF)
        
    LinkStateTable[routernumber][routernumber] = 0 # Distance from A->A = 0
    pq = [(0,routernumber)]
    heapq.heapify(pq)
    while len(pq) > 0 :
        v = heapq.heappop(pq)
        if v[0] != LinkStateTable[routernumber][v[1]]:
            continue
        for edge in AdjacencyList[v[1]]:
            if (v[0] + edge[1]) < LinkStateTable[routernumber][edge[0]]:
                dis = v[0] + edge[1]
                LinkStateTable[routernumber][edge[0]] = dis
                heapq.heappush(pq, (dis,edge[0]))
    for i in range(NumRouters):
        if LinkStateTable[routernumber][i] != temp[i]:
            UpdatedDistance[routernumber].append(i)


def StartRouterProcess(routernumber):
    CreateLinkStateTable(routernumber) # Initialise the Routing Table
    lock.acquire()
    PrintLinkStateTable(routernumber) # Print the Routing Table
    lock.release()
    SendingPackets(routernumber) # Send the Link State Table to all routers


def main():
    TakeinputsFromFile()
    print("")
    CreateRouter()
    print("\n***************************************************************\n")
    

if __name__ == "__main__":
    main()