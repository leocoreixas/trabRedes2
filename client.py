import base64
import pickle
import socket
import struct
import threading
import time

import cv2
import numpy as np


class Client:

    def __init__(self):
        HOST = '192.168.15.3'
        PORT = 6013
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dest = (HOST, PORT)
        thread = threading.Thread(target=self.listen, args=(self.udp,))
        thread.start()
        self.send_message("connect", dest)
        self.BUFF_SIZE = 65536

    def send_message(self, msg, dest):
        """
        Envia uma mensagem udp
        :param msg: Payload da mensagem
        :param dest: Endereço de envio da mensagem
        """
        print("Enviando mensagem: " + msg)
        self.udp.sendto(msg.encode(), dest)

    def listen(self, udp):
        """
        Recebe dados do outro usuário. Isto é, quem responde a chamada.
        :param udp: Objeto da conexão atual.
        """

        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        while True:
            try:
                packet, _ = udp.recvfrom(self.BUFF_SIZE)
                if "end_video" in packet.decode():
                    cv2.destroyAllWindows()
                    return
                else:
                    data = base64.b64decode(packet, ' /')
                    npdata = np.fromstring(data, dtype=np.uint8)
                    frame = cv2.imdecode(npdata, 1)
                    frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imshow("RECEIVING VIDEO", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        # client_socket.close()
                        break
                    if cnt == frames_to_count:
                        try:
                            fps = round(frames_to_count / (time.time() - st))
                            st = time.time()
                            cnt = 0

                        except:
                            pass
                    cnt += 1

            except Exception as e:
                print("Error: " + str(e))


client = Client()

