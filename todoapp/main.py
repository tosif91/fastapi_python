from fastapi import FastAPI,Depends,HTTPException,Path,status
from sqlalchemy.orm import  Session
from typing import  Annotated
from database import engine,Base,SessionLocal
from models import Todo
from schemas import TodoRequest

app = FastAPI()

#this will only run if our todo.db database is not present
Base.metadata.create_all(bind=engine) #when server runs it will create a database

#fast api works fast as you can see below we create a connection and once the
#data send to the client then later we are closing our database (using yield)
#normally what happened , when we request form api , before sending data to ther client database
#is closed, which take time
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Depends is an dependency incjection , before executing the code we inject dependency using Depends
#Annotated in python allows developers to declare the type of a reference and provide additional information related to it.
db_dependency = Annotated[Session,Depends(get_db)]
@app.get('/todos',status_code=status.HTTP_200_OK)
async def read_all(db :db_dependency):
    return db.query(Todo).all()

@app.get('/todo/{todo_id}',status_code=status.HTTP_200_OK)
async def getTodo(db:db_dependency,todo_id:int = Path(gt=0,description='id should be greater then 0')):
    data = db.query(Todo).filter(Todo.id == todo_id).first()
    if data is not None:
        return data
    raise HTTPException(status_code=404,detail='todo not found')

@app.post('/todo/create',status_code=status.HTTP_201_CREATED,)
async def addTodo(db:db_dependency,todo_request:TodoRequest):
    todo_model = Todo(**todo_request.model_dump())
    db.add(todo_model) #add make database get ready
    db.commit() #here all transaction of adding and flushing will be done

@app.put('/todo/update/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def updateTodo(db:db_dependency,todo_request:TodoRequest,todo_id:int = Path(gt=0),):
    todo_model = db.query(Todo).where(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@app.delete('/todo/delete/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(db :db_dependency,todo_id:int=Path(gt=0)):
    todo_model = db.query(Todo).where(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='todo not found ')
    db.query(Todo).filter(Todo.id == todo_model.id).delete()
    db.commit()


