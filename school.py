import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
import logging
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from googletrans import Translator
from config import TOKEN
from gtts import gTTS
import os
import sqlite3
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

def init_db():
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, grade TEXT NOT NULL)''')
    conn.commit()
    conn.close()


init_db()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет, как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком ты классе?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: types.Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    # Сохранение данных в базу данных
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age, grade) VALUES (?, ?, ?)",
                   (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    # Отправка сообщения с данными пользователю
    user_report = (f"Имя - {user_data['name']}\n"
                   f"Возраст - {user_data['age']} лет\n"
                   f"Класс - {user_data['grade']}")
    await message.answer(user_report)
    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
