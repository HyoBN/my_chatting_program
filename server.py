from socket import *
from threading import *
import sys
import time

def send(sock):
    while(True):
        sendData = input('당신 : ')
        sock.send(sendData.encode('utf-8'))
        if(sendData == 'quit'):
            print('대화방을 나갑니다.')
            serverSock.close()
            sys.exit(1)

def recv(sock):
    while(True):
        recvData = (sock.recv(1024)).decode('utf-8')
        if(recvData == 'quit'):
            print('상대방이 대화방을 나갔습니다.')
            serverSock.close()
            sys.exit(1)
            
        print('상대방 :', recvData)
    return 1

    


print('------Server------')
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSock.bind(('127.0.0.1', 8106))

serverSock.listen(1)

print('연결 대기중...')
connectionSock, addr = serverSock.accept()

print(str(addr), '와 연결되었습니다!')

sender = Thread(target=send, args=(connectionSock,))

receiver = Thread(target=recv, args=(connectionSock,))

'''
sender.daemon=True
receiver.daemon=True
'''

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass


