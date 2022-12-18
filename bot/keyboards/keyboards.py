from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from keyboards import key_text
from keyboards.key_text import BACK, BACK_SPES, BACK_MENU, \
    LIST_CANCEL, LIST_PRICTICES_DATE, LIST_AUTOMATIC_DISTRIBUTION, BACK_LINK, BACK_FORM_TERM, \
    LIST_MAILING, CALENDAR_CAREER_EVENTS, RESPONSE
from database.database import *
from aiogram.types.web_app_info import WebAppInfo


def anonymous_user_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавиатура для незарегистрированного пользователя
    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    first_key = KeyboardButton(text=key_text.CURRENT_VACANCIES)
    second_key = KeyboardButton(text=key_text.PROJECTS)
    third_key = KeyboardButton(text=key_text.PROFILE)
    fourth_key = KeyboardButton(text=key_text.TECHNICAL_SUPPORT, url='https://t.me/bbizon')
    # fifth_key = KeyboardButton(text=key_text.INFORMATIONAL_PORTAL)
    keyboard.add(first_key, second_key, third_key, fourth_key)
    return keyboard


def current_keyboard(current_list: List) -> InlineKeyboardMarkup:
    """
        Клавиатура  меню практики/вакансии
        :param: current_list: List
        :return: InlineKeyboardMarkup
        """
    keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    for elem in current_list:
        keyboard.add(InlineKeyboardButton(text=elem[0], callback_data=elem[1]))
    return keyboard.add(InlineKeyboardButton(text=key_text.menu, callback_data=key_text.menu))


async def technical_support_keyboard() -> InlineKeyboardMarkup:
    """
        Клавиатура  меню практики/вакансии
        :param: current_list: List
        :return: InlineKeyboardMarkup
        """
    keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    return keyboard.add(InlineKeyboardButton(text=key_text.support, url='https://t.me/bbizon'),
           InlineKeyboardButton(text=key_text.menu, callback_data=key_text.menu)
    )


def detailed_keyboard(ads_id: int, command: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для детального просмотра практики
    :param ads_id: int
    :param command: str
    :return: InlineKyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    text = key_text.DETAILED
    return keyboard.add(
        InlineKeyboardButton(text=key_text.DETAILED, callback_data=text + '&' + str(ads_id)),
    )


def response_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1, response_keyboar=True)
    return keyboard.add(InlineKeyboardButton(text=RESPONSE, url='mailto:mail@e.mail.ru/compose?to=job@rgsu.net&subject=Отклик%20на%20вакансию'))


async def task_keyboard(project_id: str, link: str, variable: str, num_page: str, end: int, start=1) -> InlineKeyboardMarkup:
    """
    Функция - создаёт Inline клавиатуру выполнения задания.
    :return: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=3)
    if variable == 'detailed':
        keyboard.add(InlineKeyboardButton(text=key_text.detailed, callback_data=f'detailed&{project_id}&{num_page}'))
    else:
        keyboard.add(InlineKeyboardButton(text=key_text.to_project, url=link))
    if start == end:
        return keyboard.add(InlineKeyboardButton(text=key_text.menu, callback_data=key_text.menu))
    else:
        if int(num_page) == start:
            left = str(end)
            right = str(int(num_page) + 1)
        elif int(num_page) == end:
            left = str(int(num_page) - 1)
            right = str(start)
        else:
            left = str(int(num_page) - 1)
            right = str(int(num_page) + 1)
    return keyboard.add(
            InlineKeyboardButton(text='«', callback_data=f'pagination&' + left),
            InlineKeyboardButton(text=f'{num_page}/{end}', callback_data='pass'),
            InlineKeyboardButton(text='»', callback_data=f'pagination&' + right),
            InlineKeyboardButton(text=key_text.menu, callback_data=key_text.menu),
        )


async def webAppKeyboardInline(): #создание inline-клавиатуры с webapp кнопкой
   keyboard = InlineKeyboardMarkup(row_width=1)
   webApp = WebAppInfo(url="https://www.ahtem.ru:3005/reg/") #создаем webappinfo - формат хранения url
   one = InlineKeyboardButton(text="Обо мне", web_app=webApp) #создаем кнопку типа webapp
   webApp_1 = WebAppInfo(url="https://www.ahtem.ru:3005/settings/")  # создаем webappinfo - формат хранения url
   too = InlineKeyboardButton(text="Настройки уведомлений", web_app=webApp_1)  # создаем кнопку типа webapp
   keyboard.add(one, too) #добавляем кнопку в клавиатуру

   return keyboard.add(InlineKeyboardButton(text=key_text.menu, callback_data=key_text.menu))