import socket 
import select 
import sys 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


IP_address = "3.12.58.153"
Port = 12000
print("Connecting...")
server.connect((IP_address, Port)) 

while True: 

    sockets_list = [sys.stdin, server] 
    read_sockets,write_socket,error_socket = select.select(sockets_list,[],[]) 

    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print(message)
        else:
            message = raw_input()
            if(message == "{exit}"):
                server.close()
            server.send(message)
            print("You: " + message)

server.close() 

#oserror winerror 10038 an operation was attempted on something that is not a socket