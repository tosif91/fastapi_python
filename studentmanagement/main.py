from fastapi import FastAPI,status,HTTPException
import database as db
from models import Student,StudentRequest

app = FastAPI()

@app.get('/students',status_code=status.HTTP_200_OK)
async  def getStudents():
    return db.studentDB

@app.post('/student/add',status_code=status.HTTP_201_CREATED)
async def addStudent(data : StudentRequest):
    db.studentDB.append(getStudentID(data))

def getStudentID(student: StudentRequest)->Student:
    s = Student(**student.model_dump())
    if len(db.studentDB) != 0:
        s.id = db.studentDB[-1].id + 1
    else:
        s.id = 1

    return s


@app.put('/student/update',status_code=status.HTTP_201_CREATED)
async def updateStudent(data : StudentRequest):
    for i in range(len(db.studentDB)):
        if db.studentDB[i].id == data.id:
            db.studentDB[i] = data
            break
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found!")

@app.delete('/student/{id}',status_code=status.HTTP_200_OK)
async def deleteStudent(id):
    for i in range(len(db.studentDB)):
        if id == db.studentDB[i].id:
            db.studentDB.pop(i)
            break
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Student not found!')