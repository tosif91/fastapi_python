from fastapi import FastAPI
from routes import user_routes,book_routes
from auth import auth_service


app = FastAPI()

app.include_router(auth_service.router)
app.include_router(user_routes.router)
app.include_router(book_routes.router)
