from fastapi import FastAPI

app = FastAPI()
#to run the code user cmd : uvicorn basic:app --reload
#here uvicorn is ther webserver that comes installed with the fastapi
@app.get('/endpoint')
async def firstapi():  #async is not explicictly needed in fastapi  , fast api automatically add it
    return {"message" : "welcome to fast api"}