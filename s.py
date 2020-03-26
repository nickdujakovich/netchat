import socket 
import select 
import sys 
from thread import *
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 



IP_address = "0.0.0.0"
print("My IP: " + IP_address)
Port = 12000
  
server.bind((IP_address, Port)) 

server.listen(10) 
  
clientlist = [] 
  
def clientthread(conn, addr): 
  
    conn.send("Welcome to NetChat!")
    conn.send("Type {exit} to disconnect.\n") 
  
    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 

                    print addr[0] + ": " + message 
                    message_to_send = addr[0] + ": " + message 
                    broadcast(message_to_send, conn) 
  
                else: 
                    remove(conn) 
            except: 
                continue
  
def broadcast(message, connection): 
    for clients in clientlist: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
                remove(clients) 
  
def remove(connection): 
    if connection in clientlist: 
        print(connection.getpeername()[0] + " on port " + connection.getpeername()[1] + "has disconnected.")
        list_of_clients.remove(connection) 
  
while True: 
  
    conn, addr = server.accept() 
  
    clientlist.append(conn) 
  
    print addr[0] + " connected"
  
    start_new_thread(clientthread,(conn,addr))     
  
conn.close() 
server.close() 