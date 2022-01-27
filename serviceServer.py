import base64
import socket
import threading
import os
from _thread import *
import cv2
import pickle
import struct
import imutils
import tkinter as tk
from tkinter import messagebox
class ServiceServer :

    def __init__(self):
        self.clients = []
        # self.HOST = socket.gethostbyname(socket.gethostname())
        self.HOST = "127.0.0.1"
        self.PORT = 6011
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.orig = (self.HOST, self.PORT)
        self.tcp.bind(self.orig)
        self.tcp.listen(5)

        print("Servidor Iniciado" +str(self.HOST))

    # def in_communication(self, client, connection):
    #     while True:
    #         msg = connection.recv(1024).decode()
    #         if msg == "./videos/homem_aranha_720p.mov":


    def start_Server(self) :
        try:
            """
            Main loop do servidor. Fica aguardando novas conexões
            """
            tkWindow1 = tk.Tk()
            tkWindow1.geometry('200x250')
            tkWindow1.title('Informações do Usuário')
            text = tk.Text(tkWindow1)
            while True:
                con, client = self.tcp.accept()
                msg = con.recv(1024).decode()

                if "GET_USER_INFORMATION" in msg:
                    id = msg.split(";")[1]
                    for client in self.clients:
                        if(client[2] in id):
                            text.insert(tk.INSERT, "nome:" + client[2] + "tipo do perfil:" + client[3])
                            print("nome:" + client[2] + "tipo do perfil:" + client[3])
                            con.send(("USER_INFORMATION;"+client[3]).encode())
                else:
                    msg = msg.split(";")
                    self.clients.append((con, client, msg[0], msg[1]))
        except KeyboardInterrupt as e:
            print("Servidor finalizado pelo teclado")
        except Exception as e:
            print("Error: " + str(e))

server = ServiceServer()
server.start_Server()