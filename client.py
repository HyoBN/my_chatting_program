from socket import *

print('------client------')
clientSock=socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1',8104))

print('Connected...!')


while(True):
    
    recvData=(clientSock.recv(1024)).decode('utf-8')

    if(recvData=='quit'):
        print('상대방이 대화방을 나갔습니다.')
        break
    
    print('상대방 : ', recvData)

    sendData=input('당신 : ')
    
    clientSock.send(sendData.encode('utf-8'))
    if(sendData=='quit'):
        break
    
clientSock.close()
