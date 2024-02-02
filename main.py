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

    def filter_currencies(self, obj):
        filtered_currencies = list(filter(lambda x: x['currency'] in self.CURRENCIES, obj['exchangeRate']))
        return filtered_currencies

    async def format_obj(self, obj):
        filtered_currencies = self.filter_currencies(obj)
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

    async def data_from_api(self, days: List[str]):  # days: List[str] - list of days '%d.%m.%Y'
        async with asyncio.TaskGroup() as tg:
            results = []
            for date in days:
                task = tg.create_task(self.fetch_api_pb(date))
                results.append(await task)
            return results

    async def get_data(self, days_list):
        data = await self.data_from_api(days_list)
        return data

    async def format_results(self, data):
        results = []

        for day_data in data:
            result = await self.format_obj(day_data)
            results.append(result)
        return results

    async def print_results(self, results):
        print(json.dumps(results, indent=2))

    async def results_data(self, days_list, currencies):
        data = await self.get_data(days_list)
        results = await self.format_results(data)
        return results

    async def main(self):
        parser = argparse.ArgumentParser(description='Fetch exchange rates for specified days')
        parser.add_argument('days', type=int, help='Number of days to fetch exchange rates')
        parser.add_argument('--currencies', '-c', default='EUR,USD', help='Comma-separated list of currencies')
        args = parser.parse_args()
        days = args.days
        currencies = args.currencies
        self.CURRENCIES = tuple(currencies.split(','))
        days_num = min(abs(days), 10)
        days_list = await self.get_days_list(days_num)
        # days_list = ['01.12.2014', '01.12.2023']
        results = await self.results_data( days_list, currencies)

        await self.print_results(results)


if __name__ == '__main__':
    data = Data_exchange_pb()
    asyncio.run(data.main())
