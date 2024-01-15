import database.book_db as db
from fastapi import  FastAPI
from models.book_model import  BookRequest,Book

app = FastAPI()
db.loadData()


@app.get('/books')
async  def getBooks():
    return db.booklist

@app.post('/createbook')
async def createbook(data:BookRequest):
    try:
        b =Book(**data.model_dump())
        db.booklist.append(b)
        return True
    except:
        return False