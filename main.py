from fastapi import FastAPI
from src.books.router import router as book_router
from src.users.router import router as user_router
from src.auth.router import router as auth_router
from src.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(auth_router)
app.include_router(book_router)
app.include_router(user_router)
