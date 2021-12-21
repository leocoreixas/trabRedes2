import base64
import socket
import threading
import os
from _thread import *
import cv2
import pickle
import struct
import imutils


class Server:
    """
    Servidor de ligação. Responsável por receber e tratar dados e chamadas.
    """

    def __init__(self):
        self.clients = []
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 6013
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
            if "connect" in msg.decode():
                self.clients.append(client)

                print(self.clients)
                thread = threading.Thread(target=self.sendVideo, args=(client,))
                thread.start()

    def sendVideo(self, client):
        try:
            video = cv2.VideoCapture("./videos/homem_aranha.mov")
            i = 0  # frame counter
            frameTime = 1  # time of each frame in ms.

            while (video.isOpened()):
                ret = video.grab()  # grab frame
                i = i + 1  # increment counter
                _, frame = video.read()
                frame = imutils.resize(frame, width=400)
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
