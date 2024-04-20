import logging

from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command

from .. import Plugin


async def start_handler(message: types.Message, bot: Bot):
    logging.info(f'Plugin {__name__} received message')
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text='echo from start_plugin'
        )
    except TelegramBadRequest as e:
        logging.error(f'Failed to send a message to chat_id {message.chat.id}. {e}')


class StartPlugin(Plugin):
    @staticmethod
    def init(dp: Dispatcher):
        dp.message(Command("start"))(start_handler)
