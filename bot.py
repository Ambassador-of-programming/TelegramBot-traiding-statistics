from time import sleep
import telebot
import asyncio
from config.telegram_token import TOKEN
from db.db_class import General_db


bot = telebot.TeleBot(TOKEN, parse_mode=None)
name_channel = '@trading_statistics'  # здесь указывается группа

while True:
	try:
		async def message():
			bot.send_message(name_channel, f'''
				📊Статистика торговли\n
				🗝Ордер ID: {General_db.db_order_id()}\n
				🥇Название монеты: {General_db.db_coin()}\n
				🔔Индикатор открытия: {General_db.db_open()}\n
				🔕Индикатор закрытия: {General_db.db_closes()}\n
				💰Процент прибыли: {General_db.db_profit()}%\n
				🕗Время трейдинга: {General_db.db_times()}\n
				🌪Стратегия трейдинга: {General_db.db_strategy()}\n''')

			General_db.Candlestick()   # рисует графику и сохраняет в папке image
			bot.send_photo(name_channel, photo=open(f'image/{General_db.search_id()}.png', 'rb'))
			General_db.db_remove_photo()    # удаляет сохранную графику из папки image
			General_db.delete_id()    # функция для вызова удаления id
		asyncio.run(message())
	except: 
		sleep(30)
		continue