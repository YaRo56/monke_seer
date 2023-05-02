import os
import io
from tempfile import TemporaryFile
import tempfile
import datetime
import pickle
import time
import numpy as np
import socket
import cv2
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from time import sleep

def activate_stream(client_socket, picture):
    # читаем файл с картинкой
    # with open('smile.png', 'rb') as f:
    #     image_data = f.read()

    # отправляем картинку на сервер
    ####v1
    # client_socket.sendall(picture)
    # print(type(picture))
    # print(picture)
    # client_socket.send(b" <END> ")
    # print('pic send')

    ###v2

    # # f = io.StringIO()
    # f = TemporaryFile()
    # print(picture.shape)
    # client_socket.sendall(str(picture.shape[0]).encode())
    #
    # client_socket.sendall(str(picture.shape[1]).encode())
    #
    # print(type(f))
    # np.savez_compressed(f, frame=picture)
    # f.seek(0)
    # out = f.read()
    # client_socket.sendall(out)
    # client_socket.shutdown(1)

    ###v3 it works fine but slowly

    # BUF = 4096
    # timestr = time.strftime("%Y%m%d_%H%M%S")
    # image_name = "client_" + time.strftime(timestr) + ".png"
    # cv2.imwrite(image_name, picture)
    #
    #
    #
    #
    # fp = open(image_name, "rb")
    #
    # data = fp.read(BUF)
    # while data:
    #     client_socket.send(data)
    #     data = fp.read(BUF)
    # fp.close()
    # print(image_name + " sended")
    #
    # client_socket.send(b" <END> ")
    # os.remove(image_name)
    #
    # data = client_socket.recv(1024)
    #
    # print('Received from the server :', str(data.decode('ascii')))
    # print(f'Server: {data.decode()}')
    #
    # return f'{data.decode()}'


    ###v4
    data_string = pickle.dumps(picture)
    # print(data_string)
    # print(type(data_string))
    print(len(data_string))
    client_socket.send(data_string)
    client_socket.send(b" <END> ")
    print('pickle send')

    data = client_socket.recv(4096)
    return f'{data.decode()}'













class MainApp(MDApp):

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        self.image = None
        self.button = MDFlatButton(
            text='action',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(None, None)
        )
        # self.button2 = MDFlatButton(
        #     text='action',
        #     pos_hint={'center_x': 0.5, 'center_y': 0.5},
        #     size_hint=(None, None)
        # )
        self.pressed = False
        self.label = MDLabel(
            text="OBJECT",
            halign="center",
            size_hint=(None, None)
        )
        # хост и порт сервера
        HOST = 'localhost'
        PORT = 8888

        # создаем клиентский сокет

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 8888))


    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        self.button.bind(on_press=self.helping_func)
        layout.add_widget(self.button)

        layout.add_widget(self.label)
        Clock.schedule_interval(self.load_video, 1.0 / 8.0)
        return layout

    def helping_func(self, instance):
        if self.pressed:
            print('go to sleep plz\nzzz..')
        if not self.pressed:
            self.pressed = True
        else:
            self.pressed = False

        if self.pressed:
            Clock.schedule_interval(self.taking_pictures, 1)

    def taking_pictures(self, *args):
        if self.pressed:
            ret, frame = self.capture.read()
            x = datetime.datetime.now()
            timestr = time.strftime("%Y%m%d_%H%M%S")
            image_name = time.strftime(timestr) + ".png"
            # cv2.imwrite("clients_dir/" + image_name, frame)
            print('took a picture!')

            self.label.text = activate_stream(self.client_socket, frame)
            print("hello")
            # os.remove("clients_dir/" + image_name)


    def load_video(self, *args):
        ret, frame = self.capture.read()
        # self.image.frame = frame
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture


if __name__ == '__main__':
    MainApp().run()


