import chainlit as cl
from bot import ChatBot

chat_bot = ChatBot()

@cl.on_message  # this function will be called every time a user inputs a message in the UI
def main(message: str):
    print(message)
    response = chat_bot(message)
    print(response)
    # send back the final answer
    # cl.send_message(response["output_text"])
    cl.Message(
        response["output_text"]
    ).send()