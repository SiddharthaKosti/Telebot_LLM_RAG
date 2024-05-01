# Telegram-LLM-chatbot

## create new env 
python -m venv env_name

## activate the env
env_name/bin/activate **(Mac/Linux)**

env_name\Scripts\activate **(Windows)**

## install the requirements
pip install -r requirements_telebot.txt

## generate the telegram bot api key (reference doc)
https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/

## download the model from hugging-face: llama-2-7b-chat.ggmlv3.q4_0.bin and keep it in structure model/model_bin_file
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main

## run the app
python main_bot.py 
