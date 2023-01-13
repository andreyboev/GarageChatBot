import asyncio

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand

import config
from handlers import common


async def main():
    dp = Dispatcher()
    bot = Bot(config.TOKEN)
    await bot.set_my_commands([BotCommand(command='help', description='Help'),
                               BotCommand(command='menu', description='Menu')])
    dp.include_router(common.router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
