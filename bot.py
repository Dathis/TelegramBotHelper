from aiogram import Bot, Dispatcher, executor, types
from config import token, weather_token, youtube_token
import keyboards as kb
from pyowm import OWM
from googleapiclient.discovery import build

# aiogram
bot = Bot(token=token)
dp = Dispatcher(bot)
# pyowm
owm = OWM(weather_token)
mgr = owm.weather_manager()
# youtube
youtube = build('youtube', 'v3', developerKey=youtube_token)


# Start menu
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Welcome, " + message.from_user.first_name + '\nChoose the option', reply_markup=kb.menu_kb)


# WEATHER
@dp.callback_query_handler(lambda c: c.data == 'weather')
async def get_weather(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Kindly,write the name of the city following')
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

    @dp.message_handler()
    async def send_weather(message: types.Message):
        try:
            observation = mgr.weather_at_place(message.text)
            w = observation.weather
            await message.answer((message.text).upper() + f'\n🌡Avarage temp:{w.temperature("celsius")["temp"]},'
                                                          f'\n☁{w.detailed_status}', reply_markup=kb.back1_kb)

        except:
            await message.answer('Sorry, I`m didn`t find this city😢', reply_markup=kb.back1_kb)


# Music
@dp.callback_query_handler(lambda c: c.data == 'music')
async def get_music(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Enter the name of the video')
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

    @dp.message_handler()
    async def send_music(message: types.Message):
        youtube_request = youtube.search().list(q=message.text, part='snippet', type='video', maxResults=3)
        res = youtube_request.execute()

        for item in res['items']:
            await message.answer(
                'Title:' + item['snippet']['title'] + '\nLink:' + 'https://www.youtube.com/watch?v=' + item['id'][
                    'videoId'])
        await message.answer('Back to menu', reply_markup=kb.back1_kb)


# BackToMenu
@dp.callback_query_handler(lambda c: c.data == 'back1')
async def menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Welcome, " + callback_query.from_user.first_name +
                           '\nChoose the option', reply_markup=kb.menu_kb)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
