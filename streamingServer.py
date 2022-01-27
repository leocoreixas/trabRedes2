import base64
import socket
import threading
import os
import time
from _thread import *
import cv2
import pickle
import struct
import imutils
import pyglet
import pyaudio

class Server:
    """
    Servidor. Responsável por receber e tratar dados.
    """

    def __init__(self):
        self.clients = []
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 6028
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        orig = (HOST, PORT)
        self.udp.bind(orig)
        print("Socket criado" + str(HOST) + " | " + str(PORT))
        self.BUFFER = 1024

    def init_server(self):
        """
        Inicia o servidor.
        """
        print("Iniciando servidor")

        while True:
            msg, client = self.udp.recvfrom(self.BUFFER)
            print(client, str(msg))
            if "REPRODUZIR_VIDEO" in msg.decode():

                #TODO: Chamar novo server e testar se dá bom
                #TODO: Retornar vídeo ou error

                id = msg.decode().split(";")[1]
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                HOST = "127.0.0.1" # IP - serviceServer
                PORT = 6011 # Port - serviceServer
                tcp.connect((HOST, PORT))
                tcp.send(("GET_USER_INFORMATION;" + id).encode())
                msgTcp = tcp.recv(1024).decode()

                if msgTcp.split(";")[1] == "2" or  msgTcp.split(";")[1] == "1":
                    #Tem permissão
                    self.udp.sendto(("RESPOSTA;“REPRODUZINDO O VÍDEO: " + str(msg[2]) + " COM RESOLUÇÃO NOMENCLATURA DA RESOLUÇÃO;0").encode(), client)
                    thread = threading.Thread(target=self.sendVideo, args=(client, msg.decode().split(";")[2],))
                    thread.start()
                else:
                    #Não tem permissão
                    self.udp.sendto("RESPOSTA;NÃO TEM PERMISSÃO PARA REPRODUZIR VÍDEOS, POR FAVOR MUDE SUA CLASSIFICAÇÃO;-1".encode(), client)


    def sendVideo(self, client, path):
        try:

            print(" ----------------" +path)
            video = cv2.VideoCapture(path)
            fps = int(video.get(cv2.CAP_PROP_FPS))
            i = 0  # frame counter
            frameTime = 10  # time of each frame in ms.

            while (video.isOpened()):
                ret = video.grab()  # grab frame
                i = i + 1  # increment counter
                #if i % 3 == 0:  # display only one third of the frames
                   #ret, frame = video.retrieve()  # decode frame
                _, frame = video.read()
                if _ == True:
                    time.sleep(1 / fps)

                    frame = imutils.resize(frame, width=600, height=400)
                    encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

                message = base64.b64encode(buffer)
                self.udp.sendto(message, client)
            video.release()
            cv2.destroyAllWindows()
            self.udp.sendto("end_video".encode(), client)
        except:
            pass

server = Server()
server.init_server()
