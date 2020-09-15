import os

from aiogram import Bot, Dispatcher, types
from server.server import app
from server.db import smart_change_subscriber, delete_subscriber

TOKEN = os.environ.get('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


text_for_user = "Hi!\nI'm RedLevelTgBot!\n" + \
                "my command:\n" + \
                "\n/help -- for help\n" + \
                "/start -- for start\n" + \
                "/subscribe -- if U want receive data\n" + \
                "/unsubscribe -- if U dont\n" + \
                "/remove -- if U want remove you id from our base"

text_warning = "One more thing. Im very greedy bot, so i put your data in db " \
               "after first command from list -- /subscribe or /unsubscribe ." \
               " If you want to remove it, type /remove"


text_reply = {"sub": "Congratulation! You subscribe to our service! Thank you!",
                "nc_sub": "But, but... you are already subscribe",
                "nc_unsub": "But, but... you are not subscribe yet",
                "unsub":  "You unsubscribed from our service!",
                "rem": "Your data has been deleted from our service"}


@dp.message_handler(commands=['start', 'help', 'subscribe', 'unsubscribe', 'remove'])
async def send_welcome(message: types.Message):

    t_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=False)
    t_keyboard.add(types.KeyboardButton(text="/help",))
    t_keyboard.add(types.KeyboardButton(text="/start"))
    t_keyboard.add(types.KeyboardButton(text="/subscribe"))
    t_keyboard.add(types.KeyboardButton(text="/unsubscribe"))
    t_keyboard.add(types.KeyboardButton(text="/remove"))

    if message.text == "/help":
        await message.reply(text_for_user, reply=False, reply_markup=t_keyboard)

    elif message.text == "/start":
        await message.reply(text_for_user, reply=False)
        await message.reply(text_warning, reply=False, reply_markup=t_keyboard)

    elif message.text == "/subscribe":
        result = smart_change_subscriber(app['db'], message.chat.id, state=True)
        if not result:
            await message.reply(text_reply["nc_sub"], reply=False)
        else:
            await message.reply(text_reply["sub"], reply=False)

    elif message.text == "/unsubscribe":
        result = smart_change_subscriber(app['db'], message.chat.id, state=False)
        if result == 0 or result == 2:
            await message.reply(text_reply["nc_unsub"], reply=False)
        else:
            await message.reply(text_reply["unsub"], reply=False)

    elif message.text == "/remove":
        result = delete_subscriber(app['db'], message.chat.id)
        if result:
            await message.reply(text_reply["rem"], reply=False)
        else:
            await message.reply(text_reply["nc_unsub"], reply=False)

    else:
        await message.reply("Hi!\nI'm RedLevelTgBot!\ntype /help to begin!",  reply=False)


@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("Hi!\nI'm RedLevelTgBot!\ntype /help to begin!", reply=False)


