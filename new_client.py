import sys 
from datetime import datetime 
from socket import *
import threading 
from object.user import User 
from object.chat import Chat 

class Client():
    
    _user:User = User('None','None')
    __socket=None 
    
    def __init__(self, user:User):
        self._user=user
        
    def connect_server(self, ip:str, port:int):
        self.__socket=socket(AF_INET, SOCK_STREAM)
        try:
            self.__socket.connect((ip,port))
            print(f'{ip}:{port} 연결되었습니다.')
            
        except Exception as e:
            print('연결 실패했습니다. 이유 : ')
            print(e)
    
        if __name__ == '__main__':
            
            send_thread=threading.Thread(target=self.input_send, args=())
            send_thread.start()
            
            recv_thread=threading.Thread(target=self.recv_loop,args=())
            recv_thread.start()
    
    def input_send(self):
        while True:
            self.send(input())
            
    def send(self, data:str):
        chat=Chat(user=self._user, msg=data, time=datetime.now())
        self.__socket.send(chat2json(chat).encode('utf-8'))
        
    def recv_loop(self):
        while True:
            print(self.receive())
            
    def receive(self) -> Chat:
        recvData=self.__socket.recv(1024).decode('utf-8')
        
        try:
            chat=json2chat(recvData)
            return chat 
        
        except Exception as e:
            print('에러 발생. 이유 : ')
            print(e)
            return Chat(User('None','None'), '에러 발생', time=datetime.now())
        
    def set_off(self):
        self.__socket.close()
        sys.exit()
        
def init_client():
    client=Client(User('1','hb'))
    _ip=input("ip : ")
    _port=input("port : ")
    client.connect_server(_ip, int(_port))
    import atexit
    atexit.register(lambda : client.set_off())
    
if __name__=='__main__':
    init_client()