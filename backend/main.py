from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from auth.routers.router import router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")

def home(): 
    return {"message": "Backend is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)