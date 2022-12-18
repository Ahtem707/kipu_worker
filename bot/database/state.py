"""
Файл с моделями машины состояний
"""
from telegram_bot_calendar.detailed import DetailedTelegramCalendar
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMCareer(StatesGroup):
    menu = State()
    link = State()
    education = State()
    course = State()
    specialization = State()
    form = State()
    interval = State()
    first_day = State()


class CustomCalendar(DetailedTelegramCalendar):
    empty_year_button = ''
    empty_month_button = ''



