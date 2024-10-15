import chainlit as cl
from bot import ChatBot

chat_bot = ChatBot()

@cl.on_message  # this function will be called every time a user inputs a message in the UI
async def main(message: str):
    print(message)
    response = chat_bot(message)
    print(response)
    # send back the final answer
    await cl.Message(
        content = response['output_text']
    ).send()

# @cl.langchain_factory(use_async=False)
# def factory():
#     return chat_bot.getChain()