import random
import math
import matplotlib.pyplot as plt
import time

#Return a list of tuples with the edges connceting the graph together (node#,node#,speedLimit,trafficLights)
#node# is just the index the node is stored at
#I will connect each node in each town to it's nearest 2 nodes, so each node in a town should have at least 2 connecting nodes.
#The nearest node to the interstate will be connected to it
#Speed limit for town roads are randomly between 35 and 55, traffic lights between 0 and 4
#Speed limit for exits are 65 with 0 traffic lights
#Speed limit for interstate is 70 with 0 traffic lights
def EdgeMaker(nodes):
    edges=[]

    #if doing an interstate instead of a town
    if nodes[0][2]==0:
      for node in nodes:
        if node[3]!=8:
          edges.append((node[3],node[3]+1,70,0))
      return edges


    interstate=[] #used later for closest node to interstate
    for x in range(int(225/25)):
        interstate.append((100,x*25,0,x))
    iMin=200
    for mainNode in nodes: #find each nodes 2 nearest nodes
      for minCount in range(2):
        min=100
        for checkNode in nodes:
          #Check to make sure these nodes are not already connected to each other
          tof=False #temp boolean used
          for edge in edges:
            if (edge[0] == checkNode[3] and edge[1] == mainNode[3]) or (edge[1] == checkNode[3] and edge[0] == mainNode[3]):
              tof=True
              break
          if tof:
            continue

          distance=math.sqrt((mainNode[0]-checkNode[0])**2+(mainNode[1]-checkNode[1])**2) #The distance between nodes
          if distance==0: #If a node is being compared to itself
            continue
          if distance<min:
            min=distance
            index=checkNode[3]
        edges.append((mainNode[3],index,int(random.random()*20+35),int(random.random()*4)))


      #find the node closest to the interstate
      for iNode in interstate:
        distance=math.sqrt((mainNode[0]-iNode[0])**2+(mainNode[1]-iNode[1])**2)
        if distance<iMin:
          iMin=distance
          indexes=(iNode[3],mainNode[3])
    edges.append((indexes[0],indexes[1],65,0))

    #pick a node and make sure it can reach everything in the town
    #if not connect the two nodes together.
    while True:
      edgeList=[edges[0][0]]
      connected=[]
      explored=[]
      while True: #Trace through the edges of the town and make a list of all "explored" nodes AKA all nodes that connect to edges[0][0]
        explored.append(edgeList[0])
        for edge in edges:
          if edge[0]==edgeList[0]:
            connected.append(edge[1])
          elif edge[1]==edgeList[0]:
            connected.append(edge[0])
        for i in connected:
          if i not in explored and i not in edgeList:
            edgeList.append(i)
        edgeList.remove(edgeList[0])
        connected=[]
        if len(edgeList)==0:
          break

      tof=True
      for index in nodes: #If any node does not connect to edges[0][0] connect it to edges[0][0] and restart this process to check for more
        if index[3] not in explored:
          edges.append((index[3],edges[0][0],int(random.random()*20+35),int(random.random()*4)))
          tof=False
      if tof:
        break

    return edges

#Create a random graph with a deterministic interstate through the middle
#Have a few "towns" with maybe 15 nodes randomly generated around the interstate
#Graph will be 200x200 Towns will be like 30x30
#Return the node's graph as a list of tuples, with the tuples being (xCord,zCord,town#(orInterstate=0),index#)
def NodesGenerator():
    #Make an interstate going through middle of screen with an exit every 25 cords
    nodes=[] #stores all the nodes
    edges=[] #stores all the edges
    index=0
    for x in range(int(225/25)):
      nodes.append((100,x*25,0,index))
      index+=1
    edges+=EdgeMaker(nodes)
    usedXs=[] #used to store the outline of all the towns, so no towns overlap
    usedZs=[]
    #Generate 6 random towns that can not intersect with each other or the interstate
    for townNum in range(6):
      town=[]
      while True:
        zCordChange=random.random()*170  #Will move the whole town up a random amount
        xCordChange=random.random()*70  #Will move the whole town horizontally a random amount
        if (random.random()>.5): #Make the town on the right side of the interstate
          xCordChange+=100
        tof=0
        for x in range(len(usedXs)): #If the new x overlaps a prevoius towns x remember it
          if xCordChange>usedXs[x]-35 and xCordChange<usedXs[x]+35: #Make a box around the prvious values and dont let them fall in the box
            tof+=1
          if zCordChange>usedZs[x]-35 and zCordChange<usedZs[x]+35:
            tof+=1
          if (tof==2):
            break
          tof=0
        if tof !=2: #If both are overlapping get new numbers
          usedXs.append(xCordChange)
          usedZs.append(zCordChange)
          break


      #Generate one town with node amount between 15-20 20 is technically extremely rarer than the others which is ok
      for nodeNum in range(int(random.random()*5+15)):
        while True: #Garuntee the nodes are spaced out a bit from each other
          x=random.random()*30+xCordChange
          z=random.random()*30+zCordChange
          tof=True
          for node in town:
            if x>node[0]-3 and x<node[0]+3 and z>node[1]-3 and z<node[1]+3: #must be 3 units away from each other in both cords
              tof=False
          if tof:
            break
        town.append((x,z,townNum+1,index))
        index+=1
      nodes+=town
      edges+=EdgeMaker(town)
    return (nodes, edges)


#Create a plot to display the graph
def PlotGenerator(nodes, edges):
  plt.figure(figsize=(8, 8))

  for node in nodes: #Display all the nodes
    plt.annotate(node[3],(node[0],node[1]))
    plt.plot(node[0],node[1],'b',marker=".")

  for edge in edges: #Display all the edges
    plt.plot([nodes[edge[0]][0],nodes[edge[1]][0]], [nodes[edge[0]][1],nodes[edge[1]][1]], color='black', linestyle='solid', linewidth=1)

  plt.show()



values=NodesGenerator()
nodes=values[0]
connections=values[1]
pathToFind=[0,0]
PlotGenerator(nodes,connections)
time.sleep(.5)  #Add a delay to fix a bug where colab won't ask for user input after displaying the plot

nodeCount=len(nodes)-1


while True:
  print("What node would you like to start at?")
  while True:
    pathToFind[0]=int(input())
    if pathToFind[0]>=0 and pathToFind[0]<=nodeCount:
      break
    else:
      print("Error please enter a proper node number")
  print("What node would you like to end at?")
  while True:
    pathToFind[1]=int(input())
    if pathToFind[1]>=0 and pathToFind[1]<=nodeCount and pathToFind[1] !=pathToFind[0]:
      break
    else:
      print("Error please enter a proper node number, that is not the starting node.")

  print("Enter 1 for shortest distance, or 2 for shortest time")
  dot=0
  while True:
    dot=int(input())
    if dot==1 or dot==2:
      break
    print("Error please input 1 or 2")
  if dot==1:
    distance=True
  else:
    distance=False


  #Run A*
  fringe=[] #Used to store all fringe edges
  explored=[] #Used to store all explored nodes with data associated
  exploredValues=[] #Used to store all explored nodes by number alone
  goalX=0;  #Used to store x value of goal node
  goalY=0;  #Used to store y value of goal node

  startNode=pathToFind[0] #The node we are starting at
  goalNode=pathToFind[1] #The node we would like to reach

  #find the x and y cord for the goal node
  for node in nodes:
    if node[0] == goalNode:
      goalX=node[0]
      goalY=node[1]

  currentNode=startNode #Used to keep up with most recently expanded node
  currentCost=0 #Used to store most recent total Cost
  while True:
    for connect in connections: #Look through all connections to find new possible edges
      if connect[0]==currentNode and connect[1] not in exploredValues:
        #Find the hueristic for this new edge
        hueristic=0
        x=0
        y=0
        for node in nodes:
          if node[3] == connect[1]:
            x=node[0]
            y=node[1]
            if distance:
              hueristic=math.sqrt((x-goalX)**2+(y-goalY)**2)
            else:
              hueristic=math.sqrt((x-goalX)**2+(y-goalY)**2)/70

        #Find the cost of the new edges
        cost=0
        for node in nodes:
          if node[3] == connect[0]:
            fromX=node[0]
            fromY=node[1]
            mph=connect[2]
            lights=connect[3]
            if distance:
              cost=math.sqrt((x-fromX)**2+(y-fromY)**2)
            else:
              cost=math.sqrt((x-fromX)**2+(y-fromY)**2)/mph + lights*.01
        fringe.append((connect[0], connect[1], currentCost+cost, hueristic))

      #Find connections for the opposite way AKA 2 way roads
      if connect[1]==currentNode and connect[0] not in exploredValues:
        #Find the hueristic for this new edge
        hueristic=0
        x=0
        y=0
        for node in nodes:
          if node[3] == connect[0]:
            x=node[0]
            y=node[1]
            if distance:
              hueristic=math.sqrt((x-goalX)**2+(y-goalY)**2)
            else:
              hueristic=math.sqrt((x-goalX)**2+(y-goalY)**2)/70

        #Find the cost of the new edges
        cost=0
        for node in nodes:
          if node[3] == connect[1]:
            fromX=node[0]
            fromY=node[1]
            mph=connect[2]
            lights=connect[3]
            if distance:
              cost=math.sqrt((x-fromX)**2+(y-fromY)**2)
            else:
              cost=math.sqrt((x-fromX)**2+(y-fromY)**2)/mph  + lights*.01

        fringe.append((connect[1], connect[0], currentCost+cost, hueristic))



    #Now I have all new fringe vertices Select lowest cost + hueristic and explore

    min=10000
    exploreEdge=[]
    for edge in fringe:
      cost=edge[2]+edge[3]
      if cost<min:
        min=cost
        currentCost=edge[2]
        exploreEdge=edge

    exploredValues.append(exploreEdge[0])
    explored.append(exploreEdge)
    fringe.remove(exploreEdge)
    currentNode=exploreEdge[1]
    if exploreEdge[1] == goalNode:
      #Output path then break
      path=str(goalNode)
      while True:
        for e in explored:
          if e[1]==currentNode:
            currentNode=e[0]
            path=path+" "+str(int(e[0]))
            break
        if currentNode == startNode:
          break
      reversePath=path.split()
      reversePath.reverse()
      path=", ".join(reversePath)
      if distance:
        print("The shortest path with respect to distance is " + path+"\n")
        print("The distance is " + str(exploreEdge[2])+" miles\n")
      else:
        print("The shortest path with respect to time is " + path+"\n")
        print("The time is " + str(exploreEdge[2])+" hours\n")
      break

  #Ask if they want to quit, continue with same plot, or get a new plot
  print("Enter 0 to quit, 1 to continue with the same plot, or 2 to continue with a new plot")
  coq=-1
  while True:
    coq=int(input())
    if coq ==0 or coq==1 or coq==2:
      break
    print("Error please input 0, 1, or 2")
  if coq == 0:
    break
  if coq == 1:
    PlotGenerator(nodes,connections)
    time.sleep(.5)  #Add a delay to fix a bug where colab won't ask for user input after displaying the plot
    continue
  values=NodesGenerator()
  nodes=values[0]
  connections=values[1]
  pathToFind=[0,0]
  PlotGenerator(nodes,connections)
  time.sleep(.5)  #Add a delay to fix a bug where colab won't ask for user input after displaying the plot