import uvicorn
from app.core.logger import setup_logger

if __name__ == "__main__":
    setup_logger()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)