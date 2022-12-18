"""
Файл с хэндлерами старт/хэлп и регистрация
"""
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers import current_vacancies, info_portal
from keyboards import key_text
from keyboards.keyboards import anonymous_user_keyboard
from loader import bot, logger
from settings import constants
from database.database import *
from handlers.echo import delete_message


async def start_command(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду /start
    :param message: Message
    :return: None
    """
    try:
        with db:
            await delete_message(message.from_user.id)
            if isinstance(message, types.Message):
                await message.delete()
            bot_message = await bot.send_message(message.from_user.id, constants.START_COMMAND,
                                                 reply_markup=anonymous_user_keyboard())
            DeleteMessage(
                chat_id=message.from_user.id, message_id=f'{bot_message.message_id}'
            ).save()

    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def cancel_state(message: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
    """
        Хэндлер - закрывает состояния и переходит по сценарию
        :param message: Message
        :param state: FSMContext
        :return: None
        """
    try:
        if isinstance(message, types.Message):
            if await state.get_state():
                await state.finish()
            if message.text == '/start':
                await start_command(message)
            elif message.text == key_text.CURRENT_VACANCIES:
                await current_vacancies.current_vacancies(message, state)
            elif message.text == key_text.PROJECTS:
                await current_vacancies.projects_handler(message, state)
            elif message.text == key_text.PROFILE:
                await current_vacancies.profile_support(message, state)
            elif message.text == key_text.TECHNICAL_SUPPORT:
                await current_vacancies.technical_support(message, state)
            elif message.text == key_text.PROFILE:
                await info_portal.info_portal(message, state)
        else:
            if message.data == key_text.LIST_CURRENT_VACANCIES[0][1]:
                await current_vacancies.vacancies_practice(message, state)
            elif message.data == key_text.LIST_CURRENT_VACANCIES[1][1]:
                await current_vacancies.vacancies_internship(message, state)
            elif message.data == key_text.LIST_CURRENT_VACANCIES[2][1]:
                await current_vacancies.vacancies_work(message, state)
            # elif message.data == key_text.LIST_CURRENT_VACANCIES[3][1]:
            #     await current_vacancies.automatic_distribution(message, state)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)





def register_start_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_command, commands=['start'], state=None)
    dp.register_message_handler(cancel_state, lambda message: message.text in [
        '/start', '/help', key_text.CURRENT_VACANCIES, key_text.PROJECTS, key_text.PROFILE,
        key_text.TECHNICAL_SUPPORT,
    ], state='*')
    dp.register_callback_query_handler(cancel_state, lambda message: message.data in [
        elem[1] for elem in key_text.LIST_CURRENT_VACANCIES], state='*')
    dp.register_callback_query_handler(start_command, Text(equals=key_text.menu), state='*')
