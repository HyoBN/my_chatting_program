from socket import *
from threading import *
from queue import *
import sys
import os
import datetime

#--------------클라이언트 세팅 -----------------------
Host='127.0.0.1' # 서버의 IP주소를 입력하세요.
Port = 9190 # 사용할 포트 번호. 

def now_time(): 
    now = datetime.datetime.now()
    nowTime=now.strftime('[%H:%M] ')
    return nowTime

def enter_menu():
    print()
    print('  -------------< 사용 방법 >-------------')
    print('   연결 종료 : !quit 입력 or ctrl + c    ')
    print('   참여 중인 멤버 보기 : !member 입력     ')
    print()
    print('   이 프로그램 사용은 Jupyter Notebook에  ')
    print('           최적화되어 있습니다.             ')
    print('  ---------------------------------------\n\n')


def send(client_sock):

    while True:
        try:
            msg=input('당신('+name+') :')
            send_data = bytes(msg.encode())

        except:
            print('[SYSTEM] 메시지 전송에 실패하였습니다.')
            continue
            
        else:
            client_sock.send(send_data)
            if msg=='!quit':
                break

    print('서버와의 연결을 종료하였습니다.')
    client_sock.close()
    os._exit(1)

    
def recv(client_sock):

    while True:
        global send_data
        try:
            recv_data= client_sock.recv(1024).decode()
            
            if len(recv_data)==0:
                print('[SYSTEM] 서버와의 연결이 끊어졌습니다.')
                client_sock.close()
                os._exit(1)
        except:
            print('[SYSTEM] 메시지를 수신하지 못하였습니다.')

        else:
            print('\r'+recv_data+'                                             ')
            pass


client_sock= socket(AF_INET, SOCK_STREAM)

try:
    client_sock.connect((Host, Port))

except ConnectionRefusedError:
    print('서버에 연결할 수 없습니다.')
    print('1. 서버의 ip주소와 포트번호가 올바른지 확인하십시오.')
    print('2. 서버 실행 여부를 확인하십시오.')
    os._exit(1)
    
except:
    print('다른 이유로 인해 서버에 연결할 수 없습니다. 만든 사람에게 문의하세요.')

else:
    print('[SYSTEM] 서버와 연결되었습니다.')

while True:

    name = input('사용하실 닉네임을 입력하세요 :')
    flag=False
    
    for i in name:
        if i.isspace():
            print('공백은 입력이 불가능합니다.')
            flag=True
            break
    if flag==True:
        continue

    send_name=bytes(name.encode())
    client_sock.send(send_name)
    nickname_able_msg=client_sock.recv(1024).decode()

    if nickname_able_msg=='checked':
        enter_menu()
        print(now_time()+ '채팅방에 입장하였습니다.')
        enter_msg=bytes('!enter'.encode()) 
        client_sock.send(enter_msg)
        break

    elif nickname_able_msg=='overlapped':
        print('[SYSTEM] 이미 사용중인 닉네임입니다.')

    elif len(client_sock.recv(1024).decode())==0:
        print('[SYSTEM] 서버와의 연결이 끊어졌습니다.')
        client_sock.close()
        os._exit(1)
        
sender=Thread(target=send, args=(client_sock,))
sender.start()

receiver=Thread(target=recv, args=(client_sock,))
receiver.start()