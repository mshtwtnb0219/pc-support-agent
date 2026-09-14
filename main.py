from fastapi import FastAPI
from pydantic import BaseModel
from src.agent import run_agent



# FastAPI
app = FastAPI()



class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "Hello Pc Support Agent v2"}

@app.post("/chat")
def chat(request: ChatRequest):
    answer = run_agent(request.message)
    return {
        "answer": answer
    }
