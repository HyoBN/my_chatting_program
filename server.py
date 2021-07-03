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


print('------Server------')
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('127.0.0.1', 8106))
serverSock.listen(1)

print('연결 대기중...')
connectionSock, addr = serverSock.accept()

print(str(addr), '와 연결되었습니다!')

while True:

    if(send(connectionSock) or recv(connectionSock)):
        break


serverSock.close()
