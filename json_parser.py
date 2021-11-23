import json 
from datetime import datetime 
from object.user import User 
from object.chat import Chat 

def user2json(user:User)->str:
    dic={'name':user.get_name(), 'id':user.get_id()}
    return json.dumps(dic)

def json2user(jstr:str)->User:
    dic=json.loads(jstr)
    user=User(userid=dic['id'],username=dic['name'])
    return user 

def time2str(time:datetime):
    return time.strftime("%Y%m%d %H:%M:%S")

def str2time(tstr:str):
    return datetime.strptime(tstr,"%Y%m%d %H:%M:%S")

def chat2json(chat:Chat)->str:
    dic={'user':user2json(chat.user), 'msg':chat.msg, 'time':time2str(chat.time)}
    return json.dumps(dic)

def json2chat(jstr:str)->Chat:
    dic=json.loads(jstr)
    chat=Chat(user=json2user(dic['user']), msg=dic['msg'], time=str2time(dic['time']))
    return chat