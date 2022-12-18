from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from database.database import DeleteMessage
from handlers.echo import delete_message
from keyboards import key_text
from loader import bot, logger
from settings import constants


async def info_portal(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер - обрабатывает кнопку оценка компетенций
    :param message: Union[types.Message, types.CallbackQuery]
    :param state: FSMContext
    :return None
    """
    try:
        async with state.proxy() as data:
            await delete_message(message.from_user.id)
            bot_message = await bot.send_message(
                message.from_user.id, constants.SUPPORT, reply_markup=await technical_support_keyboard()
            )
            DeleteMessage(chat_id=message.from_user.id, message_id=str(bot_message.message_id)).save()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_current_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(info_portal, lambda message: message.text == key_text.INFORMATIONAL_PORTAL,
                                state=None)