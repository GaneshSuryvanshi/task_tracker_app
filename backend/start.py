from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import logging

from main import app  # Import the FastAPI app from main.py

# Mount React static files
#app.mount("/static", StaticFiles(directory="frontend_build/static"), name="static")

#@app.get("/")
#def serve_react_index():
#    return FileResponse("frontend_build/index.html")

logging.basicConfig(level=logging.INFO)
logging.info("Starting FastAPI app from start.py...")

if __name__ == "__main__":
    logging.info("Running Uvicorn server...")
    uvicorn.run(
        "start:app",
        host="0.0.0.0",
        port=8000,
        proxy_headers=True,              # <-- Add this
        forwarded_allow_ips="*",         # <-- And this
    )
