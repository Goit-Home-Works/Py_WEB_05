import aiofiles
from aiopath import AsyncPath
import json
import logging
import datetime

from main import Data_exchange_pb
logging.basicConfig(level=logging.INFO)

class GetExchange:
    def __init__(self, message, name):
        self.message = message
        self.name = name
        self.data_exchange = Data_exchange_pb()

    async def get_exchange(self):
        try:
            # Parse the message to extract selected currencies and days
            command, selected_days, selected_currencies = self.message.split()

            selected_days = int(selected_days)

            # Fetch exchange rates for specified days and currencies
            results = await self.data_exchange.main(selected_days, selected_currencies)

            return results

        except Exception as e:
            logging.error(f"Error in get_exchange: {e}")
            return None

    async def send_exchange(self, ws_handler):
        try:
            exchange_data = await self.get_exchange()
            print(exchange_data)
            log_file = AsyncPath("server_log.txt")
            if exchange_data:
                await ws_handler.send(f"Exchange rates for me: ") # {self.name}:\n")
                await ws_handler.send(json.dumps(exchange_data, indent=2))
                async with aiofiles.open(log_file, 'a') as f:
                    await f.write(f"{datetime.datetime.now()} \n"
                                  f"Exchange rates for {self.name}:\n{json.dumps(exchange_data, indent=2)}\n")
        except Exception as e:
            logging.error(f"Error in send_exchange: {e}")
  