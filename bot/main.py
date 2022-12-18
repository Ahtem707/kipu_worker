"""Файл для запуска бота. Содержит в себе все регистраторы приложения"""
import asyncio

from aiogram import types, Dispatcher
from loader import dp
from aiogram.utils import executor
from handlers import start, echo, current_vacancies, info_portal


async def set_default_commands(dp: Dispatcher):
    print("myLog: 1")
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Старт"),
        ]
    )


start.register_start_handlers(dp)
current_vacancies.register_current_handlers(dp)
info_portal.register_current_handlers(dp)
echo.register_echo_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_default_commands, skip_updates=True)