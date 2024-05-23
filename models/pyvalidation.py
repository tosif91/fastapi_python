from typing import List  
from models import BaseModel, Field

class Student(BaseModel):
    
    name:str  = Field(...,description='enter the student name')
    age:int = Field(...,title='enter age',description='age should be an integer and smallerthen 100',lt=100)
    subjects:List[str] = Field(...,title="Enter subjects",max_length=2)
    


s_dict = {
     'name':'tosif khan',
    'age':26,
    'subjects':["maths",'hindi',]
}

stud = Student(**s_dict)

print(stud.model_dump())