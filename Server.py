# python server

from audioop import add
from logging import exception
from pickle import NONE
import socket
from threading import *


class client(Thread):
    conn = NONE
    addr = NONE
    user = NONE

    def run(self):

        self.conn.sendall("please enter a username \n".encode())
        uname = self.conn.recv(1024).decode().strip().encode()
        while True:
            if uname in clients:
                self.conn.sendall("please pick a different name\n".encode())
                uname = self.conn.recv(1024).decode().strip().encode()
            else:
                clients[uname] = self
                break

        self.user = uname
        print("User name added", self.user)
        clients[self.user] = self
        self.handelMessages()

    def handelMessages(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            # if data.decode().startswith('/quit'):
            #     clients.pop(self.user)
            #     self.sendMsg(self.user + " Has left the server".encode())
            #     self._stop()
            self.sendMsg(self.user + ": ".encode()+data)

    def sendMsg(self, data):
        for key in clients:
            if clients[key] != self:
                clients[key].conn.sendall(data)

    def create(self, conn, addr):
        self.conn = conn
        self.addr = addr


clients = {}


class Server:

    def main():
        clients.clear()
        print("running")
        HOST = 'localhost'
        PORT = 2000
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            print("Bind successfull")
            s.listen()
            print("listeing")
            while True:
                conn, addr = s.accept()
                try:
                    print(f"Connected by {addr}")
                    Client = client()  # creates a new client object to start a new thread
                    # adds the connecection and address of the connection to the client
                    Client.create(conn, addr)
                    Client.start()  # starts the thread
                except:
                    print(exception)
        except:
            print(exception)


Server.main()
