from fastapi import FastAPI
from bot import ChatBot
from pydantic import BaseModel

chat_bot = ChatBot()
app = FastAPI()

class BotRequest(BaseModel):
    question: str

@app.get("/")
def root(botRequest: BotRequest):
    response = chat_bot(botRequest.question)
    return {"message": response}

