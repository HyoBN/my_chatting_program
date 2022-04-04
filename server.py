from socket import *
from threading import *
from queue import *
import sys
import datetime

#------------- 서버 세팅 -------------
HOST = '127.0.0.1' # 서버 ip 주소 .
PORT = 9190 # 사용할 포트 번호.
MAX_CLIENT_NUM = 1 # 연결할 수 있는 최대 클라이언트 수.
#------------------------------------


s=''
s+='\n  -------------< 사용 방법 >-------------'
s+='\n   연결 종료 : !quit 입력 or ctrl + c    '
s+='\n   참여 중인 멤버 보기 : !member 입력     '
s+='\n'
s+='\n   이 프로그램 사용은 Jupyter Notebook에  '
s+='\n           최적화되어 있습니다.             '
s+='\n  --------------------------------------\n\n'


def now_time(): # 현재 시각 반환하는 함수.
    now = datetime.datetime.now()
    time_str=now.strftime('[%H:%M] ') # 현재 시각 저장.
    return time_str

def send_func(lock):

    while True:
        try:
            global left_member_name
            recv = received_msg_info.get()

            if recv[0]=='!quit' or len(recv[0])==0:  
                lock.acquire() # left_member_name에 대한 Lock.
                msg=str('[SYSTEM] '+now_time()+left_member_name)+'님이 연결을 종료하였습니다.'
                lock.release() # left_member_name에 대한 Lock.

            elif recv[0]=='!enter':

                now_member_msg='현재 멤버 : '
                for mem in member_name_list:
                    if mem!='-1':
                        now_member_msg+='['+mem+'] '
                recv[1].send(bytes(now_member_msg.encode()))
                msg=str('[SYSTEM] '+now_time()+member_name_list[recv[2]])+'님이 입장하였습니다.'

            elif recv[0]=='!member':
                now_member_msg='현재 멤버 : '
                for mem in member_name_list:
                    if mem!='-1':
                        now_member_msg+='['+mem+'] '

                recv[1].send(bytes(now_member_msg.encode()))


            else:
                msg = str(now_time() + member_name_list[recv[2]]) + ' : ' + str(recv[0])

            for conn in socket_descriptor_list:

                if conn =='-1': # 연결 종료한 클라이언트 경우.
                    continue

                if recv[1] != conn: #메시지 송신하는 클라이언트에게는 자신의 메시지가 출력되지 않게 함
                    conn.send(bytes(msg.encode()))

                else:
                    pass

            if recv[0] =='!quit':
                recv[1].close()
        except:
            pass

def recv_func(conn, count, lock):

    if socket_descriptor_list[count]=='-1':
        return -1
    while True:
        global left_member_name
        data = conn.recv(1024).decode()
        lock.acquire() # left_member_name와 count 에 대한 Lock.

        received_msg_info.put([data, conn, count]) 

        lock.release()

        if data == '!quit' or len(data)==0: # 해당 클라이언트가 연결을 종료하려고 할 때.
            # len(data)==0 은 해당 클라이언트의 소켓 연결이 끊어진 경우에 대한 예외 처리임.
            lock.acquire() # left_member_name와 count 에 대한 Lock.
            print(str(now_time()+ member_name_list[count]) + '님이 연결을 종료하였습니다.')
            left_member_name=member_name_list[count] # 종료한 클라이언트 닉네임 저장.
            socket_descriptor_list[count]= '-1' # 4/4 문제 발생시 '-1'이 아니라 None (NULL)로 설정해보기
            member_name_list[count]='-1'
            lock.release()
            break

    conn.close()

    
    
print(now_time()+'서버를 시작합니다')
server_sock=socket(AF_INET, SOCK_STREAM)
server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Time-wait 에러 방지.
server_sock.bind((HOST, PORT))
server_sock.listen(MAX_CLIENT_NUM)

count = 0
socket_descriptor_list=['-1',] # 클라이언트들의 소켓 디스크립터 저장.
member_name_list=['-1',] # 클라이언트들의 닉네임 저장, 인덱스 접근 편의를 위해 0번째 요소 '-1'로 초기화.
received_msg_info = Queue()
left_member_name=''
lock=Lock()

while True:
    count = count +1
    conn, addr = server_sock.accept()
    # conn과 addr에는 연결된 클라이언트의 정보가 저장된다.
    # conn : 연결된 소켓
    # addr[0] : 연결된 클라이언트의 ip 주소
    # addr[1] : 연결된 클라이언트의 port 번호
    client_name=''

    while True:
        client_name=conn.recv(1024).decode() # 유저 닉네임

        if not client_name in member_name_list:
            conn.send(bytes('checked'.encode()))
            break
        else:
            conn.send(bytes('overlapped'.encode()))

    member_name_list.append(client_name)
    socket_descriptor_list.append(conn)
    print(str(now_time())+client_name+'님이 연결되었습니다. 연결 ip : '+ str(addr[0]))

    if count>1:

        sender = Thread(target=send_func, args=(lock,))
        sender.start()
        pass

    else:
        sender=Thread(target=send_func, args=(lock,))
        sender.start()

    receiver=Thread(target=recv_func, args=(conn, count, lock))
    receiver.start()

server_sock.close()