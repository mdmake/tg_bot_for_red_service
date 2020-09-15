import telebot
import requests
import yaml
import os
import json
import asyncio
#import grequests
#import gevent.monkey
import aiohttp
import aiogram

import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

TOKEN = os.environ.get('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

chat_ids = {}

@dp.message_handler()
async def echo(message: types.Message):
    chat_ids[message.from_user.id] = message.from_user
    text = f'{message.message_id} {message.from_user} {message.text}'
    await message.reply(text, reply=False)









