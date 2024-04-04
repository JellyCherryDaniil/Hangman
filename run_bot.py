import asyncio
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from os import getenv

from aiogram import Bot, Dispatcher, Router, types


from game_manager import GameManager
import bot_commands, bot_messages

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")
bot: Bot = None
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# game_status = "запуск"
# game: HangmanGame = None


# https://docs.python.org/3/library/logging.html#formatter-objects
FORMAT_LOG = "%(asctime)s : %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    global bot
    bot = Bot(TOKEN)
    # And the run events dispatching
    dp.include_routers(bot_commands.router, bot_messages.router)
    await dp.start_polling(bot)


if __name__ == "__main__":

    # file_handler = logging.FileHandler("log.txt", 'a', 'utf-8')
    handler = TimedRotatingFileHandler(filename="log.txt", when='D', interval=1, backupCount=1, encoding='utf-8',
                                       delay=False)
    logging.basicConfig(level=logging.INFO, handlers=[handler],
                        format=FORMAT_LOG)
    print("Бот работает")
    asyncio.run(main())