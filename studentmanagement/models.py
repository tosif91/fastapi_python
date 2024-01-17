from typing import Optional
from pydantic import  BaseModel,Field
class Student:
    id: int
    name: str
    branch: str
    address: str
    phoneno: str
    summary: str

    def __init__(self,id,name,branch,address,phoneno,summary:Optional[str] = None):
        self.id = id,
        self.name = name,
        self.branch = branch,
        self.address = address,
        self.phoneno = phoneno
        self.summary = summary

class StudentRequest(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=4,max_length=20,description='enter student name ')
    branch: str = Field(max_length=20)
    address: str  = Field(min_length=5,max_length=30)
    phoneno: str = Field(min_length=10,max_length=10)
    summary: Optional[str] = None

    class Config:
        json_schema_extra={
                'example':{
                    'name':'enter the proper user name here ',
                    'branch':'enter ther student branch',
                    'address':'address to be here ',
                    'phoneno':'phone must be 10 digit',
                    'summary':'this is optrional'
                }
            }