from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI()

# Serve React build
app.mount("/static", StaticFiles(directory="frontend_build/static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("frontend_build/index.html")

# Optional: include other FastAPI routes here

if __name__ == "__main__":
    uvicorn.run("start:app", host="0.0.0.0", port=8000)