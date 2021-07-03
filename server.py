from socket import *

print('------Server------')
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('127.0.0.1', 8105))
serverSock.listen(1)

print('연결 대기중...')
connectionSock, addr = serverSock.accept()

print(str(addr), '와 연결되었습니다!')

while True:
    sendData = input('당신 : ')
    connectionSock.send(sendData.encode('utf-8'))
    if(sendData == 'quit'):
        break

    recvData = (connectionSock.recv(1024)).decode('utf-8')
    if(recvData == 'quit'):
        print('상대방이 대화방을 나갔습니다.')
        break

    print('상대방 :', recvData)

serverSock.close()
