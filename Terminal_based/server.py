# Import all from module socket
from socket import *
#Importing all from thread
from _thread import *
import sys

################## the function definitions ########################
def clientthread(conn,addr):
	#infinite loop so that function do not terminate and thread do not end.
	first_time = True
	name_enter = False
	
	while True:
		#Sending message to connected client
		if first_time == True:
			instr = 'What is your name?'
			conn.send(instr.encode())
			first_time = False
			name_enter = True
		else:
			if name_enter:
				name = conn.recv(RECV_BUFFER)
				name = name.decode() #this is the name of the newly connected client
				name = name.rstrip() 
				#store this in database
				USERS_LIST[name]=conn
				SOCK_LIST[conn]=name
				print(name+" logged in")
				name_enter = False
				
				active_list="!"
				for socket in SOCK_LIST:
					if socket != conn:
						active_list = active_list+SOCK_LIST[socket] + " "
				try:
					active_list = active_list + name
					conn.send(active_list.encode())
					broadcast_data(conn,active_list)
				except:
					conn.close()
					del(USERS_LIST[SOCK_LIST[conn]])
					del(SOCK_LIST[conn])
					sys.exit()

			else:
				#Receiving from client
				try:
					data = conn.recv(RECV_BUFFER)
					data = data.decode()
				except:
					conn.close()
					del(USERS_LIST[SOCK_LIST[conn]])
					del(SOCK_LIST[conn])
					sys.exit()

				#checking if we have to end the connection
				if data == "#\n":
					conn.send('Connection shutting down with server\n'.encode())
					print('Connection shutting down with ',name,'\n')
					conn.close()
					del(USERS_LIST[SOCK_LIST[conn]])
					del(SOCK_LIST[conn])
					sys.exit()
				else:
					#appropriate actions to take depending on the message
					try:
						if data[0] != '@':
							broadcast_data(conn, "\r" + '<' + SOCK_LIST[conn] + '> ' + data) 
						else:
							temp = data.split(':')
							temp2 = temp[0][1:].split('@')
							# localname=temp[0][1:].rstrip()
							# print(temp2)
							list_of_names = list(map(lambda x: x.rstrip(), temp2))
							# print(list_of_names)
							
							list_of_socks = list(map(lambda x : USERS_LIST[x], list_of_names))
							
							print(list_of_socks)
							multicast_data(conn, list_of_socks, "\r" + SOCK_LIST[conn] + ':' + ':'.join(temp[1:]))
													
					except:
						broadcast_data(conn, "Client (%s, %s) is offline" % addr)
						print ("Client (%s, %s) is offline" % addr)
						conn.close()
						del(USERS_LIST[SOCK_LIST[conn]])
						del(SOCK_LIST[conn])
						sys.exit()


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

#Function to send chat message to a particular client
# def unicast_data (name, message):
# 	try:
# 		USERS_LIST[name].send(message.encode())
# 	except:
# 		USERS_LIST[name].close()
# 		del(SOCK_LIST[USERS_LIST[name]])
# 		del(USERS_LIST[name])

def multicast_data(sock, list_of_sock,message):
	for socket in list_of_sock:
		if socket != sock and socket in SOCK_LIST:
			try:
				socket.send(message.encode())
			except:
				socket.close()
				del(USERS_LIST[SOCK_LIST[socket]])
				del(SOCK_LIST[socket])
		elif socket != sock:
			try:
				sock.send("oops USER NOT PRESENT!\n".encode())
			except:
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
	host = "10.196.6.15"  #'localhost' or '127.0.0.1' or '' are all same
	# host = socket.gethostbyname(socket.gethostname())
	port = int(sys.argv[1]) #Use port > 1024, below it all are reserved
	 

	#Binding socket to a address. bind() takes tuple of host and port.
	sock.bind((host, port))
	#Listening at the address
	sock.listen(15) #5 denotes the number of clients can queue

	RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
	 
	# Add server socket to the list of readable connections
	USERS_LIST = dict()
	SOCK_LIST = dict()
 
	print ("Chat server started on port " + str(port))
 
	while 1:
		#Accepting incoming connections
		conn, addr = sock.accept()
		#Creating new thread. Calling clientthread function for this function and passing conn as argument.
		start_new_thread(clientthread,(conn,addr)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
 
sock.close()
