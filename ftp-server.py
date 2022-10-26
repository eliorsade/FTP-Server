import os
import socket
from conf import HOST, PORT
from datetime import datetime
import re

now_time = datetime.now()
dt_string = now_time.strftime("%d/%m/%Y %H:%M:%S")
sock = socket.socket()
socket_connected_count = 0

log_path = '/Users/eliorsade/PycharmProjects/FTP-server/log.txt'

sock.bind((HOST, PORT))
sock.listen(10)

f = open(log_path, "a")
f.write(dt_string + " Socket Created Successfully\n")
f.close()

print("Socket Created Successfully")
print('Server Is Listening...')

while True:
    dir_list = os.listdir('/Users/eliorsade/PycharmProjects/FTP-server/files/')
    os.chdir('/Users/eliorsade/PycharmProjects/FTP-server/files/')
    con, addr = sock.accept()
    addr_ip = addr[0]

    if socket_connected_count == 0:
        print('Connected With IP', addr[0], 'On Port', addr[1])
        f = open(log_path, "a")
        f.write(dt_string + " Connected With " + addr_ip + "\n")
        f.close()
        socket_connected_count += 1

    send_recv = con.recv(1024)
    send_recv = send_recv.decode()

    if send_recv == "r":
        print("Sending File List To Client")
        dir_list = str(dir_list)
        dir_list = dir_list.encode()
        con.send(dir_list)
        print("Waiting For A Request")
        try:
            file_to_send = con.recv(1024)
            file_size = os.path.getsize(file_to_send)

            file_size = str(file_size)
            con.send(file_size.encode())
            file_size = int(file_size)

            print(file_to_send.decode(), "file Size Is:", file_size >> 20, "MB /", os.path.getsize(file_to_send), "KB")

            with open(file_to_send, 'rb') as file:
                while True:
                    data = file.read(65536)
                    if not data:
                        break
                    con.send(data)
            file.close()

            file_to_send = file_to_send.decode()
            print(file_to_send, 'Has Been Transferred Successfully To', addr[0])
            print("Waiting For A New Request")

            f = open(log_path, "a")
            f.write(dt_string + " " + file_to_send + ' Has Been Transferred Successfully To ' + addr_ip + " File Size: " + str(file_size) + ' KB\n')
            f.close()

            con.close()
            socket_connected_count += 1

        except:
            print("Bad File Request from " + addr_ip)
            print("Waiting For A New Request")
            con.send('no_file'.encode())
            con.close()
            f = open(log_path, "a")
            f.write(dt_string + " Bad File Request from " + addr_ip + " File " + file_to_send.decode() + " Not Found On Server\n")
            f.close()
            socket_connected_count += 1

    if send_recv == 's':
        try:
            save_path = '/Users/eliorsade/PycharmProjects/FTP-server/Received-client/'
            file_sent = con.recv(1024)
            file_sent = file_sent.decode()

            full_name_and_size = re.findall(r'\d+', file_sent)[-1]
            index = file_sent.rfind(full_name_and_size)
            file_sent_name = file_sent[:index]
            file_sent_size = file_sent[index:]

            file_path_and_name = os.path.join(save_path, file_sent_name)
            print("File Name To Be Received:", file_sent_name)
            f = open(file_path_and_name, 'wb')
            while True:
                data_flag = con.recv(2048)
                data = data_flag
                if data_flag:
                    while data_flag:
                        data_flag = con.recv(2048)
                        data += data_flag
                    else:
                        break
            f.write(data)
            f.close()

            file_recv_int = int(file_sent_size) >> 20
            file_sent_size = str(file_sent_size)
            #           print(file_recv_int, file_sent_size)
            f = open(log_path, "a")
            f.write(dt_string + " File " + str(file_sent_name) + " Has Been Successfully Received From " + addr_ip + " File Size: " + str(file_sent_size) + " KB\n")
            f.close()
            print("File", file_sent_name, 'Has Been Successfully Received From', addr_ip)
            con.close()
            socket_connected_count += 1

        except:
            print("Bad File Request from " + addr_ip)
            con.close()
            socket_connected_count += 1
            f = open(log_path, "a")
            f.write(dt_string + " Bad File Request from " + addr_ip + "\n")
            f.close()

    if send_recv == 'q':
        print("Client Disconnected")
        f = open(log_path, "a")
        f.write(dt_string + " Client " + addr_ip + " Disconnected\n")
        socket_connected_count = 0
        f.close()
        con.close()
