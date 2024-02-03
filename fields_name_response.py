
from datetime import datetime
import requests

today = datetime.now().date()
url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={today.strftime("%d.%m.%Y")}'

# url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date=01.12.2014'
result = requests.get(url)
print(result.json())