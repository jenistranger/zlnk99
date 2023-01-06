import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import aioschedule
import time
import asyncio
from cfg import maintoken
from keyboard import main_kb
from parser import ParserLolzChrome
from parser import getInfo
import random

#логирование в консоли (можно удалить)
logging.basicConfig(level=logging.INFO)

#инициализация бота и диспа(е)тчера
bot = Bot(token=maintoken)
dp = Dispatcher(bot)

#headless - true (окно браузера не будет открываться)
#создание асинх функции парсинга
async def mainjob():
    mainPareser = ParserLolzChrome(state=False)
    print(mainPareser.getAllPages())

#асинх ф-ция шедла
async def schedulDo():
    #раз в 10 минут
    aioschedule.every(600).seconds.do(mainjob)
    #aioschedule.every().minute.do(doParsing)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

#метод бота, при запуске бота выполняется ф-ця шедла
async def on_startup(_):
    asyncio.create_task(schedulDo())

#команды start и help
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(f'Привет, {message.from_user.username}!\nБот был запущен', reply_markup=main_kb)

@dp.message_handler(commands=['help'])
async def sendBotParser(message: types.Message):
    await message.answer(f"Твой username: {message.from_user.username}\nТвой user id: {message.from_user.id}")

#вызов статистики
@dp.message_handler(commands=['upd'])
async def sendBotParser(message: types.Message):
    await message.answer(getInfo())

#запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)