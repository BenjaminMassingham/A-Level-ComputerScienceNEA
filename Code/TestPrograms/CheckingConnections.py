import math

#This module is used to perform regex expression comparisons, I used this to validate email addresses
import re

#This module is used to interface in between my program and my database, to store things like users details and log in activity
import sqlite3

#This module is used to halt the program to make it feel more natural
import time

dbfile = 'Data Files/AirportGraph.db'

#Establish a connection to the database
con = sqlite3.connect(dbfile)
cur = con.cursor()

sql = '''SELECT * FROM Point_Connections'''

# Split the string into lines and then split each line into values
point_coordinates = [a for a in cur.execute(sql)]

correct_point_coordinates = []

for point in point_coordinates:
    point = list(point)
    i = 0 
    while None in point:
        if point[i] == None:
            point.pop(i)
            i -= 1
        else:
            i += 1
    correct_point_coordinates.append(point)

for point in correct_point_coordinates:
    point_name = point[0]
    point.pop(0)
    connected_nodes = point[0::2]
    print(f'\nConnections to Node {point_name}')
    print(connected_nodes)
    input('Press enter to continue: ')

con.commit()
cur.close()

