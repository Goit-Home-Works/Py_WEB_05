#!/usr/bin/env python3
# chmod +x server.py


import asyncio
from aiofiles import open as aio_open
from aiopath import AsyncPath
import datetime
from faker import Faker
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from extra import GetExchange
from dual_logger import DualLogger


fake = Faker('uk-UA')

# from aiologger import Logger
# from aiologger.handlers.streams import AsyncStreamHandler
# from aiologger.handlers.files import AsyncFileHandler


class Server:
    clients = set()
    
    log_file = AsyncPath("server_log.txt")

    def __init__(self):
        self.logger = DualLogger(log_file_path=self.log_file)

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = fake.name()
        self.clients.add(ws)
        # self.logger.logger.info(f'{ws.name}-{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        # self.logger.logger.info(f'{ws.name}-{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str, sender_ws: WebSocketServerProtocol = None):
        if self.clients:
            [await client.send(message) for client in self.clients if client != sender_ws]
            # self.logger.logger.info(message) всі відкрити страніци перезавантажцються...???

            

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def send_exchange_rate(self, name, exchange_data):
        result = await exchange_data.get_exchange()
        if result:
            await self.send_to_clients(f"Exchange rate for: {name}", sender_ws=None)
            await self.send_to_clients(f"{result}", sender_ws=None)
            msg = f"Exchange rate for: {name} {result}"
            # self.logger.logger.info(msg)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.lstrip().startswith("exchange"):
                exchange_data = GetExchange(message, ws.name)
                await exchange_data.send_exchange(ws)
            else:
                msg = f"{ws.name}: {message}"
                await self.send_to_clients(msg, sender_ws=ws)
                # self.logger.logger.info(msg)

async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8081):
        await asyncio.Future()
   

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown")
        
        