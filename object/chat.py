from object.user import User 
from datetime import datetime 

class Chat:
    user:User = None 
    msg:str=None 
    time:str=None 
        
    def __init__(self, user:User, msg:str, time:datetime):
        self.user=User 
        self.msg=msg 
        self.time=time 
        