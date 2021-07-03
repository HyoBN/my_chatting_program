from socket import *
from threading import *
import time

def send(sock):
    quit_check=1
    while(quit_check):
        sendData = input('당신 : ')
        sock.send(sendData.encode('utf-8'))
        if(sendData == 'quit'):
            quit_check=0
    print('대화방을 나갑니다.')
    return 1

def recv(sock):
    while(True):
        recvData = (sock.recv(1024)).decode('utf-8')
        if(recvData == 'quit'):
            break
        print('상대방 :', recvData)
    print('상대방이 대화방을 나갔습니다.')
    return 1

    


print('------Server------')
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('127.0.0.1', 8106))
serverSock.listen(1)

print('연결 대기중...')
connectionSock, addr = serverSock.accept()

print(str(addr), '와 연결되었습니다!')

sender = Thread(target=send, args=(connectionSock,))
receiver = Thread(target=recv, args=(connectionSock,))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass
