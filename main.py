from server import server
from telegramm import dp
from aiogram import executor


if __name__ == '__main__':
    dp.loop.create_task(server())
    executor.start_polling(dp)


