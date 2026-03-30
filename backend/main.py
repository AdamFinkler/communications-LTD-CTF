from fastapi import FastAPI
import uvicorn
from database import setup
from auth.routers.router import router


app = FastAPI()

app.include_router(router)


@app.get("/")

def home(): 
    return {"message": "Backend is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)