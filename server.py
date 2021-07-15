from socket import *
from threading import *
from queue import *
import sys
import datetime


MAX_CLIENT_NUM = 10 # 연결할 수 있는 최대 클라이언트 수.

def send(socket_descriptors, member_info):
    while True:
        try:
            recv = member_info.get()
            
            for conn in socket_descriptors:
                
                now = datetime.datetime.now()
                nowTime=now.strftime('[%H:%M] ') # 현재 시각 저장.
                
                msg = str(nowTime + member_name[recv[3]-1]) + ' : ' + str(recv[0]) # recv[3]이 count이므로 0번째 index부터 접근하기 위해 -1 해줌.
                if recv[2] != conn: #메시지 송신하는 클라이언트에게는 자신의 메시지가 출력되지 않게 함(이미 터미널 창 상에서 출력이 되므로) 
                    conn.send(bytes(msg.encode()))
                else:
                    pass
        except:
            pass

def recv(conn, count, member_info):

    while True:
        data = conn.recv(1024).decode()
        member_info.put([data, recv_name, conn, count])

member_info = Queue()
HOST = ''
PORT = 9190

server_sock=socket(AF_INET, SOCK_STREAM)
server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Time-wait 에러 방지.
server_sock.bind((HOST, PORT))
server_sock.listen(MAX_CLIENT_NUM)
count = 0
socket_descriptors=[] # 클라이언트들의 소켓 디스크립터 저장. 서버에 연결한 순서대로 저장됨.

member_name=[] # 클라이언트들의 닉네임을 저장, 서버에 연결한 순서대로 저장됨.

while True:
    count = count +1
    conn, addr = server_sock.accept()
    
    recv_name=''
    #recv_name=conn.recv(1024).decode() # 유저 닉네임
    
    
    while True:
        recv_name=conn.recv(1024).decode() # 유저 닉네임
        if not recv_name in member_name:
            print('목록에 없습니다.')
            conn.send(bytes('checked'.encode()))
            break
        else:
            print('닉네임이 중복됩니다!')
            msg='overlapped'
            conn.send(bytes(msg.encode())) 
    member_name.append(recv_name)
    
    socket_descriptors.append(conn) # 닉네임 등록까지 정상적으로 마쳐야 클라이언트 간 통신 가능하도록 코드 배치, 닉네임 설정 안한 상태에서 다른 클라이언트가 보낸 메시지를 recv하는 경우 방지.
    
    print('Connected '+ str(addr) + ', user name : '+recv_name)
    
    if count>1:
        
        sender = Thread(target=send, args=(socket_descriptors, member_info,))
        sender.start()
        pass
    else:
        sender=Thread(target=send, args=(socket_descriptors, member_info,))
        sender.start()
    
    receiver=Thread(target=recv, args=(conn, count, member_info,))
    receiver.start()





