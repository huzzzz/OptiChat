#include <iostream>
#include <bits/stdc++.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>
#include <netdb.h>

using namespace std;

int main(){
	int clientFD; //to store the file descriptor of the open socket
	int port = 8888;
	int buffsize = 1024;
	char buffer[buffsize];
	char* ip = "192.168.0.103";
	bool stop = false; //handle to stop the conversation

	//now to make a socket for the server
	struct sockaddr_in serverAddr;

	clientFD = socket(AF_INET, SOCK_STREAM, 0); //AF is address domain of the socket

	if (clientFD < 0){
		cout<<"\n=> Error establishing socket!!!"<<endl;
		exit(1);
	}else{
		cout<<"\n=> Socket created successfully!"<<endl;
	}
	
	//filling the server info in the struct
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = inet_addr(ip);
	serverAddr.sin_port = htons(port);
	
	if(connect(clientFD, (sockaddr *) &serverAddr, sizeof(serverAddr)) == 0){
		cout <<"\n=> Connection to the server port number: "<<port<<endl;
	}
	else{
		cout<<"\n=> Connection to server failed."<<endl;
		exit(1);
	}

	cout<<"\n=> Awaiting confirmation from the server..."<<endl;
	int n = read(clientFD,buffer,buffsize);
	if(n<0){
		cout<<"=> Error reading from the socket"<<endl;
	}
	else{
		cout<<buffer<<endl;
		cout<<"Enter # to stop connection."<<endl;

		//int count=5;
		do{
			bzero(buffer,buffsize);
			
			cout<<"\nClient: ";
			fgets(buffer,buffsize,stdin);
			n = write(clientFD,buffer,strlen(buffer));
			if(n<0){
				cout<<"=> Error writing on socket"<<endl;
				exit(1);
			}else{
				n = read(clientFD,buffer,buffsize);
				if(n<0){
					cout<<"=> Error reading on socket"<<endl;
					exit(1);
				}
				else{
					cout<<"Server: ";
					cout<<buffer<<endl;

					if(*buffer == '#'){
						*buffer = '*';
					}
				}
			}
			//count--;
		}while(*buffer != '*');
	}
	
	//tear down phase
	cout<<"\n=> Connection terminated."<<endl;
	close(clientFD);
	return 0;
}