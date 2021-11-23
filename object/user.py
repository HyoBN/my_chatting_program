class User:
    _id:str=None
    _name:str=None 

    def __init__(self, userid, username):
        self._id=userid
        self._name=username
        
    def get_id(self)->str:
        return self._id
    
    def get_name(self)->str:
        return self._name