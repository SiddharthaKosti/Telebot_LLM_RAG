from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
from llm_ans import LlmResponse

load_dotenv()
tele_bot_token = os.getenv("tele_bot_token")

bot_obj = Bot(tele_bot_token)
dp = Dispatcher(bot_obj)

class Reference:
    def __init__(self) -> None:
        self.response = ""


reference = Reference()

def clear_the_past():
    reference.response = ""


@dp.message_handler(commands=["start"])
async def welcome(message: types.message):
    await message.reply("Hi!, I'm an Echo bot.\nWelcome to my world")

@dp.message_handler(commands=["help"])
async def helper(message: types.message):
    help_commands = """
    Hi!, I'm an Echo bot.\nHow can I help you
    /start : To start the sonversation
    /clear : To clear the past context
    /help : To get help menu
    """
    await message.reply(help_commands)


@dp.message_handler()
async def main_bot(message: types.Message):
    llm_response_obj = LlmResponse(message.text)
    result = llm_response_obj.get_response()
    print(result["result"])
    await message.reply(result["result"])
    # await bot_obj.send_message(chat_id = message.chat.id, text = reference.llm_response_obj)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)