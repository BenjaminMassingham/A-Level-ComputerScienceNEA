#This module allows direct access to some variables or functions stored inside of the interpreter
import sys

import sqlite3

#Creating the graph object 
class Graph(object):

    #Instantiating the graph object
    def __init__(self, nodes, init_graph):
        
        #Setting self.nodes to the nodes array instantiated before the graph object was created
        self.nodes = nodes

        #Setting self.graph to the graph dictionary instantiated before the graph object was created
        self.graph = init_graph
    
    #A function that returns the nodes of the graph
    def get_nodes(self):
        
        #Returns the nodes of the graph
        return self.nodes
    
    #A function that returns all of the connected nodes to a specific node
    def get_outgoing_edges(self, node):
        
        #Emptying the connections array
        connections = []

        #For loop to search through each and every node
        for out_node in self.nodes:

            #Using a get function to extract the data from the dictionary to determine if the node being searched is a neighbour 
            if self.graph[node].get(out_node, False) != False:
                
                #If the node is a neighbour, it gets added to the connections array
                connections.append(out_node)
        
        #Returning the connections array
        return connections
    
    #A function to obtain the distance between two nodes
    def value(self, node1, node2):
        
        #Returning the distance between the two nodes
        return self.graph[node1][node2]

#Defining the dijkstra's algorithm function
def dijkstra_algorithm(graph, start_node):

    #Defining an unvisited_nodes array and getting all nodes from the graph.get_nodes function
    unvisited_nodes = list(graph.get_nodes())
 
    #This dictionary is used to save the shortest known distance to each and every node 
    shortest_path = {}
 
    #This dictionary is used to save the shortest known path to each and every node
    previous_nodes = {}
 
    #This variable is initialised as infinite 
    max_value = sys.maxsize
    
    #For loop to search through each and every node that has not been visited yet
    for node in unvisited_nodes:

        #Setting the shortest path to all of the nodes to infinite
        shortest_path[node] = max_value

    #The node we start at, has a distance of 0
    shortest_path[start_node] = 0

    #The following while loop, searches for the node with the shortest distance away from the starting node from the unvisited_nodes array
    
    #A while loop to run the code indefinitely whilst there are values in the unvisited_nodes array
    while unvisited_nodes:

        #Assigning the current_min_node to None
        current_min_node = None

        #For loop to search through all remaining unvisited nodes
        for node in unvisited_nodes:
            
            #Checks if current_min_node is still None
            if current_min_node == None:

                #Assigns current_min_node a node if it is still none
                current_min_node = node

            #Searches the dictionaries to check if the shortest distance to the current node being searched is less than the distance to the current minimum
            elif shortest_path[node] < shortest_path[current_min_node]:
                
                #If it is less than, the current minimum is assigned to that node
                current_min_node = node
                
        #The code below retrieves the distance between the current minimum node and all of its neighbours

        #Extracting the neighbouring edges of the current minimum node from the graph dictionary
        neighbours = graph.get_outgoing_edges(current_min_node)
        
        #For loop to search through all of the neighbouring nodes
        for neighbour in neighbours:

            #Assigns tentative value to, the shortest distance between the current node and the neighbour, added to the shortest distance to the current node
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbour)

            #Checks if this tentative value is shorter than the already assigned shortest path to the neighbour node
            if tentative_value < shortest_path[neighbour]:

                #If the tentative value is shorter than the already assigned value, we assigned the tentative value
                shortest_path[neighbour] = tentative_value
                
                #If the tentative value is shorter than the already assigned value, we assigned the current node as the previous node
                previous_nodes[neighbour] = current_min_node
 
        # After visiting its neighbours, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    #Returning the previous_nodes and shortest_path dictionaries
    return previous_nodes, shortest_path

#A helper function to print the result of the shortest path
def print_result(previous_nodes, shortest_path, start_node, target_node):

    #Creating a path array to store the path of the shortest path
    path = []

    #Assignging the node variable to the target_node
    node = target_node
    
    #While loop to search all the way through the path and append it to the path array whilst the node doesn't equal the start_node
    while node != start_node:
        
        #Appending the current node to the path
        path.append(node)

        #Assigning the previous node to the node variable
        node = previous_nodes[node]
 
    #Adding the start_node to the path
    path.append(start_node)
    
    #Printing out the shortest distance
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    
    #Printing out the path of the shortest distance by printing the path array in reverse
    print(" -> ".join(reversed(path)))

#Determining the database file
dbfile = 'Data Files/AirportGraph.db'

#Establish a connection to the database
con = sqlite3.connect(dbfile)
cur = con.cursor()

#The sql code to extract all of the names of the point_names
sql = '''SELECT PointName FROM Point_Coordinates'''

#Appenidng all of the point names to an array called point_names
point_names = [a for a in cur.execute(sql)]

#Creating an empty nodes array
nodes = []

#For loop to search through every point in the point_names array
for point in point_names:

    #Converting the point to a list instead of a tuple
    point = list(point)

    #Append the point_name to the nodes
    nodes.append(point[0])

#Creating the intial graph dictionary
init_graph = {}

#Using a for loop to search through each node in the nodes array
for node in nodes:

    #Creating a key for each node inside of the initial graph dictionary
    init_graph[node] = {}

#SQL code to extract all of the connections from the database
sql = '''SELECT * FROM Point_Connections'''

#Putting all records into a 2 dimensional array
point_coordinates = [a for a in cur.execute(sql)]

#Creating a correct point array to store all of the individual lists that have been corrected and had their null values removed
correct_point_coordinates = []

#For loop to search through each record in the point_coordinates 2D array
for point in point_coordinates:

    #Converting the tuple to a list
    point = list(point)

    #Initialising i to 0
    i = 0 

    #While the point list has null values this while loop will run
    while None in point:

        #Checks if the value inside of point is null
        if point[i] == None:

            #If it is null, remove the value from the list
            point.pop(i)

            #Decrease i by 1 to account for the removed value
            i -= 1

        else:

            #If the value is not null, increase i by 1
            i += 1

    #Once the point has been corrected, append it to the corrected point coordinates array
    correct_point_coordinates.append(point)

#For loop to search through each point in the corrected points array
for point in correct_point_coordinates:

    #Setting the initial_point to the node which all the other nodes are connected to
    initial_point = point[0]

    #Removing the initial point from the point list
    point.pop(0)

    #Creating an array to store the name of all nodes connected
    connected_nodes_names = point[0::2]

    #Creating an array to store the distance between the initial node and all of the nodes connected
    connected_nodes_distances = point[1::2]

    #For loop to iterate for every value in the connected_nodes
    for count in range(len(connected_nodes_distances)):

        #Assigning the correct distances to the correct connections inside of the graph dictionary
        init_graph[str(initial_point)][str(connected_nodes_names[count])] = float(connected_nodes_distances[count])

#Closing and saving the database
con.commit()
cur.close()

#Calling the graph object and instantiating it using the nodes and graph data structures
graph = Graph(nodes, init_graph)

starting_point = input('Please enter your start point: ')

finishing_point = input('Please enter your end point: ')

#Calling the dijkstra's algorithm to find the shortest distance between the two nodes
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=starting_point)

#Using the helper function to print out the result in a nice way
print_result(previous_nodes, shortest_path, start_node=starting_point, target_node=finishing_point)