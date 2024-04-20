import logging

from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command

from .. import Plugin


async def echo_handler(message: types.Message, bot: Bot):
    logging.info(f'Plugin {__name__} received message')
    try:
        await message.answer('Answer from echo_plugin: ' + message.text)
    except TelegramBadRequest as e:
        logging.error(f'Failed to send a message to chat_id {message.chat.id}. {e}')


class EchoPlugin(Plugin):
    @staticmethod
    def init(dp: Dispatcher):
        dp.message()(echo_handler)
