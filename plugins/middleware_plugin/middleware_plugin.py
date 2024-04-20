import logging

from aiogram import Dispatcher, types, BaseMiddleware

from .. import Plugin


class ReactMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        logging.info(f'Middleware {__name__} triggered')
        await event.message.react(reaction=[types.ReactionTypeEmoji(emoji='🔥')])
        return await handler(event, data)


class MiddlewarePlugin(Plugin):
    @staticmethod
    def init(dp: Dispatcher):
        dp.update.outer_middleware(ReactMiddleware())
