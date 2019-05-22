import socket, select, string, sys

import Tkinter                  #The python gui interface for Tk gui extension we 're using
import ttk                      #Module providing access to the Tk themed widget set

import threading                #Threading 



##########################Class Definitions################################

# Every object (representing a gui object..sort of) in the class has a style object associated with it for formatting, styling and beautification
# Entries are objects which appear like text boxes and we can take entries inside them,
# Labels are non modifiable objects that are just used to just mention or label other objects
# Buttons are objects that have a click functionaity which is on an event of a click can call some functions 
# .grid functions are used to position the different objects that are created the before objects
#
class Application(Tkinter.Tk):
    # Member functions definititons mostly used for GUI and the socket connections and messages are done inside 
    
    def launch_app(self):    # default function always run to generate the main 
        self.title('optichat')  #Name of our Application

        self.frame = ttk.Frame(self) # A default object frame of the Frame class of the ttk library

        self.frame.style = ttk.Style() 

        # Initial frame contains two buttons: One for registration and one for Log In
        self.reg_btn = ttk.Button(self.frame, text='New user, register here!',command = self.reg_menu)
        self.reg_btn.grid(row = 2, column = 2, padx = 40, pady = 30)
        self.client_button = ttk.Button(self.frame, text = 'Launch Client', command = self.client_menu)
        self.client_button.grid(row = 2, column = 0, padx = 40, pady = 30)
        
        # Command that integrates different objects into a single parent object.
        self.frame.pack(fill = Tkinter.BOTH, expand = True)

        self.theme_use = 'default'
        #self.lift() ##### ????????????

        self.frame.style.theme_use(self.theme_use)

        #mailoop command keeps on running this for some time continuously, else it disappears.
        self.mainloop()

    # The Registration Menu
    def reg_menu(self):
        #Previous menu's buttons destroyed
        self.client_button.destroy()
        self.reg_btn.destroy()
        
        #Entries of this frame are host, port name and password and corresponding labels and entries are created
        self.host_entry_label = ttk.Label(self.frame, text = 'Server IP Address', anchor = Tkinter.W, justify = Tkinter.LEFT)
        self.host_entry = ttk.Entry(self.frame)
        self.port_entry_label = ttk.Label(self.frame, text = 'Port Number', anchor = Tkinter.W, justify = Tkinter.LEFT)
        self.port_entry = ttk.Entry(self.frame)
        self.reg_name_label = ttk.Label(self.frame, text = 'Your name', anchor = Tkinter.W, justify = Tkinter.LEFT)
        self.reg_name_entry = ttk.Entry(self.frame)
        self.reg_pwd_label = ttk.Label(self.frame, text='Yout Password', anchor = Tkinter.W, justify = Tkinter.LEFT)
        self.reg_pwd_entry = ttk.Entry(self.frame, show = '*')

        #Register Button
        self.register_btn = ttk.Button(self.frame, text='register', command = self.reg_user)

        #Forgetting the previous packed Buttons
        self.frame.pack_forget() 
        
        self.title('optichat registration')
        
        #Positioning the labels and text boxes appropriately
        self.host_entry_label.grid(row=0, column=0, pady=10,padx=5)
        self.host_entry.grid(row=0, column=1, pady=10,padx =5)
        self.port_entry_label.grid(row=1,column=0,pady=10,padx=5)
        self.port_entry.grid(row=1,column=1,pady=10,padx=5)
        self.reg_name_label.grid(row=2,column=0,pady=10,padx=5)
        self.reg_name_entry.grid(row=2,column=1,pady=10,padx=5)
        self.reg_pwd_label.grid(row=3,column=0,pady=10,padx=5)
        self.reg_pwd_entry.grid(row=3,column=1,pady=10,padx=5)
        self.register_btn.grid(row=4,column=2,pady=10,padx=5)

        self.host_entry.focus_set()# to decide where the cursor is set

        self.frame.pack(fill= Tkinter.BOTH, expand = True)

    # Registering a new user
    def reg_user(self):
        # get function is used to call 
        self.host = self.host_entry.get()
        self.port = self.port_entry.get()
        self.port = int(self.port)
        self.username = self.reg_name_entry.get().rstrip()
        self.password = self.reg_pwd_entry.get().rstrip()

        ## delete the objects created in the frame that it was called into
        self.host_entry_label.destroy()
        self.host_entry.destroy()
        self.port_entry_label.destroy()
        self.port_entry.destroy()
        self.reg_name_label.destroy()
        self.reg_name_entry.destroy()
        self.reg_pwd_label.destroy()
        self.reg_pwd_entry.destroy()
        self.register_btn.destroy()
        self.frame.pack_forget()

        #creating socket for client and connecting with it the socket using the host IP and the host port

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.settimeout(2)
        try:
            self.conn.connect((self.host,self.port)) #Connected with the host at port number 'port'
        except:
            self.reg_menu() #create the previous window again since the connection was not successful
        
        try:
            self.conn.send(self.username + ' ' + self.password) #Sending username and password for storing in the database
        except:    
            self.reg_menu() # Failing to send the username and password

        self.client_menu()

    # The Log in menu
    def client_menu(self):
        #Preious buttons destroyed
        self.client_button.destroy()
        self.reg_btn.destroy()
        
        self.title('Log In')

        #Entries of this frame are host, port name and password and corresponding labels and entries are created
        self.host_entry_label = ttk.Label(self.frame, text = 'Server IP Address', anchor = Tkinter.W, justify = Tkinter.LEFT)
        self.host_entry = ttk.Entry(self.frame)
        self.port_entry_label = ttk.Label(self.frame, text = 'Port Number', anchor = Tkinter.W, justify = Tkinter.LEFT)
        self.port_entry = ttk.Entry(self.frame)
        self.name_entry_label = ttk.Label(self.frame, text = 'username', anchor = Tkinter.W, justify = Tkinter.LEFT)
        self.name_entry = ttk.Entry(self.frame)
        self.pwd_entry_label = ttk.Label(self.frame,text='password', anchor=Tkinter.W,justify=Tkinter.LEFT)
        self.pwd_entry = ttk.Entry(self.frame, show = '*')

        #Attempt a Log in.
        self.launch_button = ttk.Button(self.frame, text = 'Log In', command = self.launch_client)

        #Positioning the labels and text boxes appropriately
        self.host_entry_label.grid(row = 0, column = 0, pady = 10, padx = 5)
        self.host_entry.grid(row = 0, column = 1, pady = 10, padx = 5)
        self.port_entry_label.grid(row = 1, column = 0, pady = 10, padx = 5)
        self.port_entry.grid(row = 1, column = 1, pady = 10, padx = 5)
        self.name_entry_label.grid(row = 2, column = 0, pady = 10, padx = 5)
        self.name_entry.grid(row = 2, column = 1, pady = 10, padx = 5)
        self.pwd_entry_label.grid(row=3,column=0,pady=10,padx=5)
        self.pwd_entry.grid(row=3,column=1,pady=10,padx=5)
        self.launch_button.grid(row = 5, column = 1, pady = 10, padx = 5)

        self.host_entry.focus_set()

        self.frame.pack(fill=Tkinter.BOTH, expand= True)

    # Connecting to the server
    def launch_client(self):
        #Obtaining the host address and port number
        self.host = self.host_entry.get()
        self.port = self.port_entry.get()
        self.port = int(self.port)
        self.name = self.name_entry.get()
        self.pwd = self.pwd_entry.get()

        #Destroying the previous labels and entries
        self.host_entry_label.destroy()
        self.host_entry.destroy()
        self.port_entry_label.destroy()
        self.port_entry.destroy()
        self.name_entry_label.destroy()
        self.name_entry.destroy()
        self.pwd_entry_label.destroy()
        self.pwd_entry.destroy()

        self.launch_button.destroy()
        self.frame.pack_forget()

        #creating socket for client
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.settimeout(2)
        try:
            self.conn.connect((self.host,self.port)) #Attempting to connect to the server
        except:
            self.client_menu() #Authentication failure

        self.list_of_active_user = self.initial_setup() #Obtaining the list of active users on successful connection to the user

        #########################layout details####################
        self.title('OptimumClient '+self.name) #Window title

        self.should_quit = False   

        self.protocol('WM_DELETE_WINDOW', self.client_quit) ###?????

        self.chat_frame = ttk.Frame(self.frame, borderwidth = 5)    #for the actual display of chat
        self.clients_frame = ttk.Frame(self.frame)                  #for radio buttons
        self.entry_frame = ttk.Frame(self)                          #for input text

        ########## Stylising ############## 
        self.chat_frame.style = ttk.Style()
        self.chat_frame.style.theme_use(self.theme_use)
        #########
        self.clients_frame.style = ttk.Style()
        self.clients_frame.style.theme_use(self.theme_use)
        #########   
        self.entry_frame.style = ttk.Style()
        self.entry_frame.style.theme_use(self.theme_use)
        ####################################

        #state indicates the chat history so far, and is uneditable
        self.chat_text = Tkinter.Text(self.chat_frame, state = Tkinter.DISABLED) 

        self.chat_entry = ttk.Entry(self.entry_frame)                       #Text box for sending messages
        self.send_button = ttk.Button(self.entry_frame, text = 'Send')      #For actually sending the messages

        self.send_button.bind('<Button-1>', self.send)                      #press button-1 to send messages
        self.chat_entry.bind('<Return>', self.send)                         #Alternate to sending messages, hitting the return button

        #Packing the above created objects and giving them positions while packing
        self.entry_frame.pack(side = Tkinter.BOTTOM, fill = Tkinter.X)
        self.frame.pack(side = Tkinter.TOP, fill = Tkinter.BOTH, expand = True)
        self.clients_frame.pack(side = Tkinter.LEFT, fill = Tkinter.BOTH, expand = True)
        self.chat_frame.pack(side = Tkinter.RIGHT, fill = Tkinter.BOTH, expand = True)

        self.chat_entry.pack(side = Tkinter.LEFT, fill = Tkinter.X, expand = True)
        self.send_button.pack(side = Tkinter.RIGHT)

        self._i = 1
        self.dest = Tkinter.StringVar() #shared variable of type string for radio buttons
        #Radio buttons for the list of active users
        self.radios = []

        self.radio_label = ttk.Label(self.clients_frame,
                    width = 15,
                    wraplength = 125,
                    anchor = Tkinter.W,
                    justify = Tkinter.LEFT,
                    text = 'Choose receiver from the following connected clients:')

        self.radio_label.pack()
        self.chat_text.pack(fill = Tkinter.BOTH, expand = True)
        #############################################################   
        
        ## For the default broadcast option:
        r0 = ttk.Radiobutton(self.clients_frame, text = "Broadcast", variable = self.dest, value = "broadcast")
        r0.pack(anchor = Tkinter.W)
        self.radios.append(r0)

        # Radio buttons for the various options:
        for client in self.list_of_active_user:
            #self.dest is shared variable of radio buttons
            #Variable self.dest assigned 'value=client' when radio button 'r' is selected
            r = ttk.Radiobutton(self.clients_frame, text = client, variable = self.dest, value = client)
            r.pack(anchor = Tkinter.W)
            #Appending the radio button 'r' to the list of Radio Buttons
            self.radios.append(r)

        self.dest.set(self.list_of_active_user[0]) #initialised for common variablle of radios 

        self.chat_entry.focus_set()

        #for client we will intiate a thread to display chat
        self.clientchat_thread = threading.Thread(name = 'clientchat', target = self.clientchat)
        self.clientchat_thread.start()
            
    #Sending the message according to the format specified in server.py and updating the chat history area
    def send(self,event):
        message = self.chat_entry.get()
        dest = self.dest.get()
        if (dest == "broadcast"):
            data = message            
            self.chat_entry.delete(0, Tkinter.END)     #input box empty after send
            
            self.conn.send(data.encode())               #Sending the encoded data to the server
            self.chat_text.config(state = Tkinter.NORMAL) #Enabling the edit functionality of the chat text in order to edit it
            self.chat_text.insert(Tkinter.END, data+'\n',('tag{0}'.format(2))) #Insert the message sent into the chat hitory
            self.chat_text.tag_config('tag{0}'.format(2),justify=Tkinter.RIGHT,foreground='black')
            self.chat_text.config(state = Tkinter.DISABLED) #Again Disabling the edit functionality so that the user cannot edit it
            self.chat_text.see(Tkinter.END) #Enables the user to see the edited chat history
        else:
            data = '@'+dest+':'+message
            self.chat_entry.delete(0, Tkinter.END)      #input box empty after send
            self.conn.send(data.encode())               #Sending the encoded data to the server
            self.chat_text.config(state = Tkinter.NORMAL) #Enabling the edit functionality of the chat text in order to edit it
            self.chat_text.insert(Tkinter.END, data+'\n',('tag{0}'.format(3))) #Insert the message sent into the chat hitory
            self.chat_text.tag_config('tag{0}'.format(3),justify=Tkinter.RIGHT,foreground='black')
            self._i = self._i + 1
            self.chat_text.config(state = Tkinter.DISABLED) #Again Disabling the edit functionality so that the user cannot edit it
            self.chat_text.see(Tkinter.END) #Enables the user to see the edited chat history

    #Chatting time!
    def clientchat(self):
        while not self.should_quit:     #If we are not in the 'quit' state then do :
            try:
                data = self.conn.recv(4096) #Receive and decode the data
                data = data.decode()

                if len(data): #If there is data
                    #if there is an active user message received then it means a new 
                    #user has logged in and we need to update radios
                    if data[0] == "!":
                        self.list_of_active_user = data[1:].split(' ')

                        #Destroying the previous radios
                        for r in self.radios:
                            r.destroy()

                        #Updating the new radio list
                        for client in self.list_of_active_user:
                            r = ttk.Radiobutton(self.clients_frame, text = client, variable = self.dest, value = client)
                            r.pack(anchor = Tkinter.W)
                            self.radios.append(r)

                    #it's not an activelist msg
                    else:
                        #Updating the chat history based on the new message received
                        self.chat_text.config(state = Tkinter.NORMAL)
                        self.chat_text.insert(Tkinter.END, data[1:]+'\n',('tag{0}'.format(2)))
                        self.chat_text.tag_config('tag{0}'.format(2),justify=Tkinter.LEFT,foreground='red')
                        self.chat_text.config(state = Tkinter.DISABLED)
                        self.chat_text.see(Tkinter.END)
                else:
                    break
            except:
                continue

    def initial_setup(self):
        #allow for it to communicate with server only once for 
        #the first time  till it gets the list of active users
        got_list = False
        list_of_active_user = []
        
        try:
            self.conn.send('0'.encode())    #Sending 0 to indicate that it is a non-registration message
        except:
            #Closing the connection and giving an option to reattempt 
            self.conn.close()
            self.wp_error = ttk.Label(self.frame, text='Cannot Connect to Server', anchor = Tkinter.CENTRE,justify = Tkinter.CENTER)
            self.try_again = ttk.Button(self.frame, text='Try again', command = self.client_menu)
            self.wp_error.grid(row = 0, column=1, pady=10, padx=5)
            self.try_again.grid(row=0,column=1,pady=10,padx=5)
            self.frame.pack(fill=Tkinter.BOTH, expand = True)

        while 1:
            if not got_list:
                try:
                    data = self.conn.recv(4096) #Obtaining the list of all the active users
                    data = data.decode()
                except:
                    self.conn.close()
                    self.client_menu()
                
                if data == "What is your name?": #Getting the first message from the server
                    try:
                        self.conn.send((self.name+' '+self.pwd).encode())   #Sending the name and password to the server
                    except:
                        self.conn.close()
                        self.client_menu()    
                    try:
                        list_of_active_user = self.conn.recv(4096).decode() #this will be a string of name separated by spaces
                    except:
                        self.conn.close()
                        self.client_menu() 
                    if list_of_active_user == 'authentication_error':   
                        #Authentication error implies that user is either not registered or password is incorrect. Redirecting to the Client menu
                        self.wp_error = ttk.Label(self.frame, text='Authentication_Error', anchor = Tkinter.CENTER,justify = Tkinter.CENTER)
                        self.try_again = ttk.Button(self.frame, text='Try again', command = self.client_menu)
                        self.wp_error.grid(row = 0, column=1, pady=10, padx=5)
                        self.try_again.grid(row=0,column=1,pady=10,padx=5)
                        self.frame.pack(fill=Tkinter.BOTH, expand = True)

                        # self.conn.close()
                        # self.client_menu()
                    list_of_active_user = list_of_active_user[1:].split(' ') #now it has all the names separately, its not a string
                    got_list = True
            else:
                return list_of_active_user
            
    #Closing down the thread and shutting down the connection
    def client_quit(self):
        self.should_quit = True
        self.conn.shutdown(socket.SHUT_WR)
        self.clientchat_thread.join()
        self.conn.close()
        self.destroy()


# def terminal_client:


#main function
if __name__ == '__main__':


	# if(len(sys.argv) < 1):

	app = Application()

	app.launch_app()            #Launching the app

#   	elif (len(sys.argv) = 	4):

# 	else:
		

# 	def prompt() :
#     	sys.stdout.write('<You> ')
#     	sys.stdout.flush()
 		     
    	
#     host = sys.argv[1]
#     port = int(sys.argv[2])
     
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.settimeout(2)
     
#     # connect to remote host
#     try :
#         s.connect((host, port))
#     except :
#         print ('Unable to connect\n')
#         sys.exit()
     
# #    prompt()

#     while 1:
#         socket_list = [sys.stdin, s]
         
#         # Get the list sockets which are readable
#         read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
#         for sock in read_sockets:
#             #incoming message from remote server
#             if sock == s:
#                 data = sock.recv(4096)
#                 if not data :
#                     print ('\nDisconnected from chat server\n')
#                     sys.exit()
#                 else :
#                     sys.stdout.write(data.decode())	
             
#             #user entered a message
#             else :
#                 msg = sys.stdin.readline()
#                 s.send(msg.encode())
#                 #prompt()


