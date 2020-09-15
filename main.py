from server.server import server, app
from tg_app.telegramm import dp
from aiogram import executor


dp.loop.create_task(server(app))
executor.start_polling(dp, skip_updates=True)
