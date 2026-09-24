from pydantic import BaseModel
from src.agent import run_agent
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
from fastapi import FastAPI, HTTPException
from openai import RateLimitError


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



class ChatMessage(BaseModel):
    role: Literal["user","agent"]
    content: str
    
class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []
    
#　　JSONのイメージ 
# {
#   "message": "次は何を確認すればいい？",
#   "history": [
#     {
#       "role": "user",
#       "content": "DNSがおかしいです"
#     },
#     {
#       "role": "agent",
#       "content": "まずDNSの状態を確認しましょう"
#     }
#   ]
# }

@app.get("/")
def root():
    return {"message": "Hello Pc Support Agent v2"}

@app.post("/chat")
def chat(request: ChatRequest):
    
    
        # 429テスト用
    # if request.message == "test429":
    #     raise HTTPException(
    #         status_code=429,
    #         detail="429テスト"
    #     )

    try:
        answer = run_agent(request.message, request.history)
        return {"answer": answer}
    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Open APIの利用条件に達したか、一時的にリクエストが集中しています。"
        )

        
    
    
