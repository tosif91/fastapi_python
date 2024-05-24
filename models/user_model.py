from enum import Enum
from pydantic import BaseModel,Field

class UserRole(str,Enum):
    Librarian='Librarian',
    Member = 'Member'

class Meta(BaseModel):
    total_book_issued : int|None = 0 
    total_book_returned :int |None = 0


class UserInput(BaseModel):
    name:str = Field(...,max_length=20,min_length=5,description='user full name' ,examples=['tosif khan'])
    email:str = Field(...,max_length=40,min_length=5,pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        description="User's email address",examples=['tosifmid@gmail.com'] )
    password:str =Field(...,max_length=10,min_length=6,description='user password',examples=['pwd123'])
    role:UserRole = Field(...,description='enter user role ie Librarion | Member')
                          
class UserData(UserInput):
    uid:int = Field(gt=0,) 
    hashed_password:str 
    meta:Meta = Field(Meta())  
     
    
    
    