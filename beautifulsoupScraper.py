import requests
from bs4 import BeautifulSoup
import time

url = 'https://finance.yahoo.com/quote/AAPL'
headers = {'User-Agent': 'Mozilla/5.0'}

while True:
    response = requests.get(url, headers=headers)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')
    price = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
    print(f'Current Price: {price}')

    # Wait for 10 seconds before the next request
    time.sleep(10)
