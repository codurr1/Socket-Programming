# Yash Malik
# 2001CS79
# Tutorial-3 CS359


# Python version - 3.10.6

# Install libraries (pip install):
# fileinput
# threading
# time
# tabulate 


import fileinput # to take input from files
import threading # using threads in our program
import time # to call sleep function
from tabulate import tabulate # to give well formatted tables in output

inputs = [] # List that stores each line of file as input
routername = {} # Dictionary to convert routerindex to routername
routerindex = {} # Dictionary to convert routerindex to routername
routers = [] # List of new thread created for each router
RoutingTable = [] # Routing Table to be printed
Neighbours = [] # List of Neighbours
RouterQueue = [] # Router Queue storing the list of received packets
UpdatedDistance = [] # Distances that were updated

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
        Neighbours.append([])
        RouterQueue.append([])
        UpdatedDistance.append([])
        RoutingTable.append([])

    for i in range(2, len(inputs)): # Updating the Neighbours List
        if inputs[i][0] == "EOF":
            break
        router1 = int(routerindex[inputs[i][0]])
        router2 = int(routerindex[inputs[i][1]])
        Weight = int(inputs[i][2])
        Neighbours[router1].append([router2, Weight])
        Neighbours[router2].append([router1, Weight])

# Creating a thread for each router    
def CreateRouter():
    for i in range(NumRouters):
       thread = threading.Thread(target = StartRouterProcess, args = (i,))
       routers.append(thread)
       routers[i].start()
    for router in routers:
        router.join()

# Initialise the routing table for each router
def CreateRoutingTable(routernumber):
    for i in range(NumRouters): # Initialising to INF distance 
        RoutingTable[routernumber].append([INF,-1])
        
    RoutingTable[routernumber][routernumber] = [0, routernumber] # Distance from A->A = 0
    
    # Adding all the neighbours to the Routing Table
    for neighbour in Neighbours[routernumber]:
        RoutingTable[routernumber][neighbour[0]] = [neighbour[1], neighbour[0]]


# Prints the Current Version of the Routing Table of
def PrintRoutingTable(iter, routernumber):
    lock.acquire() # mutex lock needed to print
    rname = routername[routernumber]
    print("\n***************************************************************\n")
    print("Updating Routing Table of Router " + rname+".")
    print("Routing Table for router " + rname + ":\n")
    print("Iteration Count: " + str(iter))
    # Creating the Table to be output
    output=[["Router Name", "Distance from router " + rname, "Next Router"]]
    for i in range(NumRouters):
        temp = []
        Dis = RoutingTable[routernumber][i][0] # Distance to node i
        nextnode = RoutingTable[routernumber][i][1] # next node to reach i
        a = routername[i] + ("*" if i in UpdatedDistance[routernumber] else " ") # if updated add *
        b = (str(Dis) if Dis != INF else "INF") # if distance = Infinity i.e. node not reachable
        c = (routername[nextnode] if nextnode != -1 else "-") # if node not reachable 
        temp.append(a) 
        temp.append(b) 
        temp.append(c)
        output.append(temp)
    print(tabulate(output, headers = "firstrow", tablefmt = "fancy_outline", stralign="center", numalign="center"))    
    UpdatedDistance[routernumber].clear()
    lock.release()
    
# Sends Distance Vector to all the neighbouring routers
def SendRoutingTable(routernumber):
    time.sleep(2)   # Send after every 2 seconds
    for router in Neighbours[routernumber]:
        lock.acquire() # lock acquired to print
        RouterQueue[router[0]].append(routernumber)
        print("\n***************************************************************\n")
        print("Routing Table send from Router "+routername[routernumber]+" to Router " + routername[router[0]])
        lock.release() # release the lock
    
def GetNeighbourVectors(routernumber):
    # Wait until packets received from all neighbours
    while(len(RouterQueue[routernumber]) < len(Neighbours[routernumber])):
        pass
        
def UpdateRoutingTable(routernumber):
    # Once all packets received update the Routing Table Using Bellman-Ford's Equation
    for i in range(NumRouters):
        for neighbour in Neighbours[routernumber]:
            newdis = neighbour[1] + RoutingTable[neighbour[0]][i][0]
            if RoutingTable[routernumber][i][0] > newdis:
                RoutingTable[routernumber][i][0] = newdis
                UpdatedDistance[routernumber].append(i)
                RoutingTable[routernumber][i][1] = neighbour[0]
    RouterQueue[routernumber].clear()
    

def StartRouterProcess(routernumber):
    CreateRoutingTable(routernumber) # Initialise the Routing Table
    PrintRoutingTable(0, routernumber) # Print the Routing Table
    i = 0
    
    # Max Iterations needed to get shortest path in Bellman-Ford's Algorithm is
    # equal to the max length of a path in a graph of n nodes which is equal to 
    # n-1. Therefore Routing Table updated for NumRouters - 1 times.
    while i < NumRouters - 1: 
        SendRoutingTable(routernumber) # Send the Distance Vector to neighbours
        GetNeighbourVectors(routernumber) # Wait until all Distance Vectors received
        UpdateRoutingTable(routernumber) # Update using Bellman-Ford's Equation
        PrintRoutingTable(i+1,routernumber) # Print the Routing Table
        time.sleep(2)
        i += 1


def main():
    TakeinputsFromFile()
    print("")
    CreateRouter()
    print("\n***************************************************************\n")
    

if __name__ == "__main__":
    main()