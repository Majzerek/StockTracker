import time
import requests
import datetime as dt
from twilio.rest import Client
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

today_date = dt.datetime.now().date()
day = today_date.day
day_2 = today_date.day

is_up = False
is_down = False

#  ============================= function for 0 in time.data()  ===========================  #

def add_zero_to_day():
    global day, day_2
    if day == 10 and day_2 == 10:
        day_2 -= 2
        day -= 1
        day = f"0{day}"
        day_2 = f"0{day_2}"
        return day, day_2
    else:
        day -= 1
        day_2 -= 2
        return day, day_2


add_zero_to_day()
#  ============================= Days Yesterday and two day before ===========================  #
yesterday_date = f"{year}-{month}-{day}"
two_day_before_date = f"{year}-{month}-{day_2}"


#  ============================= Api Stock ===========================  #
API_KEY_ALPHA = os.environ.get("SECRET_KEY")
API_SITE_ALPHA = "https://www.alphavantage.co/query"
parameter_tesla = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": API_KEY_ALPHA,
}

response_stock = requests.get(url=API_SITE_ALPHA, params=parameter_tesla)
response_stock.raise_for_status()
tesla_stock = response_stock.json()
stock = tesla_stock['Time Series (Daily)']

#  ============================= Yesterday Stock ===========================  #
yesterday_stock = float(stock[yesterday_date]['1. open'])
yesterday_high = float(stock[yesterday_date]['2. high'])
yesterday_close = float(stock[yesterday_date]['4. close'])

#  ============================= Two Day Before Stock ===========================  #
day_before_yesterday = float(stock[two_day_before_date]['1. open'])
day_before_high = float(stock[two_day_before_date]['2. high'])
day_before_close = float(stock[two_day_before_date]['4. close'])

#  ============================= Difference between open season ===========================  #

difference_open = round(yesterday_close - day_before_close, 2)
difference = (difference_open / yesterday_close) * 100

difference = round((difference_open / yesterday_close) * 100, 2)
#  ============================= Fast sell or cry ? ===========================  #


def up_or_down():
    global is_down, is_up
    if  difference > -5:
        is_down = True
        return is_down
    elif difference < 5:
        is_up = True
        return is_up


difference = round((abs(difference_open) / yesterday_close) * 100, 2)
#  ============================= News Paper Api ===========================  #
API_SITE = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
parameter = {
    "q": COMPANY_NAME,
    "from": today_date,
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY,
}
response_news = requests.get(url=API_SITE, params=parameter)
response_news.raise_for_status()
article_slice = response_news.json()['articles'][0:3]

article_list = []
article_author = []
for article in article_slice:
    article_list.append(article['title'])
    article_author.append(article['author'])

#  ============================= Send message ===========================  #
account_sid = os.environ.get("ACC_SID")
auth_token = os.environ.get("TILIO_TOKEN")
while True:
    time.sleep(5) # 60 * 30
    if is_down:
        # client = Client(account_sid, auth_token)
        # message = client.messages \
        #     .create(
        #     body=f"{STOCK}: 🔻{difference_open}%\n{article_author[0]}: {article_list[0]}\n"
        #          f"{article_author[1]}: {article_list[1]}\n"
        #          f"{article_author[2]}: {article_list[2]}",
        #     from_='example',
        #     to='example'
        # )
        # print(message.status)
        print(f"{STOCK}: 🔻{difference}%\n{article_author[0]}: {article_list[0]}\n"
                        f"{article_author[1]}: {article_list[1]}\n"
                        f"{article_author[2]}: {article_list[2]}")
    elif is_up:
        # client = Client(account_sid, auth_token)
        # message = client.messages \
        #     .create(
        #     body=f"{STOCK}: 🔺{difference_open}%\n{article_author[0]}: {article_list[0]}\n"
        #          f"{article_author[1]}: {article_list[1]}\n"
        #          f"{article_author[2]}: {article_list[2]}",
        #     from_='example',
        #     to='example'
        # )
        # print(message.status)
        print(f"{STOCK}: 🔺{difference}%\n{article_author[0]}: {article_list[0]}\n"
                        f"{article_author[1]}: {article_list[1]}\n"
                        f"{article_author[2]}: {article_list[2]}")


#Optional: Format the SMS message like this: 
