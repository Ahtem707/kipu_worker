"""
Файл с хэндлерам Актуальные вакансии
"""
import asyncio
import calendar
import re
from datetime import date, timedelta
from typing import Union
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from database.database import *
from database.state import FSMCareer
from handlers.echo import delete_message
from keyboards import key_text
from keyboards.keyboards import detailed_keyboard, current_keyboard, response_keyboard, task_keyboard, technical_support_keyboard, webAppKeyboardInline
from loader import bot, logger
from settings import constants
from settings.constants import PRACTICES_TEMPLATE, PRACTICE_TEMPLATE


async def current_vacancies(message: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
    """
    Хендлер - обрабатывает кнопки вакансии
    :param message: Union[types.Message, types.CallbackQuery]
    :param state: FSMContext
    :return None
    """
    try:
        async with state.proxy() as data:
            if isinstance(message, types.CallbackQuery):
                await delete_message(message.from_user.id)
            else:
                await delete_message(message.from_user.id)
                await message.delete()
                message_text = message.text
                data['command'] = message_text
            await FSMCareer.menu.set()
            if data['command'] == key_text.CURRENT_VACANCIES:
                bot_message = await bot.send_message(message.from_user.id, constants.CURRENT_VACANCIES,
                                                     reply_markup=current_keyboard(key_text.LIST_CURRENT_VACANCIES))
                DeleteMessage(
                    chat_id=message.from_user.id, message_id=f'{bot_message.message_id}'
                ).save()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def projects_handler(message: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает команду tasks, входит в машину состояния FSMTask
    :param message: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    try:
        async with state.proxy() as data:
            if isinstance(message, types.CallbackQuery):
                await delete_message(message.from_user.id)
                await bot.edit_message_reply_markup(message.from_user.id, message.message.message_id)
            else:
                await delete_message(message.from_user.id)
                await message.delete()
                message_text = message.text
                data['command'] = message_text
            if data['command'] == key_text.PROJECTS:
                count = Projects.select().count()
                for task in Projects.select().paginate(1, 1):
                    await delete_message(message.from_user.id)
                    bot_message = await bot.send_message(message.from_user.id, constants.TEMPLATE.format(task.title, task.author,
                                                         task.team), reply_markup=await task_keyboard(task.id, task.link,
                                                         'detailed', str(1), count))
                    DeleteMessage(chat_id=message.from_user.id, message_id=bot_message.message_id).save()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def vacancies_practice(call: types.CallbackQuery, state: FSMContext) -> None:
    """
        Хендлер - обрабатывает клавиатуру практики
        :param call: CallbackQuery
        :param state: FSMContext
        :return None
        """
    try:
        async with state.proxy() as data:
            await delete_message(call.from_user.id)
            if data['command'] == key_text.CURRENT_VACANCIES:
                vacancies = Vacancy.select().where(Vacancy.type_vacancy == 'Практика', Vacancy.active == True)
                text = constants.NO_VACANCIES
            if len(vacancies) > 0:
                for vacancy in vacancies:
                    bot_message = await bot.send_message(call.from_user.id, vacancy.title,
                                                         reply_markup=detailed_keyboard(vacancy.id, data['command']))
                    DeleteMessage(chat_id=call.from_user.id, message_id=bot_message.message_id).save()

            else:
                await bot.send_message(call.from_user.id, text)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def vacancies_internship(call: types.CallbackQuery, state: FSMContext) -> None:
    """
        Хендлер - обрабатывает клавиатуру стажировка
        :param call: CallbackQuery
        :param state: FSMContext
        :return None
        """
    try:
        async with state.proxy() as data:
            await delete_message(call.from_user.id)
            if data['command'] == key_text.CURRENT_VACANCIES:
                vacancies = Vacancy.select().where(Vacancy.type_vacancy == 'Стажировка', Vacancy.active == True)
                text = constants.NO_VACANCIES
            if len(vacancies) > 0:
                for vacancy in vacancies:
                    bot_message = await bot.send_message(call.from_user.id, vacancy.title,
                                                         reply_markup=detailed_keyboard(vacancy.id,
                                                                                        data['command']))
                    DeleteMessage(chat_id=call.from_user.id, message_id=bot_message.message_id).save()

            else:
                await bot.send_message(call.from_user.id, text)

    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def vacancies_work(call: types.CallbackQuery, state: FSMContext) -> None:
    """
        Хендлер - обрабатывает клавиатуру стажировка
        :param call: CallbackQuery
        :param state: FSMContext
        :return None
        """
    try:
        async with state.proxy() as data:
            await delete_message(call.from_user.id)
            if data['command'] == key_text.CURRENT_VACANCIES:
                vacancies = Vacancy.select().where(Vacancy.type_vacancy == 'Работа', Vacancy.active == True)
                text = constants.NO_VACANCIES
            if len(vacancies) > 0:
                for vacancy in vacancies:
                    bot_message = await bot.send_message(call.from_user.id, vacancy.title,
                                                         reply_markup=detailed_keyboard(vacancy.id,
                                                                                        data['command']))
                    DeleteMessage(chat_id=call.from_user.id, message_id=bot_message.message_id).save()

            else:
                await bot.send_message(call.from_user.id, text)

    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def tasks_paginate_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обрабатывает пагинацию
    :param call: CallbackQuery
    :return: None
    """
    try:
        num_page = int(call.data.split('&')[1])
        count = Projects.select().count()
        tasks = Projects.select().paginate(num_page, 1)
        for task in tasks:
            await delete_message(call.from_user.id)
            bot_message = await bot.send_message(call.from_user.id, constants.TEMPLATE.format(task.title, task.author,
                                                 task.team),
                                                 reply_markup=await task_keyboard(task.id, task.link, 'detailed', str(num_page), count))
            DeleteMessage(chat_id=call.from_user.id, message_id=bot_message.message_id).save()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def task_detailed_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - обрабатывает команду detailed
    :param call: CallbackQuery
    :return: None
    """
    try:
        i, task_id, num_page = call.data.split('&')
        count = Projects.select().count()
        task = Projects.get(Projects.id == int(task_id))
        await delete_message(call.from_user.id)
        bot_message = await bot.send_message(call.from_user.id, constants.DETAILED.format(task.title,
                                             task.type_projects, task.status, task.author, task.team,
                                             task.description),
                                             reply_markup=await task_keyboard(task.id, task.link, 'task', str(num_page), count)
                                             )
        DeleteMessage(chat_id=call.from_user.id, message_id=bot_message.message_id).save()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def technical_support(message: types.Message, state: FSMContext) -> None:
    """
       Хендлер - выводит  меню рассылок.
       :param message: CallbackQuery
       :param state: FSMContext
       :return None
    """
    try:
        await delete_message(message.from_user.id)
        bot_message = await bot.send_message(
            message.from_user.id, constants.SUPPORT, reply_markup=await technical_support_keyboard()
        )
        DeleteMessage(chat_id=message.from_user.id, message_id=str(bot_message.message_id)).save()
        await message.delete()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def profile_support(message: types.Message, state: FSMContext) -> None:
    """
       Хендлер - выводит  профиль.
       :param message: CallbackQuery
       :param state: FSMContext
       :return None
    """
    try:
        await delete_message(message.from_user.id)
        bot_message = await bot.send_message(
            message.from_user.id, constants.PROFILE, reply_markup=await webAppKeyboardInline()
        )
        DeleteMessage(chat_id=message.from_user.id, message_id=str(bot_message.message_id)).save()
        await message.delete()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def show_vacancies(call: types.CallbackQuery, state: FSMContext, form=None) -> bool:
    """
        Функция - Логика показа объявлений.
        :param call: CallbackQuery
        :param state: FSMContext
        :param form: None
        :return bool
    """
    try:
        flag = False
        async with state.proxy() as data:
            specialization_list = [int(elemnt) for elemnt in data['specialization'].split(',') if elemnt.isdigit()]
            course_list = [int(elem) for elem in data['course'].split('&')]
            if data['command'] == key_text.CURRENT_VACANCIES:
                if form:
                    i_form = form
                else:
                    i_form = data['form']
                sda = ListVacancies.select().where(ListVacancies.level == int(data['education']),
                                                   ListVacancies.course.in_(course_list),
                                                   ListVacancies.specialization.in_(specialization_list))
                if len(sda) > 0:
                    flag = False
                    for elem in sda:
                        if str(elem.vacancies.form_of_employment.id) == i_form:
                            print('условие верное')
                            flag = True
                            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                        text=elem.vacancies.title,
                                                        reply_markup=detailed_keyboard(elem.vacancies.id, data['command']))
            else:
                if data.get('form', None):
                    i_form = data['form']
                else:
                    i_form = call.data
                asd = ListPractices.select().where(ListPractices.level == int(data['education']),
                                                   ListPractices.course.in_(course_list),
                                                   ListPractices.specialization.in_(specialization_list))
                if len(asd) > 0:
                    flag = False
                    for elem in asd:
                        if str(elem.practices.practice_period) == i_form:
                            print('условие верное')
                            flag = True
                            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                        text=elem.practices.title,
                                                        reply_markup=detailed_keyboard(elem.practices.id, data['command']))
        return flag
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def detailed_vacancies(call: types.CallbackQuery) -> None:
    """
           Хендлер - Выводит подробное сообщение о практики.
           :param call: CallbackQuery
           :return None
       """
    try:
        key, ads_id = call.data.split('&')
        if key == key_text.DETAILED:
            ads = Vacancy.get_or_none(Vacancy.id == int(ads_id))
            text = PRACTICE_TEMPLATE.format(ads.title, ads.type_vacancy,ads.busyness, ads.schedule, ads.address, ads.description)
            if ads:
                text = text.replace('<p>', '')
                text = text.replace('</p>', '')
                text = text.replace('<br>', '')
                text = text.replace('<br />', '')
                text = text.replace('&nbsp;', ' ')
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=text, reply_markup=response_keyboard(),
                                            parse_mode='HTML', disable_web_page_preview=True)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def register_user(message) -> None:
    """
    Хэндлер - обрабатывает команду /start
    :param message: Message
    :return: None
    """
    try:
        print(message.web_app_data)
        await bot.send_message(message.chat.id, f"получили инофрмацию из веб-приложения: {message.web_app_data.data}")
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_current_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(detailed_vacancies, lambda call: call.data.split('&')[0] in [key_text.DETAILED, key_text.DETAILED_PRAC], state='*')
    dp.register_message_handler(current_vacancies, Text(equals=key_text.CURRENT_VACANCIES), state=None)
    dp.register_callback_query_handler(current_vacancies, Text(equals=key_text.BACK_MENU), state='*')
    dp.register_callback_query_handler(vacancies_practice,  Text(equals=key_text.LIST_CURRENT_VACANCIES[0][1]), state=FSMCareer.menu)
    dp.register_callback_query_handler(vacancies_internship,  Text(equals=key_text.LIST_CURRENT_VACANCIES[1][1]), state=FSMCareer.menu)
    dp.register_callback_query_handler(vacancies_work, Text(equals=key_text.LIST_CURRENT_VACANCIES[2][1]), state=FSMCareer.menu)
    # dp.register_callback_query_handler(technical_support, Text(equals=key_text.LIST_CURRENT_VACANCIES[3][1]), state=FSMCareer.menu)
    dp.register_message_handler(projects_handler, Text(equals=key_text.PROJECTS), state='*')
    dp.register_callback_query_handler(tasks_paginate_handler, Text(startswith='pagination'), state='*')
    dp.register_callback_query_handler(task_detailed_handler, Text(startswith='detailed'), state='*')
    # dp.register_callback_query_handler(technical_support, state=FSMCareer.menu)
    dp.register_message_handler(register_user, content_types=['web_app_data'], state=None)



