from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

option_btn = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(KeyboardButton("📽Video download"), KeyboardButton("🎶Music Download"))\
    .add(KeyboardButton("ℹInfo"))\
    .add(KeyboardButton("🆘Help"))

inline_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Buy me a coffee", url="https://t.me/MENZ_UZB"))
