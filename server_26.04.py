import io
import socket
import threading
import os
import pickle
import time
from PIL import Image
import cv2
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
import numpy as np


# хост и порт
HOST = 'localhost'
PORT = 8888

# создаем серверный сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f'Server started at {HOST}:{PORT}')





def ML(frame,model):



    # picture = Image.frombytes(mode='RGB', size =(1, len(frame)) , data=frame)
    resizeImg = cv2.resize(frame, (224, 224))

    # picture = frame.resize((224,224))

    picture = np.array(resizeImg).reshape((1,224,224,3))

    ans = model.predict(picture)

    info = tf.keras.applications.resnet50.decode_predictions(
        ans, top=1
    )
    return info[0][0][1]







# функция для обработки клиентского соединения
def handle_client(client_socket, model):



    # file_stream = io.BytesIO()
    # flag = 0
    # i = 0
    # while True:
    #     i += 1
    #     print(i)
    #     flag = 1
    #     # принимаем данные от клиента (картинки)
    #     data = client_socket.recv(1024)
    #     if b" <END> " in data:
    #         break
    #     file_stream.write(data)
    #
    #     if not data:
    #         image = Image.open(file_stream)
    #         print('pic recieved completly')
    #         break
    # client_socket.sendall(str(ML(image, model)).encode('utf-8'))
    #     # отправляем клиенту сообщение "картинка получена"



    ####v1
    # i = 0
    # while True:
    #     data = client_socket.recv(1024)
    #     file_stream = io.BytesIO()
    #     while data:
    #         file_stream.write(data)
    #         data = client_socket.recv(1024)
    #         print(i)
    #         i+=1
    #         if b" <END> " in data:
    #             print("END")
    #             break
    #     image = Image.open(file_stream)
    #     client_socket.sendall(str(ML(image, model)).encode('utf-8'))


    ####v2
    # i = 0
    # ultimate_buffer = b''
    # while True:
    #     receiving_buffer = client_socket.recv(1024)
    #     if not receiving_buffer:
    #         break
    #     ultimate_buffer += receiving_buffer
    #     print('recieved ', i)
    #     i+=1
    # # print(ultimate_buffer)
    # # bin_image = b''
    # # print(type(ultimate_buffer))
    # vector_bytes_str = str(ultimate_buffer)
    # vector_bytes_str_enc = vector_bytes_str.encode()
    # bytes_np_dec = vector_bytes_str_enc.decode('unicode-escape').encode('ISO-8859-1')[2:-1]
    # # np.frombuffer(bytes_np_dec, dtype=np.float32)
    # final_image = np.asarray(bytearray(bytes_np_dec), dtype=np.uint8)
    # # print(type(final_image))
    #
    #
    # # final_image = np.load(io.BytesIO(ultimate_buffer))['frame']
    # print(final_image)
    # print(type(final_image))
    # print(len(final_image))
    # image = np.resize(final_image, 224*224*3)
    # print(final_image)
    # print(final_image.shape)
    # print("image: ", image.shape)
    # image1 = image.reshape(224, 224, 3)
    # # picture = np.array(final_image).reshape((1, 224, 224, 3))
    # print("image1", image1.shape)
    # img = Image.fromarray(image1, 'RGB')
    # img.show()


    ####v2.1
    # s1 = client_socket.recv(1024)
    # s1 = s1.decode()
    # print(s1)
    # s2 = client_socket.recv(1024)
    # s2 = s2.decode()
    # print(s2)
    #
    # i = 0
    # ultimate_buffer = b''
    # while True:
    #     receiving_buffer = client_socket.recv(1024)
    #     if not receiving_buffer:
    #         break
    #     ultimate_buffer += receiving_buffer
    #     print('recieved ', i)
    #     i += 1
    # # print(ultimate_buffer)
    # # bin_image = b''
    # # print(type(ultimate_buffer))
    # # vector_bytes_str = str(ultimate_buffer)
    # # vector_bytes_str_enc = vector_bytes_str.encode()
    # # bytes_np_dec = vector_bytes_str_enc.decode('unicode-escape').encode('ISO-8859-1')[2:-1]
    # print("hello?")
    # arr = np.frombuffer(ultimate_buffer, dtype=np.uint8).reshape((int(s1), int(s2), 3))
    # print("hello?")
    # # np_array = np.resize(arr, (224, 224, 3))
    # pixel_array_resized = np.resize(arr, (224, 224, 3))
    # img = Image.fromarray(pixel_array_resized)
    # img.show()



    # ####v3 it works fine but slowly
    # BUF = 4096
    # while True:
    #
    #     file_stream = io.BytesIO()
    #     flag = 0
    #     image_name = 'zeronulll'
    #
    #     recvfile = client_socket.recv(BUF)
    #
    #     while recvfile:
    #         flag = 1
    #         file_stream.write(recvfile)
    #         recvfile = client_socket.recv(BUF)
    #
    #
    #         if b" <END> " in recvfile:
    #             timestr = time.strftime("%Y%m%d_%H%M%S")
    #             image_name =time.strftime(timestr) + ".png"
    #
    #             break
    #
    #     if flag == 1:
    #         image = Image.open(file_stream)
    #         image.save("serv_" + image_name, format="PNG")
    #
    #
    #     ###MLMLMLMLL
    #
    #
    #     client_socket.send("ya_ustal".encode())

    ###V4 with jsons
    while True:
        buf = b''
        while True:
            data = client_socket.recv(4096)
            if b" <END> " in data:
                buf += data
                break
            buf += data
        data_arr = pickle.loads(buf)
        # print(data_arr)
        print(data_arr.shape)
        # img = Image.fromarray(data_arr[:,:,0], 'RGB')
        # img.save('l1.png', format='PNG')
        # img = Image.fromarray(data_arr[:, :, 1], 'RGB')
        # img.save('l2.png', format='PNG')
        # img = Image.fromarray(data_arr[:, :, 2], 'RGB')
        # img.save('l3.png', format='PNG')
        # r = data_arr[:,:,0]
        # data_arr[:,:,0] = data_arr[:,:,2]
        # data_arr[:,:,2] = r
        # img = Image.fromarray(data_arr, mode="")
        # img.show()
        client_socket.sendall(str(ML(data_arr, model)).encode('utf-8'))
        print('obj send')



model = tf.keras.applications.efficientnet_v2.EfficientNetV2B0(include_top=True,
                                       weights='imagenet',
                                       input_tensor=None,
                                       input_shape=(224, 224, 3),
                                       pooling=None,
                                       classes=1000,
                                       classifier_activation='softmax'
                                       )

while True:
    # ждем клиентского подключения
    client_socket, address = server_socket.accept()
    print(f'Connected by {address}')

    # запускаем новый поток для обработки клиентского соединения
    client_thread = threading.Thread(target=handle_client, args=[client_socket, model])
    client_thread.start()