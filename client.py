from socket import *

def send(sock):
    sendData = input('당신 : ')
    sock.send(sendData.encode('utf-8'))
    if(sendData == 'quit'):
        print('대화방을 나갑니다.')
        return 1
def recv(sock):
    recvData = (sock.recv(1024)).decode('utf-8')
    if(recvData == 'quit'):
        print('상대방이 대화방을 나갔습니다.')
        return 1

    print('상대방 :', recvData)


print('------client------')
clientSock=socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1',8106))

print('Connected...!')


while(True):
 
    if(recv(clientSock) or send(clientSock)):
        break

clientSock.close()
