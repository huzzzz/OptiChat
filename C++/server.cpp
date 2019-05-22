#include <iostream>
#include <bits/stdc++.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>

using namespace std;

int main(){
	int clientFD, serverFD;
	int port = 8888;
	int stop = false;
	int buffsize = 1024;
	char buffer[buffsize];
	char* ip = "192.168.0.103"; //my private ip in my hostel room.


	struct sockaddr_in serverAddr, clientAddr;
	socklen_t size;

	serverFD = socket(AF_INET, SOCK_STREAM, 0);

	if (serverFD < 0){
		cout<<"\n=> Error establishing socket!!!"<<endl;
		exit(1);
	}else{
		cout<<"\n=> Socket created successfully!"<<endl;
	}
	
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = INADDR_ANY; //this will automatically fill the IP of the host at which server.cpp is running// inet_addr(ip);
	serverAddr.sin_port = htons(port);

	if((bind(serverFD, (struct sockaddr*) &serverAddr, sizeof(serverAddr))) < 0){
		cout<<"=> Error binding connection, the socket has already been established..."<<endl;
		return -1;
	}
	else{
		cout<<"=> The server socket binded..."<<endl;
		cout << "=> Looking for clients..." << endl;
	}
	
	//listening call
	// This listen() call tells the socket to listen to the incoming connections.
    // The listen() function places all incoming connection into a backlog queue
    // until accept() call accepts the connection.
	listen(serverFD, 5);
	int clientcount = 5;

	size = sizeof(clientAddr);
	// accept() writes in struct clientAddr info of new accepted client
	// while listening on serverFD and returns a socket id which I store in
	// clientFD
	clientFD = accept(serverFD, (struct sockaddr*) &clientAddr, &size);

	if(clientFD < 0){
		 cout << "=> Error on accepting..." << endl;
	}else{
		cout<<"=> New client accepted..."<<endl;
		cout<<"=> Client IP: "<<inet_ntoa(clientAddr.sin_addr)<<endl;
		cout<<"=> Client Port: "<<ntohs(clientAddr.sin_port)<<endl<<endl;
	}
	//sending the first message to indicate that the connection is established
	strcpy(buffer, "=> Server is connected...\n");
	send(clientFD,buffer,buffsize,0);
	bzero(buffer,buffsize);
	
	while(clientFD > 0){
		//int count = 5;
		cout<<"Enter # to stop connection."<<endl<<endl;;
		do{
			bzero(buffer,buffsize);
			int n = read(clientFD,buffer,buffsize);
			if(n<0){
				cout<<"=> Error reading from socket"<<endl;
				exit(1);
			}
			else{
				cout<<"Client: ";
				cout<<buffer<<endl;
				if(*buffer == '#'){
					*buffer = '*';
				}
				else{
					bzero(buffer,buffsize);
					cout<<"\nServer: ";
					fgets(buffer,buffsize,stdin);
					n = write(clientFD,buffer,buffsize);
					if(n<0){
						cout<<"=> Error writing on the socket"<<endl;
						exit(1);
					}
					if(*buffer == '#'){
						*buffer = '*';
					}
				}				
			}
			//count--;
		}while(*buffer != '*');	

		cout << "\n\n=> Connection terminated with IP " << inet_ntoa(clientAddr.sin_addr)<<endl;
		close(clientFD);
		//stop = false;
		exit(1);
	}

	close(serverFD);
	return 0;
}