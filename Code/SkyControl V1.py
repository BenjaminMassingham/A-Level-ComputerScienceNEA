#Importing the required modules

#The modules below are necessary to create the GUIs for the program to run on 
import customtkinter as ctk
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

#This module is used to perform regex expression comparisons, I used this to validate email addresses
import re

#This module is used to interface in between my program and my database, to store things like users details and log in activity
import sqlite3

#This module allows direct access to some variables or functions stored inside of the interpreter
import sys

#This module is used to halt the program to make it feel more natural
import time

import threading

#Setting the appearance mode and theme colour
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue") 

#Creatin the Main Menu Page
class MainMenu(ctk.CTk):

    #Setting the default window size
    width = 1200
    height = 800

    #Creating a dictionary to store all of the nodes
    nodes = {}

    #Creating a dictionar to store all of the aircraft
    planes = {}

    #Setting the constants to make sure the planes move on the apron and not elsewhere on the GUI
    CONST_X = 209
    CONST_Y = 83

    def __init__(self):
        super().__init__()

        #Setting Window Title
        self.title('SkyControl')

        #Setting Window Icon
        self.after(201, lambda :self.iconbitmap('Graphics/Logo.ico'))

        #Get screen dimensions
        self.ws = self.winfo_screenwidth() 
        self.hs = self.winfo_screenheight()
        
        #Setting Window Size and Placing it in the middle of the screen
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, ((self.ws/2)-(self.width/2)), ((self.hs/2)-(self.height/2))))
        
        #Setting Background Image to a locked background
        self.backgroundImage = PhotoImage(file=r'Graphics/Locked Main Menu GUI PNG File.png')
        self.bgimage = Label(self, image = self.backgroundImage)
        self.bgimage.place(x=0,y=0)
        
        #Making the window none resizeable
        self.resizable(False,False)

        #Calling the login and signUp Menu
        LogIn = MainLogin()
        LogIn.mainloop()

        #Creating and instantiating the graph of the airport

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

        #Setting the background image to an unlocked background
        self.backgroundImage = PhotoImage(file=r'Graphics/Main Menu GUI PNG File.png')
        self.bgimage = Label(self, image = self.backgroundImage)
        self.bgimage.place(x=0,y=0)

        #Finding and fixing the username of the user who logged in 
        username = self.finding_username()

        #Adding the username to the screen
        self.username_text = ctk.CTkLabel(self, 
                                            text=f"{username}", 
                                            font = ('Manrope', 20), 
                                            fg_color='#5a5a5a', 
                                            bg_color='#2b2b2b',
                                            text_color='#f8f8f8')
        self.username_text.place(x = 1135, y = 34, anchor = 'e')

        #Creating and Placing the LogOut button 
        self.logout_button = ctk.CTkButton(self, 
                                            text="Logout", 
                                            font = ('Manrope', 20), 
                                            command=self.logout_event, 
                                            width=100, 
                                            height=50, 
                                            corner_radius=50, 
                                            bg_color='#f8f8f8', 
                                            fg_color='#077fda', 
                                            text_color='#f8f8f8')
        self.logout_button.place(x=50,y=720)

        #Creating and Placing the Go button 
        self.go_button = ctk.CTkButton(self, 
                                            text="Go", 
                                            font = ('Manrope', 20), 
                                            command=lambda: self.plane_go(graph), 
                                            width=74, 
                                            height=50, 
                                            corner_radius=50, 
                                            bg_color='#f8f8f8', 
                                            fg_color='#077fda', 
                                            text_color='#f8f8f8')
        self.go_button.place(x=63,y=300)

        #Creating and Placing the start point entry text box
        self.start_point = ctk.CTkEntry(self, 
                                            width=150, 
                                            height=50, 
                                            placeholder_text="Start Point", 
                                            font = ('Manrope', 15), 
                                            bg_color='#f8f8f8', 
                                            border_color= '#000000',
                                            fg_color='#e4f3ff', 
                                            corner_radius= 20)
        self.start_point.place(x=25,y=150)

        #Creating and Placing the end point entry text box
        self.end_point = ctk.CTkEntry(self, 
                                            width=150, 
                                            height=50, 
                                            placeholder_text="End Point", 
                                            font = ('Manrope', 15), 
                                            bg_color='#f8f8f8', 
                                            border_color= '#000000',
                                            fg_color='#e4f3ff', 
                                            corner_radius= 20)
        self.end_point.place(x=25,y=225)

    #This function is used to extract the username from the database
    def finding_username(self):

        #Executing SQL command to find who is currently logged in
    
        #Find the path for the database
        dbfile = 'Data Files/UserLoginInfo.db'

        #Establish a connection to the database
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        #Writing SQL command 
        sql = 'SELECT Username FROM LoginInfo WHERE Logged_In = 1'

        #Executing SQL command 
        username_list = [a for a in cur.execute(sql)]

        #Extracting the username
        username = username_list[0]

        #Save the Database
        con.commit()

        #Close the Database
        con.close()

        #Cleaning up data 
        username = username[0]

        #Returning the username 
        return username

    #This function is called when the logout button is pressed and is used to leave the program
    def logout_event(self):
        Leave = ExitMenu('Graphics/Leaving Program PNG File.png')
        Leave.mainloop()
        self.destroy()
        self.quit()

    #This function is called when the go button is pressed and is used to process all inputted data and move the aircraft from A to B
    def plane_go(self, graph):
        
        #Giving the plane a custom key
        key = f'{self.start_point.get()}{self.end_point.get()}'

        #Creating a key inside of the planes dictionary using that key
        self.planes[key] = {}

        #Using dijkstra's algorithm to find the shortest path between two nodes
        previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=self.start_point.get())

        #Using a helper function to return a list of the path
        path = return_path_list(previous_nodes, shortest_path, start_node=self.start_point.get(), target_node=self.end_point.get())

        #Creating an array to store the corrected path
        correct_path = []
        
        #For loop to reverse the order of the path list

        #For loop to search through the path list in reverse order
        for node in path[::-1]:

            #Appending the node to the correct_path list
            correct_path.append(node)
        
        #Setting path to correct_path
        path = correct_path

        #Determining the database file
        dbfile = 'Data Files/AirportGraph.db'

        #Establish a connection to the database
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        #SQL code to return the coordinates of the starting position
        sql = f'''SELECT * FROM Point_Coordinates WHERE PointName = "{path[0]}"'''

        #Running the SQL code and storing the outcome in the next_point array
        next_point = [a for a in cur.execute(sql)]

        #Setting the starting coordinates of the plane to the position of the starting node + the constants
        new_x = int(next_point[0][1]) + self.CONST_X
        new_y = int(next_point[0][2]) + self.CONST_Y

        #Initialising the visted_nodes array which will store all of the nodes that the plane has already visited, the starting node is added automatically
        visited_nodes = [path[0]]

        #Initialising the pixel path array, this array stores the path of the aircraft in pixel form which can be done to perform the movement of the image, the starting nodes position is added
        pixel_path = [[new_x, new_y]]

        #Creating a tick system, to help the program index the pixel_path array
        tick = 0

        #The below for loop goes through each node in the path and calculates pixel coordinates for each tick movement

        #For loop to search through each node in the path
        for node in path:
            
            #Checking if the node has already been visted
            if node not in visited_nodes:

                #SQL code to find the coordinates of the next node
                sql = f'''SELECT * FROM Point_Coordinates WHERE PointName = "{node}"'''

                #Running the SQL and storing the outcome in an array called next_point
                next_point = [a for a in cur.execute(sql)]

                #SQL code to find the coordinate of the current
                sql = f'''SELECT * FROM Point_Coordinates WHERE PointName = "{visited_nodes[len(visited_nodes)-1]}"'''

                #Running the SQL code and inputting the data into a list called current_point
                current_point = [a for a in cur.execute(sql)]

                #Calculate the difference in x and y between the 2 points
                dist_y = next_point[0][2] - current_point[0][2]
                dist_x = next_point[0][1] - current_point[0][1]

                #Appending this node to the vistited nodes array
                visited_nodes.append(node)

                #Running a loop whilst the plane has not reached the node
                while dist_x != 0 or dist_y != 0:
                    
                    #Checking if the plane is not at the correct x coordinate
                    if dist_x != 0:
                        
                        #Checking if the difference is greater than 0
                        if dist_x > 0:
                            
                            #If the difference is greater than 0, add one to the current pixel position
                            new_x = pixel_path[tick][0] + 1

                            #Minus 1 from the difference
                            dist_x -= 1
                        
                        else:
                            
                            #If the difference is less than 0, minus one to the current pixel position
                            new_x = pixel_path[tick][0] - 1

                            #Add 1 to the difference
                            dist_x += 1

                    else:
                        
                        #If the difference is equal to zero and the pixel is already at the correct coordinate, the plane stays on the same axis level
                        new_x = pixel_path[tick][0]
                    
                    #Checking if the difference between current position and necessary position is equal to 0
                    if dist_y != 0:
                        
                        #If not 0, check if the difference is greater than 0
                        if dist_y > 0:

                            #If the difference is greater than 0, add one to the current pixel position
                            new_y = pixel_path[tick][1] + 1

                            #Minus 1 from the difference
                            dist_y -= 1
                        
                        else:

                            #If the difference is less than 0, minus one to the current pixel position
                            new_y = pixel_path[tick][1] - 1

                            #Add 1 to the difference
                            dist_y += 1
                    
                    else:
                        
                        #If the difference is equal to zero and the pixel is already at the correct coordinate, the plane stays on the same axis level
                        new_y = pixel_path[tick][1]
                    
                    #Appending the new x and y coordinates to the pixel path
                    pixel_path.append([new_x,new_y])
                    
                    #Increasing the tick counter by 1
                    tick += 1
            else:
                
                #If the difference is equal to zero and the pixel is already at the correct coordinate, the plane stays on the same axis level
                visited_nodes.append(node)

            #Once this node has been explored, reset the differences to 0
            dist_x, dist_y = 0, 0  

        #Running the move_plane function inside of a seperate thread so that the time.sleep function inside of that function does not affect the mainloop of the GUI program
        threading.Thread(target = self.move_plane, args= (pixel_path, key)).start()

    #This function is used to display the plane sprite
    def place_plane(self, x, y, key):
        
        #Creating the aircraft sprite
        planeImage = PhotoImage(file=r'Graphics/Heavy Aircraft Radar Dot PNG File.png')

        #Creates a label and addes it to the planes dictionary
        self.planes[key] = Label(self, 
                                   image = planeImage,
                                   borderwidth=0, 
                                   bg='#ffffff')
        
        #Places the aircraft in the designated position
        self.planes[key].place(x=x,y=y)

    #This function is used to remove the plane sprite
    def remove_plane(self, key):

        #Deletes the plane with the designated key
        self.planes[key].destroy()

    #This function uses both the place_plane function and the remove_plane function to create a smooth movement of the aircraft from A to B
    def move_plane(self, path, key):

        #Searches through each pixel coordinate in the pixel path array
        for node in path:

            #Calls the place_plane function to place the plane at that coordinate
            self.place_plane(node[0],node[1],key)

            #Sleeps for x amount of seconds
            time.sleep(0.005)

            #Calls the remove_plane function to remove this iteration of the sprite before creating the next
            self.remove_plane(key)

#Creating the Main Login page
class MainLogin(ctk.CTkToplevel):

    #Setting the default window size
    width = 1000
    height = 600

    def __init__(self):
        super().__init__()

        #Setting Window Title
        self.title('SkyControl')

        #Setting Window Icon
        self.after(201, lambda :self.iconbitmap('Graphics/Logo.ico'))

        #Get screen dimensions
        ws = self.winfo_screenwidth() 
        hs = self.winfo_screenheight()
        
        #Setting Window Size and Placing it in the middle of the screen
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, ((ws/2)-(self.width/2)), ((hs/2)-(self.height/2))))
        
        #Setting Background Image
        self.backgroundImage = PhotoImage(file=r'Graphics/Login Sign Up Page PNG File.png')
        bgimage = Label(self, image = self.backgroundImage)
        bgimage.place(x=0,y=0)
        
        #Making the window none resizeable
        self.resizable(False,False)

        #Creating and Placing the Username entry text box
        self.username_entry = ctk.CTkEntry(self, 
                                            width=400, 
                                            height=50, 
                                            placeholder_text="Username", 
                                            font = ('Manrope', 15), 
                                            bg_color='#f8f8f8', 
                                            border_color= '#000000',
                                            fg_color='#e4f3ff', 
                                            corner_radius= 20)
        self.username_entry.place(x=125,y=225)

        #Creating and Placing the Password entry box
        self.password_entry = ctk.CTkEntry(self, 
                                            width=400, 
                                            height=50, 
                                            show="*", 
                                            placeholder_text="Password", 
                                            font = ('Manrope', 15), 
                                            bg_color='#f8f8f8', 
                                            border_color= '#000000', 
                                            fg_color='#e4f3ff', 
                                            corner_radius= 20)
        self.password_entry.place(x=125,y=300)

        #Creating and Placing the LOGIN button 
        self.login_button = ctk.CTkButton(self, 
                                            text="Login", 
                                            font = ('Manrope', 20), 
                                            command=self.login_event, 
                                            width=100, 
                                            height=50, 
                                            corner_radius=50, 
                                            bg_color='#f8f8f8', 
                                            fg_color='#077fda', 
                                            text_color='#f8f8f8')
        self.login_button.place(x=275,y=375)

        #Creating and Placing the SIGNUP button 
        self.signup_button = ctk.CTkButton(self, 
                                            text="Sign Up", 
                                            font = ('Manrope', 20), 
                                            command= self.signup_event, 
                                            width=100, 
                                            height=50, 
                                            corner_radius=50, 
                                            bg_color='#077fda', 
                                            fg_color='#f8f8f8', 
                                            text_color='#000000')
        self.signup_button.place(x=775,y=300)

    def checking_username_exists(self, userData):
        
        #Setting valid to False by default 
        valid = False 

        #Find the path for the database
        dbfile = 'Data Files/UserLoginInfo.db'

        #Establish a connection to the database
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        #Extracts the username from the entered data
        username = userData[0]

        #Extracts all of the usernames from the table that are the same
        username_list = [a for a in cur.execute(f"Select Username From LoginInfo Where Username = '{username}'")]

        #Gather all the usernames that are the same as the inputted username
        usernameExist = len(username_list)

        #Check if the amount of duplicates is greater than 0
        if usernameExist == 1:
            valid = True 

        #Close the Database
        con.close()

        #Return valid variable 
        return valid

    def check_password(self, userData):

        #Setting valid to False by default 
        valid = False 

        #Find the path for the database
        dbfile = 'Data Files/UserLoginInfo.db'

        #Establish a connection to the database
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        #Extracts the data from the entered data
        username = userData[0]
        password = (f"('{userData[1]}',)")

        #Extracting the SQL code
        realPassword = [a for a in cur.execute(f"Select Password From LoginInfo Where Username = '{username}'")]

        #Save the Database
        con.commit()

        #Close the Database
        con.close()

        #Comparing the entered password to the real password
        if str(password) == str(realPassword[0]):
            valid = True

        return valid

    def login_event(self):
        
        #Setting valid to false by default
        valid = False

        #Extracting the data from the entry fields
        self.userData = [self.username_entry.get(), self.password_entry.get()]

        #Checking the validity of the data 
        valid = self.checking_username_exists(self.userData)

        if valid == True:
            
            #Setting valid to false by default
            valid = False

            #Checking the validity of the password
            valid = self.check_password(self.userData)

            if valid == True:
                
                #Logging the user in on the SQL database
    
                #Find the path for the database
                dbfile = 'Data Files/UserLoginInfo.db'

                #Establish a connection to the database
                con = sqlite3.connect(dbfile)
                cur = con.cursor()

                #Writing SQL command 
                sql = f'UPDATE LoginInfo SET Logged_In = 1 WHERE Username = "{self.userData[0]}"'

                #Executing SQL command 
                cur.execute(sql)

                #Save the Database
                con.commit()

                #Close the Database
                con.close()

                #Completing login process and opening the main menu page
                self.quit()
                self.destroy()

            else:
                
                #Calling the error label for username not existing
                Error = Popup('Graphics/Invalid Username or Password PNG File.png')
                Error.mainloop()
            
        else:
            
            #Calling the error label for username not existing
            Error = Popup('Graphics/Invalid Username or Password PNG File.png')
            Error.mainloop()
    
    def signup_event(self):

        self.withdraw()
        SignUp = SignUpPage()
        SignUp.mainloop()
        self.deiconify()

#Creating the Sign Up page
class SignUpPage(ctk.CTkToplevel):

    #Setting the Sign Up pages height and width 
    width = 400
    height = 600

    def __init__(self):
        super().__init__()
        
        #Setting Window Title
        self.title('SkyControl')

        #Setting Window Icon
        self.after(201, lambda :self.iconbitmap('Graphics/Logo.ico'))

        #Get screen dimensions
        ws = self.winfo_screenwidth() 
        hs = self.winfo_screenheight()
        
        #Setting Window Size and Placing it in the middle of the screen
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, ((ws/2)-(self.width/2)), ((hs/2)-(self.height/2))))

        #Setting Background Image
        self.bgimage = PhotoImage(file = r'Graphics/Sign Up Page PNG File.png')
        signUpImage = Label(self, image = self.bgimage)
        signUpImage.place(x=0,y=0)

        #Making the window none resizeable
        self.resizable(False,False)

        #Creating and Placing the Forename entry text box
        self.forename_entry = ctk.CTkEntry(self, 
                                            width=120,
                                            height=50, 
                                            placeholder_text="First Name", 
                                            font = ('Manrope', 12), 
                                            bg_color='#f8f8f8', 
                                            border_color= '#000000',
                                            fg_color='#e4f3ff', 
                                            placeholder_text_color='#9ea0a2', 
                                            text_color='#000000', 
                                            corner_radius= 20)
        self.forename_entry.place(x=73,y=101)

        #Creating and Placing the Surname entry text box
        self.surname_entry = ctk.CTkEntry(self, 
                                            width=120, 
                                            height=50, 
                                            placeholder_text="Surname", 
                                            font = ('Manrope', 12), 
                                            bg_color='#f8f8f8', 
                                            border_color= '#000000',
                                            fg_color='#e4f3ff', 
                                            placeholder_text_color='#9ea0a2', 
                                            text_color='#000000', 
                                            corner_radius= 20)
        self.surname_entry.place(x=207,y=101)

        #Creating and Placing the Email entry text box
        self.email_entry = ctk.CTkEntry(self, 
                                            width=254, 
                                            height=50, 
                                            placeholder_text="Email", 
                                            font = ('Manrope', 12), 
                                            bg_color='#f8f8f8', 
                                            border_color= '#000000',
                                            fg_color='#e4f3ff', 
                                            placeholder_text_color='#9ea0a2', 
                                            text_color='#000000', 
                                            corner_radius= 20)
        self.email_entry.place(x=73,y=176)

        #Creating and Placing the Email entry text box
        self.username_entry = ctk.CTkEntry(self, 
                                            width=254, 
                                            height=50, 
                                            placeholder_text="Username", 
                                            font = ('Manrope', 12), 
                                            bg_color='#f8f8f8', 
                                            border_color= '#000000',
                                            fg_color='#e4f3ff', 
                                            placeholder_text_color='#9ea0a2', 
                                            text_color='#000000', 
                                            corner_radius= 20)
        self.username_entry.place(x=73,y=251)

        #Creating and Placing the Email entry text box
        self.password_entry = ctk.CTkEntry(self, 
                                            width=254, 
                                            height=50, 
                                            placeholder_text="Password", 
                                            show = '*',
                                            font = ('Manrope', 12), 
                                            bg_color='#f8f8f8', 
                                            border_color= '#000000',
                                            fg_color='#e4f3ff', 
                                            placeholder_text_color='#9ea0a2', 
                                            text_color='#000000', 
                                            corner_radius= 20)
        self.password_entry.place(x=73,y=326)

        #Creating and Placing the SIGNUP button 
        self.submit_button = ctk.CTkButton(self, 
                                            text="Sign Up", 
                                            font= ('Manrope', 12), 
                                            command= self.sign_up_pressed,
                                            width=100, 
                                            height=50, 
                                            corner_radius=20, 
                                            border_color= '#000000', 
                                            bg_color='#f8f8f8', 
                                            fg_color='#077fda', 
                                            text_color='#f8f8f8')
        self.submit_button.place(x=227,y=401)
    
    #A function to enter all of the users information into the database
    def input_into_database(self, userData):

        #Find the path for the database file
        dbfile = 'Data Files/UserLoginInfo.db'

        #Establishes a connection to the database
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        #Write the SQL command
        sql = f''' INSERT INTO LoginInfo ("Forename","Surname","Email","Username","Password") VALUES ("{userData[0]}","{userData[1]}","{userData[2]}",'{userData[3]}',"{userData[4]}"); '''
        
        #Executes the SQL command
        cur.execute(sql)

        #Save the Database
        con.commit()

        #Close the Database
        con.close()

    #A function to check the validity of their password
    def check_password_validity(self, userData):

        #Creating a list of all of the special characters
        self.special_characters = ['!','"','#','$','%',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','^','_','`','{','}','|','~']
        
        #Setting valid to false by default
        valid = False

        #Making sure the password contains at least 8 characters
        if len(userData[4]) >= 8:
            valid = True

        #Ends the method if the password does not pass the first check
        if valid == False:
            return valid
        
        else:

            #Setting valid to false by default
            valid = False

            #Checks through all of the characters in the special characters list to make sure the password contains at least 1
            for character in self.special_characters:
                if character in userData[4]:
                    valid = True
            
            #Ends the method if the password does not pass the second check
            if valid == False:
                return valid
            
            else:

                #Setting valid to false by default
                valid = False

                #Checks that the password contains at least 1 number
                for character in userData[4]:
                    if character.isnumeric():
                        valid = True
        
        return valid

    #A function to check if their username already exists
    def check_username_exist(self, userData):

        #Setting the default value for valid to False 
        valid = False

        #Find the path for the database file
        dbfile = 'Data Files/UserLoginInfo.db'

        #Establishes a connection to the database
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        #Extracts the username from the entered data
        username = userData[3]

        #Extracts all of the usernames from the table that are the same
        username_list = [a for a in cur.execute(f"Select Username From LoginInfo Where Username = '{username}'")]

        #Gather all the usernames that are the same as the inputted username
        repeat_of_username = len(username_list)

        #Check if the amount of duplicates is greater than 0
        if repeat_of_username == 0:
            valid = True 

        #Close the Database
        con.close()

        #Return valid variable 
        return valid

    #A function to check if all of the data is valid, calls several other functions inside
    def check_data_validity(self, userData):

        #Checking all of the fields have data in them
        valid = True
        for field in userData:
            if len(field) == 0:
                valid = False
        
        #Checking if valid is true, so the process does not carry on if the data has alread failed its checks
        if valid  == True:
            
            #Checking if the password the User entered is valid 
            valid = self.check_password_validity(userData)

            #Checking if valid is true, so the process does not carry on if the data has alread failed its checks
            if valid == True:

                #Setting the regular expression for searching a valid email address 
                regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

                #Making sure the email is valid
                if not re.match(regex, userData[2]):
                    valid = False
                
                #Checking if valid is true, so the process does not carry on if the data has alread failed its checks
                if valid == True:

                    #Making sure the username doesn't already exist
                    valid = self.check_username_exist(userData)

                    #Submitting the data to the database if it is all valid
                    if valid == True:
                        return valid
                    
                    else:
                        #Calling the error label for an incorrect username
                        self.error_label('Graphics/Username Already Exists Error PNG File.png')
                
                else:
                    #Calling the error label for an incorrect email
                    self.error_label('Graphics/Invalid Email Address Error PNG File.png')
            
            else:
                #Calling the error label for an incorrect password
                self.error_label('Graphics/Invalid Password Error PNG File.png')
        
        else:
            #Calling the error label for empty fields
            self.error_label('Graphics/Fields Empty Error PNG File.png')
        
        return valid

    #A function to produce an error label if any of the data is invalid
    def error_label(self, errorType):

        #Calling the error label class
        DisplayError = Popup(errorType)
        DisplayError.mainloop()

    #The function that is called when the sign up button is pressed
    def sign_up_pressed(self):

        #Extracting Data from Entry Fields
        userData = [self.forename_entry.get(), self.surname_entry.get(), self.email_entry.get(), self.username_entry.get(), self.password_entry.get()]

        #Check that the data entered is valid
        valid = self.check_data_validity(userData)

        #Inputs the data into the database regarding that all of the data is valid
        if valid == True:

            #Calling the input_into_database function to enter all of the users information into the database
            self.input_into_database(userData)

            #Destroying this window to make place for the login screen
            self.destroy()

            #Calling the exit menu class to send the user to the login page
            Approved = ExitMenu('Graphics/Sign up complete PNG File.png')
            Approved.mainloop()

            #Ending the mainloop
            self.quit()

#Creating a SuperErrorClass that can cover all of the errors
class Popup(ctk.CTkToplevel):

    #Setting the Sign Up pages height and width 
    width = 600
    height = 200

    def __init__(self, ErrorType):
        super().__init__()
        
        #Setting Window Title
        self.title('SkyControl')

        #Setting Window Icon
        self.after(201, lambda :self.iconbitmap('Graphics/Logo.ico'))
        
        #Get screen dimensions
        ws = self.winfo_screenwidth() 
        hs = self.winfo_screenheight()
        
        #Setting Window Size and Placing it in the middle of the screen
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, ((ws/2)-(self.width/2)), ((hs/2)-(self.height/2))))

        #Setting Background Image
        self.image = Image.open(fr'{ErrorType}')
        self.resized_image = self.image.resize((self.width,self.height))
        self.bgimage = ImageTk.PhotoImage(self.resized_image)
        signUpImage = Label(self, image = self.bgimage)
        signUpImage.place(x=0,y=0)

        #Making the window none resizeable
        self.resizable(False,False)

        #Creating and Placing the Submit button 
        self.submit_button = ctk.CTkButton(self, 
                                            text="Ok", 
                                            font= ('Manrope', 12), 
                                            command= self.exit_window,
                                            width=100, 
                                            height=50, 
                                            corner_radius=20, 
                                            border_color= '#000000', 
                                            bg_color='#f8f8f8', 
                                            fg_color='#077fda', 
                                            text_color='#f8f8f8')
        self.submit_button.place(x=250,y=120)
    
    def exit_window(self):

        self.destroy()
        self.quit()

#Exit Window popup
class ExitMenu(ctk.CTkToplevel):
    
    #Setting the Sign Up pages height and width 
        width = 600
        height = 200

        def __init__(self,graphic):
            super().__init__()
            
            #Setting Window Title
            self.title('SkyControl')

            #Setting Window Icon
            self.after(201, lambda :self.iconbitmap('Graphics/Logo.ico'))
            
            #Get screen dimensions
            ws = self.winfo_screenwidth() 
            hs = self.winfo_screenheight()
            
            #Setting Window Size and Placing it in the middle of the screen
            self.geometry('%dx%d+%d+%d' % (self.width, self.height, ((ws/2)-(self.width/2)), ((hs/2)-(self.height/2))))

            #Setting Background Image
            self.image = Image.open(fr'{graphic}')
            self.resized_image = self.image.resize((self.width,self.height))
            self.bgimage = ImageTk.PhotoImage(self.resized_image)
            signUpImage = Label(self, image = self.bgimage)
            signUpImage.place(x=0,y=0)

            #Making the window none resizeable
            self.resizable(False,False)

            #Changing the text on the button depending on what it's doing
            if graphic == 'Graphics/Leaving Program PNG File.png':
                
                #Creating and Placing the Logout button 
                self.submit_button = ctk.CTkButton(self, 
                                                    text="Logout", 
                                                    font= ('Manrope', 12), 
                                                    command= self.exit_window,
                                                    width=100, 
                                                    height=50, 
                                                    corner_radius=20, 
                                                    border_color= '#000000', 
                                                    bg_color='#f8f8f8', 
                                                    fg_color='#077fda', 
                                                    text_color='#f8f8f8')
                self.submit_button.place(x=250,y=120)
            
            else:
                
                #Creating and Placing the Submit button 
                self.submit_button = ctk.CTkButton(self, 
                                                    text="Ok", 
                                                    font= ('Manrope', 12), 
                                                    command= self.exit_window,
                                                    width=100, 
                                                    height=50, 
                                                    corner_radius=20, 
                                                    border_color= '#000000', 
                                                    bg_color='#f8f8f8', 
                                                    fg_color='#077fda', 
                                                    text_color='#f8f8f8')
                self.submit_button.place(x=250,y=120)
        
        def exit_window(self):

            self.quit()
            self.destroy()

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

#A helper function to return the path result in an array
def return_path_list(previous_nodes, shortest_path, start_node, target_node):

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

    return path

#Running the GUI
if __name__ == "__main__":
    Main = MainMenu()
    Main.mainloop()
    
    #Executing SQL command to log everyone out
    
    #Find the path for the database
    dbfile = 'Data Files/UserLoginInfo.db'

    #Establish a connection to the database
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    #Writing SQL command 
    sql = 'UPDATE LoginInfo SET Logged_In = 0 WHERE Logged_In = 1'

    #Executing SQL command 
    cur.execute(sql)

    #Save the Database
    con.commit()

    #Close the Database
    con.close()