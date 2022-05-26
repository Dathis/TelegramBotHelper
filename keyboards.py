from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


menu = InlineKeyboardMarkup()
menu.add(InlineKeyboardButton('Weather ☁', callback_data='weather'))
menu.add(InlineKeyboardButton('Music🎵',callback_data='music'))
menu.add(InlineKeyboardButton('News NYT📰',callback_data='news'))
menu.add(InlineKeyboardButton('Books📖',callback_data='books'))
menu.add(InlineKeyboardButton('Crypto prices₿', callback_data='crypto'))


news = InlineKeyboardMarkup()
news.add(InlineKeyboardButton('Political news',callback_data='politic'))
news.add(InlineKeyboardButton('Economic news',callback_data='economy'))
news.add(InlineKeyboardButton('Scientific news',callback_data='science'))


books = InlineKeyboardMarkup(row_width=1)
books.add(InlineKeyboardButton('Art literature', callback_data='art_l'))
books.add(InlineKeyboardButton('Scientific and popular science literature', callback_data='science_l'))
books.add(InlineKeyboardButton('Literature in Psychology and Self-Development', callback_data='self_l'))

back = InlineKeyboardMarkup()
back.add(InlineKeyboardButton('<<Back', callback_data='back'))



