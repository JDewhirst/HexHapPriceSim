#Pathfinding algorithm
import math
import copy
#Implementation of Dijkstra's algorithm

def Dijkstra(graph,source,target):
    #All the nodes which have not been visited yet
    unvisited_nodes = copy.deepcopy(graph)
    #Will store the shortest distance from one node to another
    shortest_distance={}
    #Will store the shortest path between source and target
    route=[]
    #Will store the predecessors of the nodes
    predecessor={}
    
    for nodes in unvisited_nodes:
        #setting shortest_distance of all nodes as infinity
        shortest_distance[nodes]= math.inf
    
    #the dist of a point to itself is 0
    shortest_distance[source] = 0
    
    #loop while all nodes have not been visited
    while(unvisited_nodes):
        
        min_Node = None
        
        #iterate through all the unvisited nodes
        for current_node in unvisited_nodes:
            
            if min_Node is None:
                min_Node = current_node 
            elif shortest_distance[min_Node] > shortest_distance[current_node]:
                #if the value of the min_Node is less than that of current_node
                min_Node = current_node
                
        #iterating through connected nodes of curren_node) and the weight of the edges
        for child_node, value in unvisited_nodes[min_Node].items():
        
            #checking if the value of the current_node + value of the edge
            #that connects this neighbour node with current_node
            #is lesser than the value that distance between current nodes
            #and its connections
            if value + shortest_distance[min_Node] < shortest_distance[child_node]:
                #if true set the new value as the minimum distance of that connection
                shortest_distance[child_node] = value + shortest_distance[min_Node]
                #add current node as the predecessor of the child_node
                predecessor[child_node] = min_Node
                
                
        #after the node has been visited remove it from the unvisited_nodes
        unvisited_nodes.pop(min_Node)
    
    #Shortest distance has been found. Set curent node as target
    node = target
    
    #Backtrack from goal node to source node to see what path we followed
    while node != source:
        try:
            route.insert(0,node)
            node = predecessor[node]
        except Exception:
            print('Path not reachable')
            break
    route.insert(0, source)
    
    if shortest_distance[target] != math.inf:
        #print('Shortest distance is ' + str(shortest_distance[target]))
        #print('And the path is ' + str(route))
        return shortest_distance[target], str(route)
        
