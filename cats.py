import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
import logging

from aiogram.types import Message, FSInputFile, CallbackQuery
from googletrans import Translator
from config import TOKEN, THE_CAR_API_KEY

from gtts import gTTS
import keyboards as kb
import os


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_cat_breeds():
    url = 'https://api.thecatapi.com/v1/breeds'
    headers = {'x-api-key' : THE_CAR_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def get_cat_image_by_breed(breed_id):
    url = f'https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}'
    headers = {'x-api-key' : THE_CAR_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']

def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Напиши название пароды котика")


@dp.message()
async def send_cat_info(message: Message):
    breed_name = message.text
    bread_info = get_breed_info(breed_name)
    if bread_info:
        cat_image_url = get_cat_image_by_breed(bread_info['id'])
        info = (f"Породе {bread_info['name']}\n"
            f"Описание - {bread_info['description']}\n"
            f"Продолжительность жизни - {bread_info['life_span']} лет")
        await message.answer_photo(photo=cat_image_url, caption=info)
    else:
        await message.answer("Такой породы нет, попробуйте еще раз")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
