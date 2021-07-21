from socket import *
from threading import *
from queue import *
import sys
import os
import time


Host='127.0.0.1' # 서버의 IP주소를 입력하세요.
Port = 9190 # 9190번 포트를 사용합니다.

def send(client_sock, name):
    
    while True:
        
    
        try:
            msg=input('당신('+name+') :')
            send_data = bytes(msg.encode())
            

            if msg=='!quit':
                break
        except:
            print('메시지 전송에 실패하였습니다.')
            continue
        else:
            client_sock.send(send_data)
            

    print('서버와의 연결을 종료합니다.')
    client_sock.close() # ~~~~~~~~~~~~~~~~~ing
    print('연결을 종료하였습니다.')
    os._exit(1) # ~~~~~~~~~~~~~~~~~~~~~~~~ing

def recv(client_sock):
    
    while True:
        recv_data= client_sock.recv(1024).decode()
        #print('\n')
        print(recv_data)

client_sock= socket(AF_INET, SOCK_STREAM)

client_sock.connect((Host, Port))
print('[SYSTEM] 연결하는 서버 정보 : ',Host,Port)

while True:
    
    name = input('닉네임을 입력하세요 :')
    
        
    send_name=bytes(name.encode())
    client_sock.send(send_name) # 닉네임을 서버로 보내서 서버에 따로 저장함.

    nickname_able_msg=client_sock.recv(1024).decode() # 닉네임 중복 여부를 서버로부터 받음.
    
    if nickname_able_msg=='checked':
        print('연결을 종료하려면 !quit 를 입력하세요.')
        print('[SYSTEM] 채팅방에 입장하였습니다.')
        enter_msg=bytes('enter'.encode()) # 연결 시 다른 클라이언트들에게 연결 사실 알리기 위한 메시지.
        client_sock.send(enter_msg)
        break
        
        
    elif nickname_able_msg=='overlapped':
        print('[SYSTEM] 이미 사용중인 닉네임입니다.')


sender=Thread(target=send, args=(client_sock,name,))
sender.daemon=True
sender.start()

receiver=Thread(target=recv, args=(client_sock,))
#receiver.daemon=True
receiver.start()