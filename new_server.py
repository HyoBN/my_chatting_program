from socket import *
import time
import threading 
from queue import Queue 

class ChattingServer():
    
    __server_socket=None 
    __LISTENING_NUM=10 
    __IP='localhost' 
    __PORT=8080
    send_queue=Queue() 
    group=[] 
    
    def __init__(self):
        self.__server_socket=socket(AF_INET, SOCK_STREAM)
        
    def set_address(self, ip:str, port:int):
        self.__IP=ip
        self.__PORT=port
        
    def start_listening(self):
        self.__server_socket.bind((self.__IP,self.__PORT))
        self.__server_socket.listen(self.__LISTENING_NUM)
        print(f'{self.__IP}:{self.__PORT}에서 연결 대기중..')
        count=0
        
        while True:
            count+=1
            conn,addr = self.__server_socket.accept()
            group.append(conn)
            print(f'Connected {addr}')
            print(f'Group Number: {len(group)}')
            
            if count>1:
                send_queue.put('Group Changed!')
                
            t_send=threading.Thread(target=self.send, args=(group, send_queue))
            t_send.start()
            
    def send(self, group, send_queue):
        print('Send Thread Start')
        while True:
            try:
                recv=send_queue.get()
                
                if recv=='Group Changed!':
                    print('Groupd Changed!!')
                    break 
                
                for conn in group:
                    msg=str(recv[0])
                    if recv[1]!=conn:
                        try:
                            conn.send(bytes(msg.encode()))
                        except:pass 
                    else:pass 
            except:pass 
            
    def recv(self, conn, count, send_queue):
        print('Thread recv'+str(count)+'Start..!')
        
        while True:
            data=conn.recv(1024).decode() 
            
            send_queue.put([data,conn,count])

if __name__=="__main__":
    serv=ChattingServer()
    serv.start_listening()