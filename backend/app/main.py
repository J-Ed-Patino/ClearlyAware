from typing import Union
from fastapi import FastAPI

app = FastAPI( title="ClearlyAwar", description="Personal budget tracker with bank integration", version="0.1.0" )

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def check_health():
    return {"status": "working"}
 