from aiohttp import web
import os
import requests

from server.db import init_db, get_all_subscriber
port = int(os.environ.get('PORT', 8000))
TOKEN = os.environ.get('TOKEN')


app = web.Application()


def sed_message_to_user(chat_id, text):
    message = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
    requests.get(message)


def send_to_all_sunscribers(app, text):
    subscribesr_list = get_all_subscriber(app["db"], state=True)

    for user in subscribesr_list:
        sed_message_to_user(user, text)


async def red_service_handler(request):
    text = await request.text()
    send_to_all_sunscribers(app, text)
    return web.Response(text="OK")


async def server(app):
    app.on_startup.append(init_db)
    app.add_routes([web.post('/fromservice', red_service_handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=port)
    await site.start()

    print(f"======= Serving on http://127.0.0.1:{port}/ ======")
