from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup

weather_btn = InlineKeyboardButton('Weather ☁', callback_data='weather')
music_btn = InlineKeyboardButton('Music🎵',callback_data='music')
news_btn = InlineKeyboardButton('News NYT📰',callback_data='news')
books_btn = InlineKeyboardButton('Books📖',callback_data='books')
memes_btn = InlineKeyboardButton('Memes😄',callback_data='memes')

menu_kb = InlineKeyboardMarkup().add(weather_btn, music_btn, news_btn, books_btn, memes_btn)

political_btn = InlineKeyboardButton('Political news',callback_data='politic')
economy_btn = InlineKeyboardButton('Economic news',callback_data='economy')
science_btn = InlineKeyboardButton('Scientific news',callback_data='science')

news_kb = InlineKeyboardMarkup().add(political_btn,economy_btn,science_btn)

art_btn = InlineKeyboardButton('Art literature', callback_data='art_l')
science_l_btn = InlineKeyboardButton('Scientific and popular science literature', callback_data='science_l')
self_development_btn = InlineKeyboardButton('Literature in Psychology and Self-Development', callback_data='self_l')
books_kb = InlineKeyboardMarkup(row_width=1).add(art_btn,science_l_btn,self_development_btn)

back1_btn = InlineKeyboardButton('<<Back',callback_data='back1')

back1_kb = InlineKeyboardMarkup().add(back1_btn)

