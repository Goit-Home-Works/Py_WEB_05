import argparse
import asyncio
import aiohttp
from datetime import datetime, timedelta
import json
import logging
from typing import List

class Data_exchange_pb:
    BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates?'
    CURRENCIES = ()

    def format_obj(self, obj):
        filtered_currencies = list(filter(lambda x: x['currency'] in self.CURRENCIES, obj['exchangeRate']))
        formatted_currencies = {
            obj['date']: {
                x['currency']: {'sale': x.get('saleRate'), 'purchase': x.get('purchaseRate')}
                for x in filtered_currencies
            }
        }
        return formatted_currencies
    async def get_days_list(self, days_num: int) -> List[str]:
        today = datetime.now().date()
        dates = [(today - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(days_num)]
        return dates

    async def fetch_api_pb(self, day):
        params = {'json': '', 'date': day}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logging.info(response.status)
        except aiohttp.ClientConnectionError as err:
            logging.info(err)

    async def data_from_api(self, days: List[str]):
        async with asyncio.TaskGroup() as tg:
            results = []
            for date in days:
                task = tg.create_task(self.fetch_api_pb(date))
                results.append(await task)
            return results

    async def main(self):
        parser = argparse.ArgumentParser(description='Fetch exchange rates for specified days')
        parser.add_argument('days', type=int, help='Number of days to fetch exchange rates')
        parser.add_argument('--currencies', '-c', default='EUR,USD', help='Comma-separated list of currencies')
        args = parser.parse_args()

        days_num = min(abs(args.days), 10)
        self.CURRENCIES = tuple(args.currencies.split(','))
        days = await self.get_days_list(days_num)
        data = await self.data_from_api(days)
        results = []
        for day_data in data:
            result = self.format_obj(day_data)
            results.append(result)
        print(json.dumps(results, indent=2))

if __name__ == '__main__':
    data = Data_exchange_pb()
    asyncio.run(data.main())
