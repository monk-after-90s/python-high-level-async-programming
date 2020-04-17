'''
这是一个集中展示协程打印信息的服务端
'''
import asyncio
from datetime import datetime

clients = {}


async def handle_echo(reader, writer):
    while True:
        data = await reader.read(100)
        message = str(data.decode())
        name = message[:message.find(':')]
        # 注册客户端
        if name not in clients.keys():
            clients[name] = (reader, writer)

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:{message!r}")

        if 'ends' in message or 'canceled' in message:
            clients.pop(name)
            break
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
