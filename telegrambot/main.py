import asyncio
import logging
import os.path
import random

import aioschedule as aioschedule
import pytube
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandHelp, Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from config import *
from telegrambot.service import register_user, select_user, select_all_users, broadcast
from utils import *
import os
from video_processing import *


TOKEN = "5701196928:AAEVNw1nHz7xlHhDxh8nKgeTu-yMp1kSxaY"

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class DownloadVideoStates(StatesGroup):
    sending_video_url = State()
    sending_music_url = State()


@dp.message_handler(Text(equals='ℹInfo', ignore_case=True))
async def get_info(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Hi, my name is Nurmukhammad and i developed this bot you can get in touch with me by texting @MENZ_UZB', reply_markup=inline_keyboard)


@dp.message_handler(Text(equals='📽Video download', ignore_case=True))
async def get_url(msg: types.Message):
    await DownloadVideoStates.sending_video_url.set()
    await bot.send_message(msg.from_user.id, "Please send the URL of Video to download it from YOUTUBE")


@dp.message_handler(Text(equals='🎶Music Download', ignore_case=True))
async def get_url(msg: types.Message):
    await DownloadVideoStates.sending_music_url.set()
    await bot.send_message(msg.from_user.id, "Please send the URL of Video to download it from YOUTUBE")


@dp.message_handler(state=DownloadVideoStates.sending_video_url)
async def uploadMediaFiles(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Downloading...')

    try:
        yt = pytube.YouTube(message.text)
        # yt = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        file_name, path = await save_to_path(yt)
        with open(os.path.join(path, file_name), 'rb') as file:
            await bot.send_video(message.chat.id, file, disable_notification=True, reply_markup=inline_keyboard)
            # await bot.send_audio(message.chat.id, file, disable_notification=True)
        await bot.send_message(message.chat.id, 'Successful!')
    except Exception as ex:
        print(ex)
        await bot.send_message(message.chat.id, 'Something wrong. Please, check the link for correct or try again')
    finally:
        await state.finish()


@dp.message_handler(state=DownloadVideoStates.sending_music_url)
async def uploadMediaFiles(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Downloading...')

    try:
        yt = pytube.YouTube(message.text)
        yt = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        # yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        file_name, path = await save_to_path(yt)
        with open(os.path.join(path, file_name), 'rb') as file:
            # await bot.send_video(message.chat.id, file, disable_notification=True)
            await bot.send_audio(message.chat.id, file, disable_notification=True, reply_markup=inline_keyboard)
        await bot.send_message(message.chat.id, 'Successful!')
    except Exception as ex:
        print(ex)
        await bot.send_message(message.chat.id, 'Something wrong. Please, check the link for correct or try again')
    finally:
        await state.finish()


async def save_to_path(yt):
    path = './videos'
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = str(random.randint(0, 100000)) + '.mp4'

    yt.download(path, filename=file_name)
    logging.info(f'Started processing {file_name}')
    return file_name, path


@dp.message_handler(Text(equals="🆘Help", ignore_case=True))
async def bot_help(message: types.Message):
    await message.answer("You can use for downloading YoutubeVideo", reply_markup=inline_keyboard)


@dp.message_handler(commands=['start'])
async def on_start(msg: types.Message):
    user = register_user(msg)

    if user:
        await msg.answer('You successfully signed in!')
    else:
        await msg.answer('You have already signed in!')

    await bot.send_message(msg.from_user.id,
                           'Hello you can use bot to download YOUTUBE Videos by sending URL',
                           reply_markup=option_btn)


@dp.message_handler(commands=['profile'])
async def show_profile(message: types.Message):
    user = select_user(message.from_user.id)

    await message.answer(f"Your profile\n"
                         f"Name: {user.name}\n"
                         f"Username: @{user.username}\n"
                         f"Admin: {'Yes' if user.admin else 'No'}")


@dp.message_handler(commands='all_users')
async def get_all_users(message: types.Message):
    user = select_user(message.from_user.id)
    if user.admin:
        users = select_all_users()
        await message.reply(f'Users list:\n{users}')
    else:
        await message.reply('You have not permission')


@dp.message_handler(Text(startswith='broadcast', ignore_case=True))
async def broadcast_message(message: types.Message):
    await message.reply(broadcast(message.text))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
