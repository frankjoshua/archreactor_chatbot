from fastapi import FastAPI
from bot import ChatBot
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

chat_bot = ChatBot()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BotRequest(BaseModel):
    question: str

@app.post("/")
def root(botRequest: BotRequest):
    response = chat_bot(botRequest.question)
    return {"message": response}

