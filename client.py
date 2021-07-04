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
            clientSock.close()
            sys.exit(1)
        
def recv(sock):
    while(True):
        recvData = (sock.recv(1024)).decode('utf-8')
        if(recvData == 'quit'):
            print('상대방이 대화방을 나갔습니다.')
            clientSock.close()
            sys.exit(1)

        print('상대방 :', recvData)
    return 1


print('------client------')
clientSock=socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1',8106))

print('Connected...!')


sender = Thread(target=send, args=(clientSock,))
receiver = Thread(target=recv, args=(clientSock,))
'''
sender.daemon=True
receiver.daemon=True
'''

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass


