import asyncio
import os
from importlib import resources
import logging
from itertools import chain
from typing import List

from aiogram import Bot, Dispatcher

from plugins import Plugin


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s")

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher()


def load_plugins(plugin_list: list = None) -> List[Plugin]:
    found_plugins = {}
    for plugin_name in resources.contents("plugins"):
        if plugin_name.startswith("_"):
            continue
        if plugin_list and plugin_name not in plugin_list:
            continue

        plugin_module = resources.import_module(f"plugins.{plugin_name}")
        for name, obj in plugin_module.__dict__.items():
            if isinstance(obj, type) and issubclass(obj, Plugin):
                if not found_plugins.get(plugin_name):
                    found_plugins[plugin_name] = []
                found_plugins[plugin_name].append(obj())
                logging.info(f'Loaded {obj.__name__}')

    if plugin_list:
        not_found_plugins = plugin_list - found_plugins.keys()
        if not_found_plugins:
            logging.warning('Plugins not found: ' + ' '.join(not_found_plugins))

    result = []
    if plugin_list:
        for plugin_name in plugin_list:
            result += found_plugins.get(plugin_name, [])
    else:
        result = chain(*found_plugins.values())
    return result


async def main():
    await dp.start_polling(bot, drop_pending_updates=True, handle_signals=False)


if __name__ == "__main__":
    config_plugins = os.environ.get('BOT_PLUGINS')
    config_plugins = config_plugins.split(',') if config_plugins else None
    plugins = load_plugins(config_plugins)
    for plugin in plugins:
        plugin.init(dp)
        logging.info(f'Initialized {plugin.__class__.__name__}')

    loop = asyncio.get_event_loop()
    loop.create_task(main())

    loop.run_forever()





