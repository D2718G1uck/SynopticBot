# -*- coding: cp1251 -*-
import asyncio
import nltk
import requests
import json

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from nltk.chat.util import Chat, reflections
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
#nltk.download('popular')
#nltk.download('punkt_tab')

TOKEN = "8032096744:AAFkJOx0DMUg0Vqc5Ris1GgRN7U2WCKKGAk"
API = '78b6039979316269aa28bb247c948fd8'

bot = Bot(token=TOKEN)
dp = Dispatcher()

pairs = [
    ['привет|здравствуй|здравствуйте', ['Привет!', 'Здравствуйте!Как дела?']], 
    ['Как тебя зовут?|зовут|ты', ['Меня зовут бот-синоптик', 'Я бот бот-синоптик, приятно познакомиться!']],
    ['пока|до свидания',['До свидания!', 'Пока!']],
    ['как дела?|дела',['Отлично!', 'Всё супер!', 'Плохо(', 'Неважно','Шикарно']],
    ['Что ты умеешь?|умеешь|занимаешься|делаешь|помощь', ['Я могу отвечать на простые вопросы и узнавать какая сейчас погода.']],
    ['Погода|как это работает|работа', ['Что бы узнать какая сейчас погода напиши название города']],
    ['(.*)', ['Извините, я вас не понимаю, возможно вы неправильно ввели город.']]
]

@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    await message.reply(f"Привет, {user_full_name}! Я бот-синоптик. Чем могу помочь?")

@dp.message()
async def chat_bot(message: Message):
     city = message.text.strip().lower() 
     chat = Chat(pairs, reflections)
     text=f"{message.text}"
     #tokens_q = word_tokenize(text)#разбиваем вопрос на слова
     #stop_words = set(stopwords.words('russian'))#стоп слова
     #filtered_tokens = [word for word in tokens_q if word not in stop_words]#удаление стоп слов из вопроса
     response = chat.respond(text) #отвечам на вопрос
     tokens_r = word_tokenize(response) #разбиваем ответ на слова
     if (tokens_r[0] == 'Извините'):
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        data = json.loads(res.text)
        #await message.reply(f'{data}')
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            await message.reply(f'Сейчас погода в городе: {temp} °C,')
     else:  
         await message.reply(response)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
   try:
      asyncio.run(main())
   except KeyboardInterrupt:
       print('Exit')