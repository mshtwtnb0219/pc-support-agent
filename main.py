from fastapi import FastAPI
from pydantic import BaseModel
from src.agent import run_agent
from fastapi.middleware.cors import CORSMiddleware



# FastAPI
app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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
