from fastapi import FastAPI

app = FastAPI()

@app.get("/books")
async def books():
    return {"message": "noitems yet"}