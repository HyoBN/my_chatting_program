from socket import *
from threading import *
from queue import *
import sys
import time


Host='localhost' # 서버의 IP주소를 입력하세요.
Port = 9190 # 9190번 포트를 사용합니다.

def send(client_sock, name):
    while True:
        send_data = bytes(input('당신('+name+') :').encode())
        client_sock.send(send_data)
        
def recv(client_sock):
    while True:
        recv_data= client_sock.recv(1024).decode()
        print(recv_data)

client_sock=socket(AF_INET, SOCK_STREAM)

client_sock.connect((Host, Port))
print('Connecting to',Host,Port)

name = input('닉네임을 입력하세요 :')
send_name=bytes(name.encode())
client_sock.send(send_name) # 닉네임을 서버로 보내서 서버에 따로 저장함.

sender=Thread(target=send, args=(client_sock,name,))
sender.start()

receiver=Thread(target=recv, args=(client_sock,))
receiver.start()