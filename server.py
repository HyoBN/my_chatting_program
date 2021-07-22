from socket import *
from threading import *
from queue import *
import sys
import datetime

#------------- 서버 세팅 -------------
HOST = '127.0.0.1' # 서버 ip 주소 .
PORT = 9190 # 사용할 포트 번호.
MAX_CLIENT_NUM = 10 # 연결할 수 있는 최대 클라이언트 수.
#------------------------------------


def now_time(): # 현재 시각 반환하는 함수.
    now = datetime.datetime.now()
    nowTime=now.strftime('[%H:%M] ') # 현재 시각 저장.
    return nowTime


def send(lock):

    while True:

        try:
            global left_member_name
            recv = msg_info.get()

            if recv[0]=='!quit':
                lock.acquire() # left_member_name에 대한 Lock.
                msg=str('[SYSTEM] '+now_time()+left_member_name)+'님이 연결을 종료하였습니다.'
                lock.release() # left_member_name에 대한 Lock.
                    
            elif recv[0]=='enter':
                msg=str('[SYSTEM] '+now_time()+member_name[recv[2]])+'님이 입장하였습니다.'

            else:
                msg = str(now_time() + member_name[recv[2]]) + ' : ' + str(recv[0]) # recv[3]이 count.

            for conn in socket_descriptors:


                if conn =='-1': # 연결 종료한 클라이언트 경우.
                    continue

                if recv[1] != conn: #메시지 송신하는 클라이언트에게는 자신의 메시지가 출력되지 않게 함(이미 터미널 창 상에서 출력이 되므로)
                    conn.send(bytes(msg.encode()))

                else:
                    pass

            if recv[0] =='!quit':
                recv[1].close()
        except:
            pass

        
        
def recv(conn, count, lock):

    if socket_descriptors[count-1]=='-1':
        return -1
    while True:
        global left_member_name
        data = conn.recv(1024).decode()

        lock.acquire() # left_member_name와 count 에 대한 Lock.

        msg_info.put([data, conn, count]) # 일단 queue에 넣고,

        lock.release()

        if data == '!quit': # 해당 클라이언트가 연결을 종료하려고 할 때.
            lock.acquire() # left_member_name와 count 에 대한 Lock.
            socket_descriptors[count-1]='-1'
            left_member_name=member_name[count] # 종료한 클라이언트 닉네임 저장.
            print('[SYSTEM] '+str(now_time()+ member_name[count]) + '님이 연결을 종료하였습니다.')
            member_name[count]='-1'
            lock.release()
            break


    conn.close()


server_sock=socket(AF_INET, SOCK_STREAM)
server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Time-wait 에러 방지.
server_sock.bind((HOST, PORT))
server_sock.listen(MAX_CLIENT_NUM)


count = 0
socket_descriptors=[] # 클라이언트들의 소켓 디스크립터 저장.

member_name=['-1',] # 클라이언트들의 닉네임 저장, 인덱스 접근 편의를 위해 0번째 요소 '-1'로 초기화.

msg_info = Queue()

left_member_name=''

lock=Lock()



while True:
    count = count +1
    conn, addr = server_sock.accept()
    recv_name=''

    while True:
        recv_name=conn.recv(1024).decode() # 유저 닉네임
        
        if not recv_name in member_name:
            conn.send(bytes('checked'.encode()))
            break
            
        else:
            msg='overlapped'
            conn.send(bytes(msg.encode()))
            
    member_name.append(recv_name)
    socket_descriptors.append(conn) # 닉네임 등록까지 정상적으로 마쳐야 클라이언트 간 통신 가능하도록 코드 배치, 닉네임 설정 안한 상태에서 다른 클라이언트가 보낸 메시지를 recv하는 경우 방지.

    print(str(now_time())+'Connected '+ str(addr) + ', user name : '+recv_name)

    if count>1:

        sender = Thread(target=send, args=(lock,))
        #sender.daemon=True
        sender.start()
        #sender.join()
        pass
    
    else:
        sender=Thread(target=send, args=(lock,))
        #sender.daemon=True
        sender.start()
        #sender.join()
    
    receiver=Thread(target=recv, args=(conn, count, lock))
    #receiver.daemon=True
    receiver.start()
    #receiver.join()





