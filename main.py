import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
import logging
from aiogram.types import Message
from config import TOKEN

logging.basicConfig(level=logging.INFO)


WEATHER_API_KEY = '2b350a87de1accceaaa66f9966efb1fe'
CITY_NAME = 'Minsk'

bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        description = weather["description"]
        return f"Температура в {CITY_NAME}: {temperature}°C\nОписание: {description.capitalize()}"
    else:
        return "Город не найден."
@dp.message(Command('weather'))
async def send_weather(message: types.Message):
    weather_info = get_weather()
    await message.reply(weather_info)


@dp.message(Command('photo'))
async def photo(message: Message):
    list = ["https://avatars.mds.yandex.net/i?id=de0084100c904d6817d4ebefa7719dbd0bb6e4c6-12421110-images-thumbs&n=13", "https://avatars.mds.yandex.net/i?id=1f8bbfb8a1a86aece3839f53e3956258a8858587eaaecef3-4564518-images-thumbs&n=13", "https://avatars.mds.yandex.net/i?id=c8bdc409edbf8becd52e08a61f2120023aef07b2-10805549-images-thumbs&n=13"]
    list1 = ["Линейка старый", "Раскольникова", "Дрюня"]
    rand_photo = random.choice(list)
    rand_answ = random.choice(list1)

    await message.answer_photo(photo=rand_photo, caption=rand_answ)

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ["Кот в сапогах", "Зачем совам уши?", "Ловкий пингвин", "Закат на пляже"]
    rand_answ = random.choice(list)
    await message.answer(rand_answ)

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("Искусственный интеллект (ИИ) — это компьютерная программа, которая принимает и анализирует данные, а затем делает выводы на их основе.")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(f"Этот бот умеет выполнять следующие команды:\n/help - помощь\n/start - запуск бота\n/photo - случайное фото\n Что такое ИИ? - информация по запросу\n Примечание: бот реагирует на отправку фото")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
