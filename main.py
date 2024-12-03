from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import asyncio, logging
from config import token
from bs4 import BeautifulSoup
import requests
import sqlite3
import time
from threading import Thread

bot = Bot(token=token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect("news.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        news TEXT
    );
""")
cursor.connection.commit()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("/news xначать /stop остонавить")

def parse_news():
    url = 'https://24.kg/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    news_list = soup.find_all('h2', class_='article__title')

    for news_item in news_list:
        news_text = news_item.text.strip()
        cursor.execute("INSERT INTO news (news) VALUES (?);", (news_text,))
        cursor.connection.commit()

@dp.message(Command("news"))
async def get_news(message: Message):

    thread = Thread(target=parse_news)
    thread.start()

    await message.answer("Парсинг новостей начался")

@dp.message(Command("stop"))
async def stop_parsing(message: Message):
    await message.answer("Парсинг новостей остановлен")


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
