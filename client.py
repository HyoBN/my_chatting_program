from socket import *
from threading import *
import sys
import time

quit_check=True
def send(sock):
    global quit_check
    while(quit_check):
        sendData = input('당신 : ')
        sock.send(sendData.encode('cp949'))
        
        if(sendData == 'quit'):
            print('대화방을 나갑니다.')
            quit_check=False
            clientSock.close()
            sys.exit()
            
            
        
def recv(sock):
    global quit_check
    while(quit_check):
        recvData = (sock.recv(1024)).decode('cp949')
        
        if(recvData == 'quit'):
            print('상대방이 대화방을 나갔습니다.')
            quit_check=False
            clientSock.close()
            sys.exit()
            
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
sender.join()
receiver.join()

while True:
    if(quit_check==False):
        sys.exit()
    time.sleep(1)
    
    pass


