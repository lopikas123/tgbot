import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
import logging

from aiogram.types import Message, FSInputFile, CallbackQuery
from googletrans import Translator
from config import TOKEN, NEWS_API_KEY, NEWS_API_URL



logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


translator = Translator()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Напишите команду /news для получения новостей.")
async def fetch_news():
    params = {
        "country": "us",
        "apiKey": NEWS_API_KEY
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()  # Это вызовет HTTPError, если код ответа 4xx или 5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при получении новостей: {e}")
        return None

@dp.message(Command("news"))
async def send_news(message: types.Message):
    news_data = await fetch_news()
    if not news_data:
        await message.answer("Не удалось получить новости.")
        return

    if news_data.get("status") == "ok":
        articles = news_data.get("articles", [])
        if articles:
            for article in articles[:5]:
                title = article.get("title")
                description = article.get("description")
                url = article.get("url")

                # Перевод заголовка и описания на русский
                title_ru = translator.translate(title, dest='ru').text if title else "Нет заголовка"
                description_ru = translator.translate(description, dest='ru').text if description else "Нет описания"

                await message.answer(f"Заголовок: {title_ru}\nОписание: {description_ru}\nСсылка: {url}")
        else:
            await message.answer("Новости не найдены.")
    else:
        await message.answer("Не удалось получить новости.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
