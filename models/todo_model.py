from pydantic import BaseModel,Field,field_validator
from datetime import datetime 
from enum import Enum


class Branch(str,Enum):
    CSE = "Computer Sceince",
    IT = "Information Technology",
    EC = "Electrical",
    ME = 'Mechanical'
    
    
    

class Address(BaseModel):
    pincode:int = Field(...,description="enter a valid pincode",)  
    address:str = Field(...,description='enter your full address',max_length=100)

    @field_validator('pincode') 
    def validatePincode(cls,val):
        if len(str(val))!= 6:
            raise ValueError("Invalid pincode entered")
        return val 


class Student(BaseModel):
    name:str = Field(...,description='enter your full name',max_length=25)
    age: int = Field(...,description='enter you age',lt=100,gt=15)
    branch: Branch = Field(...,description='enter if branch assigned',example= Branch.CSE)
    address: Address = Field(...,description='enter the proper valid address',
                             example=Address(pincode=455001,address='64/1 vikhroli, Mumbai'))
    
    
    