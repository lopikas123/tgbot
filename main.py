import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
import logging
from aiogram.types import Message, FSInputFile
from googletrans import Translator
from config import TOKEN
from gtts import gTTS
import os


logging.basicConfig(level=logging.INFO)

WEATHER_API_KEY = '2b350a87de1accceaaa66f9966efb1fe'
CITY_NAME = 'Minsk'

bot = Bot(token=TOKEN)
dp = Dispatcher()

#погода
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


#видео
@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

#документы

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile('TG02.pdf')
    await bot.send_document(message.chat.id, doc)

#голосовое сообщение

@dp.message(Command('voice'))
async def audio(message: Message):
    voice = FSInputFile('audio.ogg')
    await message.answer_voice(voice)

#аудио
@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('audio.mp3')
    await bot.send_audio(message.chat.id, audio)

#команда фото
@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1: Силовая тренировка\nЦель: Развитие мышечной массы и силы\nУпражнения: Приседания со штангой, Жим лёжа, Тяга верхнего блока, Жим стоя\nПродолжительность: 60 минут\nИнтенсивность: Высокая",
        "Тренировка 2: Кардиотренировка\nЦель: Улучшение сердечно-сосудистой выносливости и сжигание калорий\nУпражнения: Бег на дорожке, Велотренажёр, Гребной тренажёр, Скакалка\nПродолжительность: 45 минут\nИнтенсивность: Средняя",
        "Тренировка 3: Функциональная тренировка\nЦель: Улучшение общей физической подготовки, координации и баланса\nУпражнения: Бёрпи, Планка, Выпады с гантелями, Махи гирей\nПродолжительность: 50 минут\nИнтенсивность: Высокая",
        "Тренировка 4: Йога\nЦель: Улучшение гибкости, укрепление мышц и релаксация\nУпражнения: Позы собаки мордой вниз, Виньяса, Поза воина, Медитация\nПродолжительность: 60 минут\nИнтенсивность: Низкая",
        "Тренировка 5: Интервальная тренировка высокой интенсивности (HIIT)\nЦель: Быстрое сжигание жира и улучшение выносливости\nУпражнения: Спринты, Плиометрические прыжки, Боковые выпады, Альпинист\nПродолжительность: 30 минут\nИнтенсивность: Очень высокая"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини тренировка на сегодня {rand_tr}")

    tts = gTTS(text=rand_tr, lang="ru")
    tts.save("training.ogg")
    voice = FSInputFile("training.ogg")
    await bot.send_voice(message.chat.id, voice)
    os.remove("training.ogg")


#команда фото
@dp.message(Command('photo'))
async def photo(message: Message):
    list = ["https://avatars.mds.yandex.net/i?id=de0084100c904d6817d4ebefa7719dbd0bb6e4c6-12421110-images-thumbs&n=13", "https://avatars.mds.yandex.net/i?id=1f8bbfb8a1a86aece3839f53e3956258a8858587eaaecef3-4564518-images-thumbs&n=13", "https://avatars.mds.yandex.net/i?id=c8bdc409edbf8becd52e08a61f2120023aef07b2-10805549-images-thumbs&n=13"]
    list1 = ["Линейка старый", "Раскольникова", "Дрюня"]
    rand_photo = random.choice(list)
    rand_answ = random.choice(list1)

    await message.answer_photo(photo=rand_photo, caption=rand_answ)

#реакция на фото
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ["Кот в сапогах", "Зачем совам уши?", "Ловкий пингвин", "Закат на пляже"]
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f"tmp/{message.photo[-1].file_id}.jpg")
#ответ на вопрос
@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("Искусственный интеллект (ИИ) — это компьютерная программа, которая принимает и анализирует данные, а затем делает выводы на их основе.")
#ответ на привет
    @dp.message()
    async def start(message: Message):
        if message.text.lower() == "привет":
            await message.answer(f"Привет, {message.from_user.full_name}!")


#помощь
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(f"Этот бот умеет выполнять следующие команды:\n/help - помощь\n/start - запуск бота\n/photo - случайное фото\n Что такое ИИ? - информация по запросу\n /weather - погода \n Примечание: бот реагирует на отправку фото")
#старт
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")

#перевод на английский

translator = Translator()

@dp.message()
async def translate_mesesag(message: Message):
    # Переводим текст сообщения на английский
    translated = translator.translate(message.text, dest='en')
    # Отправляем переведенный текст пользователю
    await message.answer(translated.text)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
