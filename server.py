#!/usr/bin/env python3
# chmod +x server.py


from aiofiles import open as aio_open
import asyncio
from faker import Faker
import logging
import websockets
from aiopath import AsyncPath
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from extra import GetExchange

fake = Faker('uk-UA')
logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()
    
    log_file = AsyncPath("server_log.txt")

    async def register(self, ws: WebSocketServerProtocol):
        print(ws)
        ws.name = fake.name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        # if ws in self.clients:
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str, sender_ws: WebSocketServerProtocol):
        if self.clients:
            [await client.send(message) for client in self.clients if client != sender_ws]
        logging.info(message)

        async with aio_open(self.log_file, 'a') as f:
            await f.write(message + "\n")

    async def ws_handler(self, ws: WebSocketServerProtocol):
        reg = await self.register(ws)
        print(reg)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    # async def send_exchange_rate(self, name, exchange_data):
    #     result = await exchange_data.get_exchange()
    #     print(result)
    #     if result:
    #         await self.send_to_clients(f"Exchange rate for: {name}", None)
    #         await self.send_to_clients(f"{result}", None)
    #     logging.info(result)

    # async def distribute(self, ws: WebSocketServerProtocol):
    #     async for message in ws:
    #         if message.lstrip().startswith("exchange"):
    #             exchange_data = GetExchange(message, ws.name)
    #             await exchange_data.send_exchange(ws)
    #         else:
    #             await self.send_to_clients(f"{ws.name}: {message}", ws)


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, '0.0.0.0', 8081) as server:
        await server.server.serve_forever()



if __name__ == '__main__':

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown")
        
