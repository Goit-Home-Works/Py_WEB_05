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

class Server:
    clients = set()
    log_messages = [] 
    log_file = AsyncPath("server_log.txt")

    def __init__(self):
        self.logger = DualLogger(log_file_path=self.log_file)

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = fake.name()
        self.clients.add(ws)
        self.log_messages.append(f'{ws.name}-{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        self.log_messages.append(f'{ws.name}-{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str, sender_ws: WebSocketServerProtocol = None):
        # if self.clients:
        #     [await client.send(message) for client in self.clients if client != sender_ws]
        if self.clients:
            for client in list(self.clients):
                if client != sender_ws and client.open:
                    await client.send(message)

            

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)


    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.lstrip().startswith("exchange"):
                exchange_data = GetExchange(message, ws.name)
                result = await exchange_data.send_exchange(ws)

                if result is not None:
                    msg = f"Exchange rate for: {ws.name} {result}"
                    self.log_messages.append(msg)
                    print("message: ", msg)
                    print(self.log_messages)
            else:
                msg = f"{ws.name}: {message}"
                await self.send_to_clients(msg, sender_ws=ws)
                self.log_messages.append(msg)
                print("message: ", msg)
                print(self.log_messages)

    async def write_logs_to_file(self):
        async with aio_open(self.log_file, 'a') as file:
            for log_message in self.log_messages:
                await file.write(log_message + '\n')




async def main():
    server = Server()

    try:
        async with websockets.serve(server.ws_handler, 'localhost', 8081):
            await asyncio.Future()
    except KeyboardInterrupt:
        print("\nShutdown")
    finally:
        await server.write_logs_to_file()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown")

        
        