from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

#тестовые кнопки
button_upd = KeyboardButton('/upd')
button_help = KeyboardButton('/help')

##добавить статистику за день

main_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder="Введи команду")
main_kb.add(button_upd, button_help)