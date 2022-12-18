from aiogram import Dispatcher, types
from database.database import DeleteMessage
from loader import logger, bot
from settings import constants


async def echo_handler(message: types.Message) -> None:
    """
    Хэндлер - оповещает бота о некорректной команде (Эхо)
    :param message: Message
    :return: None
    """
    try:
        await bot.send_message(message.from_user.id, constants.INCORRECT_INPUT)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def delete_message(user_id: int) -> None:
    """
    Функция - обрабатывает удаление сообщений
    :param user_id: int
    :return: None
    """
    try:
        message = DeleteMessage.select().where(DeleteMessage.chat_id == user_id)
        if len(message):
            for mess in message:
                if '&' in mess.message_id:
                    mes_ids = mess.message_id.split('&')
                    for elem in mes_ids:
                        try:
                            await bot.delete_message(chat_id=mess.chat_id, message_id=int(elem))
                        except Exception:
                            pass
                else:
                    try:
                        await bot.delete_message(chat_id=mess.chat_id, message_id=int(mess.message_id))
                    except Exception:
                        pass
                try:
                    mess.delete_instance()
                except Exception:
                    pass
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_echo_handlers(dp: Dispatcher) -> None:
    """
    Функция - регистрирует все хэндлеры файла echo.py
    :param dp: Dispatcher
    :return: None
    """
    dp.register_message_handler(echo_handler)