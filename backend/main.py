import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from auth.routers.router import router

app = FastAPI()

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
PAGES_DIR = FRONTEND_DIR / "pages"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

app.mount("/styles", StaticFiles(directory=FRONTEND_DIR / "styles"), name="styles")
app.mount("/scripts", StaticFiles(directory=FRONTEND_DIR / "scripts"), name="scripts")
app.mount("/pages", StaticFiles(directory=PAGES_DIR), name="pages")


@app.get("/")
def home():
    return RedirectResponse(url="/pages/main.html")


@app.get("/api/health")
def health():
    return {"message": "Backend is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
