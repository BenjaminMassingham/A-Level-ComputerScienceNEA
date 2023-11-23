import math

#This module is used to perform regex expression comparisons, I used this to validate email addresses
import re

#This module is used to interface in between my program and my database, to store things like users details and log in activity
import sqlite3

#This module is used to halt the program to make it feel more natural
import time

f = open('distances.txt','w')

dbfile = 'Data Files/AirportGraph.db'

#Establish a connection to the database
con = sqlite3.connect(dbfile)
cur = con.cursor()

sql = '''SELECT * FROM Point_Coordinates'''

# Split the string into lines and then split each line into values
point_coordinates = [a for a in cur.execute(sql)]

# Convert the strings to integers
data_list = [[item if i == 0 else int(item) for i, item in enumerate(line)] for line in point_coordinates]

for coordinate in data_list:
    for coord in data_list:
        dist_y = coord[2] - coordinate[2]
        dist_x = coord[1] - coordinate[1]
        distance = round(math.sqrt(((dist_x)**2)+((dist_y)**2)),2)
        f.write(f'Distance between {coordinate[0]} and {coord[0]}: {distance}\n')

        #Write the SQL command
        sql = f''' INSERT INTO All_Distances ("Node A","Node B","Distance Between A & B") VALUES ("{coordinate[0]}","{coord[0]}","{distance}"); '''
        
        #Executes the SQL command
        cur.execute(sql)

#Save the Database
con.commit()

#Close the Database
con.close()

f.close()
