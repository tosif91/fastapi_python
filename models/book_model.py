#data 
#publisher 
#writer 
#title 
#summary 
#isIssued 
from datetime import datetime
from pydantic import Field


class Book:
    date:datetime =Field(...,description='book publishing date')
    title:str = Field(...,description='book title')
    writer:str = Field(...,description='book writer name')
    rack_no:int = Field(...,description="rack number where book is placed")
    publisher:str = Field(None,description='book publisher name')
    description:str =Field(None,description='book summary')
    is_issued : bool = Field(False,description='Is book issued')
    issued_by :str = Field(None,description='user uid who issued this book')    
    
    
    