import base64
import socket
import threading
import time
import cv2
import numpy as np
import pyaudio
import wave

class Client:

    def __init__(self, name, type):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = "127.0.0.1"
        PORT = 6011
        self.BUFF_SIZE = 65536
        self.dest = (HOST, PORT)
        self.tcp.connect(self.dest)
        self.name = name
        self.type = type
        self.tcp.send((str(name) +";"+ str(type)).encode())

    def showMovie(self, path):
        HOST = '192.168.15.5'
        PORT = 6028
        # initLogin()
        # endereço IPV4 e protocolo TCP orientado à conexão
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dest = (HOST, PORT)

        udp.sendto(("REPRODUZIR_VIDEO;"+self.name+";"+path).encode(), dest)
        msg, _ = udp.recvfrom(self.BUFF_SIZE)

        if "-1" in msg.decode().split(";")[2]:
            # Não tem permissão
            return -1
        else:
            """
                      Recebe dados do outro usuário.
                      :param udp: Objeto da conexão atual.
                      """
            x = ''
            if path == './videos/homem_aranha_360p.mp4':
                x = 'homem_aranha_1080p.wav'
            if path == './videos/homem_aranha_1080p.mov':
                x = 'homem_aranha_1080p.wav'
            if path == './videos/homem_aranha_720p.mov':
                x = 'homem_aranha_720p.wav'
            if path == './videos/gucci_1080p.mov':
                x = 'gucci_1080p.wav'
            if path == './videos/gucci_720p.mov':
                x = 'gucci_720p.wav'




            fps, st, frames_to_count, cnt = (0, 0, 20, 0)
            pa = pyaudio.PyAudio()
            pa.get_default_host_api_info()
            wav_file = wave.open(x)
            stream_out = pa.open(
                rate=wav_file.getframerate(),  # sampling rate
                channels=wav_file.getnchannels(),  # number of output channels
                format=pa.get_format_from_width(wav_file.getsampwidth()),  # sample format and length
                output=True,  # output stream flag
                output_device_index=4,  # output device index
                frames_per_buffer=1024,  # buffer length
            )
            output_audio = wav_file.readframes(5 * wav_file.getframerate())
            stream_out.write(output_audio)

            while True:
                try:
                    packet, _ = udp.recvfrom(self.BUFF_SIZE)
                    if "end_video" in packet.decode():
                        cv2.destroyAllWindows()
                        return
                    else:
                        data = base64.b64decode(packet, ' /')
                        # Uma nova matriz inicializada a partir de dados binários ou de texto brutos em uma string.
                        npdata = np.fromstring(data, dtype=np.uint8)
                        # lê os dados do cache de memória especificado e converte (decodifica) os dados em formato de imagem
                        frame = cv2.imdecode(npdata, 10)
                        frame = cv2.putText(
                            frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.imshow("Filme", frame)

                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('q'):
                            # client_socket.close()
                            cv2.destroyAllWindows()
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
            return 0

    # def receiveMovie(self, udp):




