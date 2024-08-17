from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
#привет и пока
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Привет')],
    [KeyboardButton(text='Пока')],
], resize_keyboard=True)

#ссылки

#опции

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Показать больше', callback_data='dinamics')],
], resize_keyboard=True)

test = ["Опция 1"]
test1 = ["Опция 2"]
async def test_keyboard():
    kb = InlineKeyboardBuilder()
    for key in test:
        kb.add(InlineKeyboardButton(text=key, callback_data="opt1"))
        for key1 in test1:
            kb.add(InlineKeyboardButton(text=key1, callback_data="opt2"))
        return kb.as_markup()

#main = ReplyKeyboardMarkup(keyboard=[
 #   [KeyboardButton(text='Привет')],
 #   [KeyboardButton(text='Пока')],
#], resize_keyboard=True)


inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Новость', url="https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuTnNHZ0pUU1NnQVAB?hl=ru&gl=RU&ceid=RU:ru")],
    [InlineKeyboardButton(text='Музыка', url="https://www.youtube.com/watch?v=NnfqY_b_-fg")],
    [InlineKeyboardButton(text='Видео', url="https://www.youtube.com/watch?v=jdUfiXCt_Gw&t=794s")],
], resize_keyboard=True)
