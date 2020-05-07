from tkinter import *
import threading
import socket 
import select 
import sys 
from requests import get

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

IP_address = "3.12.58.153"
Port = 12000


class Application:
    def __init__(self, master):
        self.master = master
        self.master.title('NetChat')
        self.textArea = Text(root, height=20, width=100)
        self.scrollbar = Scrollbar(root)
        self.scrollbar.config(command=self.textArea.yview)
        self.textArea.config(state='disabled', yscrollcommand=self.scrollbar.set)

        self.textArea.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1)
        self.entry = Entry(master, width=100)
        self.entry.grid(row=1, column=0)
        self.enterButton = Button(master, text="Enter", command=self.sendMessage).grid(row=1, column=1)

        self.entry.focus_set()

        self.textArea.config(state='normal')
        self.textArea.insert(END, "Connecting...\n")
        self.textArea.config(state='disabled')
        try:
            server.connect((IP_address, Port)) 
        except socket.error as err:
            self.textArea.config(state='normal')
            self.textArea.insert(END, err)
            self.textArea.config(state='disabled')


    def sendMessage(self):
        self.textArea.config(state='normal')
        message = self.entry.get()
        if(message == "{exit}"):
                root.quit()
        message = self.entry.get() + '\n'
        server.send(message.encode())
        ip = get('https://api.ipify.org').text
        self.textArea.insert(END, ip + ': ' + message)
        self.entry.delete(0, 'end')

        self.textArea.config(state='disabled')

    def printMessage(self, receieved):
        self.textArea.config(state='normal')
        self.textArea.insert(END, receieved)
        self.textArea.config(state='disabled')

terminateProgram = False

def echo_data(sock):
    while True:
        try:
            if(terminateProgram == True):
                break
            received = sock.recv(1024).decode()
            app.printMessage(received)
        except OSError:
            break
        
        

root = Tk()
app = Application(root)
root.bind('<Return>', lambda event=None: app.sendMessage())
t1 = threading.Thread(target=echo_data, args = (server,))
t1.start()
root.mainloop()
terminateProgram = True
t1.stop = True
server.close()
root.destroy()
