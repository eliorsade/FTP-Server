import socket
import os


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False
    return True


def main_app(host, port, count_for_con_print):
    while True:
        while True:
            try:
                sock = socket.socket()
                sock.connect((host, port))
                if count_for_con_print == 0:
                    print('Welcome To FTP Server')
                    count_for_con_print += 1
                break
            except OSError:
                print("No Server Is Available At this Address")
                host = input("Insert Server's Address: ")

        send_recv = input("What would you like to do\nSend or Receive a File (Type q To Quit) (s/r/q)? ")
        while send_recv != "s" and send_recv != "r" and send_recv != "q":
            print(send_recv)
            send_recv = input("Invalid Input\nWhat would you like to do\nSend or Receive a File (s/r)? ")

        if send_recv == "r":
            sock.send(send_recv.encode())
            dir_list = sock.recv(4096)
            dir_list = dir_list.decode('utf-8')

            dir_list = eval(dir_list)
            sorted_list = sorted(dir_list)
            print("Available Files To Download:")

            count = 1
            for x in dir_list:
                print(count, x)
                count += 1

            file_to_download = input("Insert File To Download: ")
            sock.send(file_to_download.encode())

            save_path = '/Users/eliorsade/PycharmProjects/FTP-server/received/'
            file_path_and_name = os.path.join(save_path, file_to_download)

            try:
                file_size = sock.recv(1024)
                file_size = file_size.decode()

                if file_size == 'no_file':
                    print("File", file_to_download, "Not Found On Server")
                    sock.close()
                else:
                    f = open(file_path_and_name, 'wb')
                    while True:
                        data_flag = sock.recv(2048)
                        data = data_flag
                        if data_flag:
                            while data_flag:
                                data_flag = sock.recv(2048)
                                data += data_flag
                            else:
                                break
                    f.write(data)
                    f.close()
                    file_size = int(file_size)
                    print("File", file_to_download, "Transfer Is Complete!\nFile size is:",
                          file_size >> 20, "MB /", file_size, "KB")
                    sock.close()

            except:
                print("Disconnected From Server!")
                sock.close()
                break

        if send_recv == "s":
            sock.send(send_recv.encode())
            print("You chose to send file to server")
            os.chdir('/Users/eliorsade/PycharmProjects/FTP-server/files/')
            dir_list_send = os.listdir('/Users/eliorsade/PycharmProjects/FTP-server/files/')
            sorted_list = sorted(dir_list_send)
            for i in dir_list_send:
                x = 1
                print(x, i)
                x += 1

            file_to_send = input("Select File Name To Send: ")
            if not os.path.isfile(file_to_send):
                print("File not found")
                sock.close()
            else:
                file_size_send = os.path.getsize(file_to_send)
                file_size_send = str(file_size_send)
                file_name_and_size = file_to_send + file_size_send

                sock.send(file_name_and_size.encode())
                with open(file_to_send, 'rb') as f:
                    while True:
                        data = f.read(65536)
                        if not data:
                            break
                        sock.send(data)
                f.close()
                file_size_send = int(file_size_send)
                sock.close()
                print("File", file_to_send, "Was Successfully Sent, Size:",
                      file_size_send, "KB /", file_size_send >> 20, "MB")

        if send_recv == "q":
            print("Bye Bye")
            sock.send(send_recv.encode())
            sock.close()
            break


count_for_con_print = 0
port = 8800
host = input("Insert Server's Address To Connect: ")

is_valid_ipv4_address(host)
while not is_valid_ipv4_address(host):
    host = input("Invalid IP address, Insert Server's Address: ")

main_app(host, port, count_for_con_print)
