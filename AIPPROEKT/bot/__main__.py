import asyncio
import logging

import bot.routers.error
import bot.routers.user.start

from . import routers, state
from .core import bot, dispatcher
from .phrases import phrases
from .utils.paths import ROOT_PATH


def setup_middleware():
    """Функция для инициализации middleware aiogram3"""

    dispatcher.message.middleware.register(state.state_data_middleware)
    dispatcher.callback_query.middleware.register(state.state_data_middleware)


@dispatcher.startup()
async def on_startup():
    """Хук события запуска бота"""

    me = await bot.get_me()
    print(phrases.bot_started.format(me=me))


async def main():
    """Входная точка программы"""

    log_filename = str((ROOT_PATH / "logs.log").resolve())

    logging.basicConfig(
        filename=log_filename,
        level=logging.ERROR,
        format=r"%(asctime)s %(levelname)s %(message)s",
    )

    setup_middleware()

    dispatcher.include_router(routers.root_router)

    used_update_types = dispatcher.resolve_used_update_types()
    await dispatcher.start_polling(bot, allowed_updates=used_update_types)


asyncio.run(main())
