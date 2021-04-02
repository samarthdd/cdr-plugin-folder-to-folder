from fastapi import FastAPI
import uvicorn
from file_iteration import Loops

app = FastAPI()

@app.get("/")
def read_root():
    return "FastAPI Home"

@app.get("/loop")
def run_the_loop():
    Loops.LoopHashDirectories()
    return "Loop completed"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=80, log_level="info")