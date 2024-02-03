import asyncio
import logging
import websockets
import names  #https://pypi.org/project/names/
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from extra import GetExchange


logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str, sender_ws: WebSocketServerProtocol):
        if self.clients:
            [await client.send(message) for client in self.clients if client != sender_ws]
        logging.info(message)
    async def ws_handler(self, ws: WebSocketServerProtocol):
        reg = await self.register(ws)
        print(reg)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            await self.send_to_clients(f"{ws.name}: {message}", ws)


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080) as server:
        await server.server.serve_forever() 

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown")
        
