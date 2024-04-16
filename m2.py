import socket
import sys
import time

import serial

from var import *


class M2:
    def __init__(self):
        self.Pack_id = 0
        self.com_port = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_com()
        self.Exchange = 0
        self.timer = 0

    def send_message_to_server(self, pack):

        self.timer = time.time()
        self.sock.send(pack.encode())
        print(f'Отправлено сообщение на сервер {hex(int(pack))}')
        if pack == EXIT:
            sys.exit()

    def send_message_to_com(self, pack):
        self.com_port.write(pack.encode())
        print('отправлено сообщение на COM порт')

    def get_message_from_server(self):
        if time.time() - self.timer < M2_INTERVAL:
            out = self.sock.recv(B1).decode()
            print(f'сообщение от сервера: {hex(int(out))} Pack_id M1: {out[3:5]}')
            return out
        else:
            self.send_message_to_server(EXIT)

    def get_message_from_com(self):
        if self.com_port.in_waiting > 0:
            request = self.com_port.read(6).decode()
            self.Pack_id += 1
            print(f'сообщение от COM: {hex(int(request))} Pack_id_M3: {request[2:4]}')
            return request

    def run(self):
        # основной цикл программы
        while True:
            try:
                com_recv = self.get_message_from_com()
                self.send_message_to_server(com_recv)
                server_recv = self.get_message_from_server()
                self.send_message_to_com(server_recv)

            except:
                pass

    def init_com(self):
        for i in range(5):
            print(f'Попытка подключения №{i + 1}')
            try:
                self.com_port = serial.Serial('COM9', 9600, timeout=1, bytesize=6)
                self.sock.connect((IP_ADDRESS, PORT))
                print('приложение М2 запущено!')
            except:
                pass
            else:
                break
            if i > 4:
                sys.exit()
            time.sleep(1)


def main():
    module = M2()
    module.run()


if __name__ == '__main__':
    main()
