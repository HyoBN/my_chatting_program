from socket import *
from threading import *
from queue import *
import sys
import time


Host='localhost' # 서버의 IP주소를 입력하세요.
Port = 9190 # 9190번 포트를 사용합니다.

def send(client_sock, name):
    while True:
        msg=input('당신('+name+') :')
        send_data = bytes(msg.encode())
        client_sock.send(send_data)

        if msg=='!quit':
            break;

    print('서버와의 연결을 종료합니다.')
    client_sock.close()

def recv(client_sock):
    while True:
        recv_data= client_sock.recv(1024).decode()
        print(recv_data)

client_sock=socket(AF_INET, SOCK_STREAM)

client_sock.connect((Host, Port))
print('[SYSTEM] 연결하는 서버 정보 : ',Host,Port)

while True:
    name = input('닉네임을 입력하세요 :')
    send_name=bytes(name.encode())
    client_sock.send(send_name) # 닉네임을 서버로 보내서 서버에 따로 저장함.

    nickname_msg=client_sock.recv(1024).decode() # 닉네임 중복 여부를 서버로부터 받음.
    
    if nickname_msg=='checked':
        print('연결을 종료하려면 !quit 를 입력하세요.')
        print('[SYSTEM] '+name+'님이 입장하였습니다.')
        break
        
    elif nickname_msg=='overlapped':
        print('[SYSTEM] 이미 사용중인 닉네임입니다.')
    

sender=Thread(target=send, args=(client_sock,name,))
sender.daemon=True
sender.start()

receiver=Thread(target=recv, args=(client_sock,))
#receiver.daemon=True
receiver.start()