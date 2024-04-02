import asyncio
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputFile
from aiogram.utils.markdown import hbold

from game_manager import GameManager
from hangman_game import HangmanGame, STATUS_VICTORY,STATUS_INPROGRESS,STATUS_DEFEAT,STATUS_PREPARE

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")
bot: Bot = None
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# game_status = "запуск"
# game: HangmanGame = None

game_manager = GameManager()
# https://docs.python.org/3/library/logging.html#formatter-objects
FORMAT_LOG = "%(asctime)s : %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"


def play_hangman(message, game, is_symbol) -> bool:
    """

    Шаг игры Hangman
    :param symbol: Загаданное слово или буква
    :param game: объект типа HangmanGame
    :param is_symbol: является ли введёное буквой
    :return: возвращает результат игры
    """
    message_text = message.text.lower()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    button_start = [
        [types.KeyboardButton(text="Запуск игры")],
        [types.KeyboardButton(text="Справка")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button_start)

    await message.answer("Главное меню", reply_markup=keyboard)

    # await message.answer(f"Hello, {message.from_user.full_name}!")


def return_keyboard():
    """
    Возвращает возможность использование кнопок
    :return:
    """
    button_start = [
        [types.KeyboardButton(text="Стоп")],
        [types.KeyboardButton(text="Перезапуск")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button_start)
    return keyboard


@dp.message(Command("start_game"))
async def command_start_game_handler(message: Message) -> None:
    """
    Команда запуска игры
    :param message: Сообщение из телеграмма
    :return:
    """
    global game_manager
    game = game_manager.create_game(message.from_user.id)
    await message.answer("Игра начинается \n"
                        f"Тема игры: {game.theme}\n"
                        f"Отгадайте слово: {game.word}")
    await message.answer("Введите букву или слово целиком:", reply_markup=return_keyboard())


async def process_game(message: Message, game) -> None:
    message_text = message.text.lower()

    game_over = False
    correct_input = False
    is_symbol = True
    if len(message_text) == 1 and message_text.isalpha():
        correct_input = True
    elif len(message_text) > 1 and message_text.isalpha():
        correct_input = True
        is_symbol = False
    if not correct_input:
        await message.answer("Введите, пожалуйста, букву или целое слово!")
        return

    if is_symbol:
        guess_function = game.guess
    else:
        guess_function = game.guess_word

    if guess_function(message_text):
        await message.answer(game.word)
    else:
        await message.answer("Вы не угадали\n"
              f"Слово:{game.word}\n")
        photo = types.FSInputFile(game.return_hangman_image())
        await bot.send_photo(chat_id=message.chat.id, photo=photo)

    if game.status == STATUS_VICTORY:
        await message.answer("Вы выиграли")
        game_over = True
    elif game.status == STATUS_DEFEAT:
        await message.answer("Вы проиграли")
        game_over = True

    if game_over:
        await message.answer("Хотите продолжить? (Введите да, чтобы продолжить)")


@dp.message(Command("stop_game"))
async def command_stop_game_handler(message: Message) -> None:
    """
    Команда остановки игры
    :param message: Сообщение из телеграмма
    :return:
    """
    global game_manager
    game = game_manager.get_game(message.from_user.id)
    if game is not None:
        game.game_over()
        await message.answer("Игра закончена")
    else:
        await message.answer("Игра не запущена")



@dp.message()
async def text_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    global game_manager
    game:HangmanGame = game_manager.get_game(message.from_user.id)
    game_status = game.status if game is not None else None


    try:
        # Send a copy of the received message
        # await message.send_copy(chat_id=message.chat.id)

        if game_status == STATUS_INPROGRESS and message.text == "Стоп":
            await command_stop_game_handler(message)
        elif game_status == STATUS_INPROGRESS and message.text == "Перезапуск":
            await command_start_game_handler(message)
        elif game_status == STATUS_INPROGRESS:
            await process_game(message, game)
        elif any(game_status == st for st in (STATUS_VICTORY, STATUS_DEFEAT)):
            continuation = message.text.lower()
            if continuation == "да":
                await command_start_game_handler(message)
        elif message.text == "Запуск игры":
            await command_start_game_handler(message)
        else:
            logging.info(f"Пользователь ввел неправильную команду: {message.text}")
            await message.answer(f"Я ничего не понимаю!")
    except Exception as exception:
        logging.error(f"Произошла ошибка текстового ввода :{exception}")
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Произошла ошибка!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    global bot
    bot = Bot(TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":

    # file_handler = logging.FileHandler("log.txt", 'a', 'utf-8')
    handler = TimedRotatingFileHandler(filename="log.txt", when='D', interval=1, backupCount=1, encoding='utf-8',
                                       delay=False)
    logging.basicConfig(level=logging.INFO, handlers=[handler],
                        format=FORMAT_LOG)
    print("Бот работает")
    asyncio.run(main())