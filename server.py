import asyncio
from aiohttp import web


async def handler(request):
    print("accept!!!", request.text)
    return web.Response(text="OK !!!!!!")


async def server():
    app = web.Application()
    app.add_routes([web.get('/fromservice', handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=8080)
    await site.start()

    print("======= Serving on http://127.0.0.1:8080/ ======")