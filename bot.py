from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import States
from config import token, weather_token, youtube_token
import keyboards as kb
from pyowm import OWM
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup as bs
import random

# aiogram
# states
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
# pyowm
owm = OWM(weather_token)
mgr = owm.weather_manager()
# youtube
youtube = build('youtube', 'v3', developerKey=youtube_token)


# Start menu
@dp.message_handler(commands=['start'], state=None)
async def send_welcome(message: types.Message):
    await message.answer("Welcome, " + message.from_user.first_name + '\nChoose the option', reply_markup=kb.menu_kb)
    await States.menu.set()


# WEATHER
@dp.callback_query_handler(lambda c: c.data == 'weather', state=States.menu)
async def get_weather(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Kindly,write the name of the city following')
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await States.weather.set()

    @dp.message_handler(state=States.weather)
    async def send_weather(message: types.Message):
        try:
            observation = mgr.weather_at_place(message.text)
            w = observation.weather
            await message.answer((message.text).upper() + f'\n🌡Avarage temp:{w.temperature("celsius")["temp"]},'
                                                          f'\n☁{w.detailed_status}', reply_markup=kb.back1_kb)

        except:
            await message.answer('Sorry, I`m didn`t find this city😢', reply_markup=kb.back1_kb)


# Music
@dp.callback_query_handler(lambda c: c.data == 'music', state=States.menu)
async def get_music(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Enter the name of the video')
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await States.music.set()

    @dp.message_handler(state=States.music)
    async def send_music(message: types.Message):
        youtube_request = youtube.search().list(q=message.text, part='snippet', type='video', maxResults=3)
        res = youtube_request.execute()

        for item in res['items']:
            await message.answer(
                'Title:' + item['snippet']['title'] + '\nLink:' + 'https://www.youtube.com/watch?v=' + item['id'][
                    'videoId'])
        await message.answer('Back to menu', reply_markup=kb.back1_kb)


# News

@dp.callback_query_handler(lambda c: c.data == 'news', state=States.menu)
async def get_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose type of news', reply_markup=kb.news_kb)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await States.news.set()


@dp.callback_query_handler(lambda c: c.data == 'politic', state=States.news)
async def send_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    r = requests.get('https://www.nytimes.com/section/world/europe')
    html = bs(r.text, 'lxml')
    div = html.find_all('div', class_='css-1l4spti')
    urls = []

    for i in div:
        a = i.find('a')
        url = a.get('href')
        urls.append(str(url))
    send_url = random.choice(urls)
    await bot.send_message(callback_query.from_user.id, f'https://www.nytimes.com/{send_url}', reply_markup=kb.back1_kb)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'economy', state=States.news)
async def send_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    r = requests.get('https://www.nytimes.com/section/business/economy')
    html = bs(r.text, 'lxml')
    div = html.find_all('div', class_='css-1l4spti')
    urls = []

    for i in div:
        a = i.find('a')
        url = a.get('href')
        urls.append(str(url))
    send_url = random.choice(urls)
    await bot.send_message(callback_query.from_user.id, f'https://www.nytimes.com/{send_url}', reply_markup=kb.back1_kb)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'science', state=States.news)
async def send_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    r = requests.get('https://www.nytimes.com/section/science?auth=link-dismiss-google1tap')
    html = bs(r.text, 'lxml')
    div = html.find_all('div', class_='css-1l4spti')
    urls = []

    for i in div:
        a = i.find('a')
        url = a.get('href')
        urls.append(str(url))
    send_url = random.choice(urls)
    await bot.send_message(callback_query.from_user.id, f'https://www.nytimes.com/{send_url}', reply_markup=kb.back1_kb)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


#Books
@dp.callback_query_handler(lambda c: c.data == 'books', state=States.menu)
async def send_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose an option', reply_markup=kb.books_kb)
    await States.books.set()

@dp.callback_query_handler(lambda c: c.data == 'art_l', state=States.books)
async def send_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    r = requests.get('https://www.goodreads.com/genres/most_read/art')
    html = bs(r.text, 'lxml')
    div = html.find_all('div', class_='coverWrapper')
    urls = []
    for i in div:
        a = i.find('a')
        url = a.get('href')
        urls.append(str(url))
    book_list = random.sample(urls, 3)
    for m in book_list:
        await bot.send_message(callback_query.from_user.id, f'https://www.goodreads.com/{m}', reply_markup=kb.back1_kb)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'science_l', state=States.books)
async def send_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    r = requests.get('https://www.goodreads.com/genres/most_read/science')
    html = bs(r.text, 'lxml')
    div = html.find_all('div', class_='coverWrapper')
    urls = []
    for i in div:
        a = i.find('a')
        url = a.get('href')
        urls.append(str(url))
    book_list = random.sample(urls, 3)
    for m in book_list:
        await bot.send_message(callback_query.from_user.id, f'https://www.goodreads.com/{m}', reply_markup=kb.back1_kb)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
@dp.callback_query_handler(lambda c: c.data == 'self_l', state=States.books)
async def send_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    r = requests.get('https://www.goodreads.com/shelf/show/psychology-self-development')
    html = bs(r.text, 'lxml')
    div = html.find_all('div', class_='left')
    urls=[]
    for i in div:
        a = i.find('a')
        url = a.get('href')
        urls.append(str(url))
    book_list = random.sample(urls,3)
    for m in book_list:
        await bot.send_message(callback_query.from_user.id,f'https://www.goodreads.com/{m}', reply_markup=kb.back1_kb)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
# BackToMenu
@dp.callback_query_handler(lambda c: c.data == 'back1', state=States.all_states)
async def menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Welcome, " + callback_query.from_user.first_name +
                           '\nChoose the option', reply_markup=kb.menu_kb)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await States.menu.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
