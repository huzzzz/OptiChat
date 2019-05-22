# Import all from module socket
from socket import *
#Importing all from thread
from _thread import *
import sys
import netifaces as ni

#For python3, decode is required after receiving messages and encode before sending messages (part of string library)
#for every action , we have used try and except for error catching

################## the function definitions ########################
def clientthread(conn,addr): #Common client function for each socket connection
	try:
		type_msg = conn.recv(RECV_BUFFER) #initital msg type to distinguish between non registration and registration messages
		type_msg = type_msg.decode()  #to convert encoded received msg to string
	except:
		conn.close()
		sys.exit()		

	if type_msg =='0': #If initial message is '0' then, non reg msg
		
		first_time = True   #When msg sent for first time after connection, name and pwd req for authentication, this maintains the state
		name_enter = False

		#infinite loop so that function do not terminate and thread do not end.
		while True:
			#Sending message to connected client
			if first_time == True:
				instr = 'What is your name?'
				conn.send(instr.encode()) 
				first_time = False
				name_enter = True
			else:
				if name_enter:
					name_pwd = conn.recv(RECV_BUFFER) #Receiving name and password from the client for authentication
					name_pwd = name_pwd.decode() 
					name_pwd = name_pwd.rstrip().split(' ') #The msg format : <name> <password>. This processes it to return an array 
					name = name_pwd[0]	#this is the name of the newly connected client
					pwd = name_pwd[1]	#this is the password of the newly connected client

					if authenticate(name,pwd): #If authenticated,i.e, present in local db, then do this
						#store this in local database
						USERS_LIST[name]=conn 	#Maps the name to the socket
						SOCK_LIST[conn]=name  	#Maps the socket to the name
						print(name+" logged in")
						name_enter = False
						
						active_list="!"			#The first letter of the active list is a '!' for telling the client side that this is an active list being sent
						for socket in SOCK_LIST:
							if socket != conn:
								active_list = active_list+SOCK_LIST[socket] + " "	#Adding to the active list names of all active users (represented by SOCK_LIST[socket])
						try:
							active_list = active_list + name  #The name of the client itself should be at the end
							conn.send(active_list.encode()) #Sending the active list to the just logged in client
							broadcast_data(conn,active_list) #Sending the active list to all other clients
						except:									#Usual Error Handling
							conn.close()							#If there's any error encountered, then:
							del(USERS_LIST[SOCK_LIST[conn]])		#Remove the name from the USERS_LIST
							del(SOCK_LIST[conn])					#Remove the socket from the SOCK_LIST
							sys.exit()								#Exit , i.e. end the thread for this client socket
					else:
						conn.send('authentication_error'.encode())	#If authentication fails, i.e user-password not found, then 
						conn.close() 	#close the socket
						sys.exit()

				else:			#If authentication done, then normal chatting, do this:
					try:
						data = conn.recv(RECV_BUFFER) #Receiving the data in encoded form from the client
						data = data.decode()	#Decoding the received data to string
					except:					#Usual Error Handling
						conn.close()
						del(USERS_LIST[SOCK_LIST[conn]])
						del(SOCK_LIST[conn])
						sys.exit()

					#checking if we have to end the connection, corresponding msg to the exit sequence is data
					if data == "#!quit":
						conn.send('Connection shutting down with server\n'.encode())
						print('Connection shutting down with ',name,'\n')
						conn.close() 		#usual steps to end the connection
						del(USERS_LIST[SOCK_LIST[conn]])
						del(SOCK_LIST[conn])
						sys.exit()
					else:
						#appropriate actions to take depending on the message
						try:
							if data[0] != '@':	#If this msg does not start with @ , then it is broadcast
								broadcast_data(conn, "\r" + '<' + SOCK_LIST[conn] + '> ' + data) 
							else:				#Processing a multicast msg
								temp = data.split(':') #format: @<user1> @<user2>... : <msg>
								temp2 = temp[0][1:].split('@')
								list_of_names = list(map(lambda x: x.rstrip(), temp2))
								list_of_socks = list(map(lambda x : USERS_LIST[x], list_of_names))
								multicast_data(conn, list_of_socks, "\r" + SOCK_LIST[conn] + ':' + ':'.join(temp[1:]))
														
						except:
							broadcast_data(conn, "Client (%s, %s) is offline" % addr)		#To inform all about the user going offline
							print ("Client (%s, %s) is offline" % addr)
							conn.close() #Usual closing
							del(USERS_LIST[SOCK_LIST[conn]])
							del(SOCK_LIST[conn])
							sys.exit()
	else:
		#this is a registraion message
		#so the client is expected to directly send the user name and pwd
		name_pwd = type_msg.rstrip().split(' ')
		name = name_pwd[0]
		pwd = name_pwd[1]
		reg_user(name, pwd)
		conn.close()
		sys.exit()


#authenticating from the database
def authenticate(uname, pwd):
    is_valid = False
    with open('database.txt','r') as f:
        for line in f:
            if uname+' '+pwd+'\n' == line:
                is_valid = True
                return is_valid
        else:
            return is_valid


#Adding a new user to the database
def reg_user(uname,pwd):
    #we will now open /update file to maintain a database
    fo = open('database.txt','a')
    fo.write(uname+' '+pwd+'\n')
    fo.close()



#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
	#Do not send the message to master socket and the client who has send us the message
	for socket in SOCK_LIST:
		if  socket != sock:
			try :
				socket.send(message.encode())
			except :
				# broken socket connection may be, chat client pressed ctrl+c for example
				socket.close()
				del(USERS_LIST[SOCK_LIST[socket]])
				del(SOCK_LIST[socket])


#Function to send a message to one or more users depending on the list of sockets
def multicast_data(sock, list_of_sock,message):
	for socket in list_of_sock:
			#Do not send the message to master socket and the client who has send us the message
		if socket ifn SOCK_LIST:
			try:
				socket.send(message.encode())
			except:
				socket.close()
				del(USERS_LIST[SOCK_LIST[socket]])
				del(SOCK_LIST[socket])
		elif socket != sock:
			try:
				sock.send("oops USER NOT PRESENT!\n".encode()) 
			except: #usual error handling
				sock.close()
				del(USERS_LIST[SOCK_LIST[sock]])
				del(SOCK_LIST[sock])
				sys.exit()	

#the main function
if __name__ == "__main__":

	if(len(sys.argv) < 2):
		print ('Usage : python3 server.py port')
		sys.exit()

	#Creating socket object
	sock = socket()
	# Defining server address and port
	ni.ifaddresses('wlp3s0')
	host = ni.ifaddresses('wlp3s0')[2][0]['addr']
	# host = "27.11.19.117"  #'localhost' or '127.0.0.1' or '' are all same
	port = int(sys.argv[1]) #Use port > 1024, below it all are reserved
	 

	#Binding socket to a address. bind() takes tuple of host and port.
	sock.bind((host, port))
	#Listening at the address
	sock.listen(15) #5 denotes the number of clients can queue

	RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
	 
	# Add server socket to the list of readable connections
	USERS_LIST = dict() #A map of all active users' names to sockets
	SOCK_LIST = dict()	#A map of all active users' sockets to names 
 
	print ("Chat server started on port " + str(port))
 
	while 1:
		#Accepting incoming connections
		conn, addr = sock.accept()
		#Creating new thread. Calling clientthread function for this function and passing conn as argument.
		start_new_thread(clientthread,(conn,addr)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
 
sock.close() #close socket after all is done
