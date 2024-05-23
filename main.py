from fastapi import FastAPI , Path, Query,Cookie,HTTPException
from fastapi.responses import JSONResponse 
from typing import List
from models.todo_model import Student
app = FastAPI()

students: list[Student] = []

@app.get('/')
def root():
    return {'message':'hello world'}


# THIS ARE PATH PARAMETERS

# http://127.0.0.1:8000/hello/tosif_khan
@app.get('/hello/{name}')
def getName(name):
    return {'message': name}

# http://127.0.0.1:8000/hello/tosif_khan/26
@app.get('/hello/{name1}/{age}')
def getAllName(name1 : str,age :int): #type hint can be added and also provide proper validation 
    return{'name1':name1,'age':age}

# This are query parameters 
# http://127.0.0.1:8000/hello?name1=tosif_khan&name2=saif_khan
# This ? in trailing part of url is called "Query String"
@app.get('/hello')
def getAllName(name1:str,name2:str): #quey parameter may have type hints depends on need
    return{'name1':name1,'name2':name2}



# PARAMETER VALIDATION

# Validation can be added on both path and query parameters 

# Path parameter validation 

#http://127.0.0.1:8000/validate/path/tosif  
@app.get('/validate/name/{name}')
def getValidateName(name : str = Path(min_length=3,max_length=20)):
    return {'name':name}

#http://127.0.0.1:8000/validate/age/110
@app.get('/validate/age/{age}')
def getValidateAge(age:int = Path(lt=100,gt=10)):
    return{"age":age}


#QUERY PARAMETER VALIDATION
#It is similart to path param validation , only you have to change object from Path to Query 


#mutlitple query data validation 
@app.get('/validate/query/')
def getValidateMultiQueryData(name:str=Query(min_length=2,max_length=5),age:int=Query(lt=100,gt=10)):
    return {'name':name,'age':age}



@app.post('/add/student')
def addStudent(body:Student):
    students.append(Student(**body.model_dump()))
    return {'message':body.model_dump()}
    

@app.get('/students')
def getStudents():
    return {'data': students}


 
 
#COOKIE PARAMETERS  

@app.post('/cookie')
def create_cookie():
    content = {'message':'this is the data in response'}        
    response = JSONResponse(content= content)
    response.set_cookie(key='username',value='tosif khan')
    
    return response

@app.get('/readcookie')
def read_cookie(username:str = Cookie(None)):
    return {'username':username}    





#DEPENCDENCY INJECTION 

#here two route deocrator function have same query paramter where we can inject this dependency 
#if we do not inject then when changes required in the query paramter the we have to make changes in 
#both the route decorator function 


from fastapi import Depends 

def my_dependencies(id:int,name:str):
    return {'id':id,'name':name}


@app.get('/depends1')
def depends_1(data:dict = Depends(my_dependencies)):
    return data

@app.get('/depends2')
def depends2(data:dict = Depends(my_dependencies)):
    return data


#we can inject dependencies in the decorator level 

def validateDep(dep: dict =  Depends(my_dependencies)):
    
    if dep['id'] < 10:
        raise  HTTPException(status_code=400,detail="not eligible")
    

@app.get('/validate/depends/',dependencies=[Depends(validateDep)])
def validate_depends(): 
    return {'message':'you are eligible'}

#in place of using function for dependency we can also use class and inject them 
