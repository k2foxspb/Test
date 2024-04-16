import sys
import time
import serial
from var import *


class M3:
    def __init__(self):
        self.com_port = None
        self.Pack_id = 0
        self.init_com()

    def send_data(self):
        # у меня проблемы с кодировкой, поэтому такой большой костыль.
        self.Pack_id += 1
        data = input('введите данные')
        if data == EXIT:
            self.com_port.write('65535'.encode())
        elif data == EXCHANGE:
            self.com_port.write('65530'.encode())
        else:
            if int(data) < 16:
                data = '0' + str(data)
            if self.Pack_id < 10:
                str_pack = '0' + str(self.Pack_id)
                print(str_pack)
            else:
                str_pack = self.Pack_id

            data_pack = self.com_port.write(f'{B1}{B2_WRITE}{str_pack}{data}'.encode())

            print(f'отправлено сообщение:', hex(int(f'{B1}{B2_WRITE}{str_pack}{data}')).encode())
            print(f'длинна пакета: {data_pack} bytes')

    def run(self):
        while True:
            self.send_data()
            time.sleep(5)
            if self.com_port.inWaiting() > 0:
                out = self.com_port.read(B1).decode()
                print('Сообщение от М2', hex(int(out)))
            else:
                # Если сообщение не пришло, завершаем работу приложения.
                sys.exit()

    def init_com(self):
        try:
            self.com_port = serial.Serial('COM8', 9600, timeout=1, bytesize=6)
            print('приложение М3 запущено')
        except OSError:
            print('не удалось подключиться к COM-порту')


def main():
    x = M3()
    x.run()


if __name__ == "__main__":
    main()
