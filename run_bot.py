import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from hangman_game import HangmanGame

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
game_status = "запуск"
game = None



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
    await message.answer(f"Hello, {message.from_user.full_name}!")


@dp.message(Command("start_game"))
async def command_start_handler(message: Message) -> None:
    """
    Команда запуска игры
    :param message: Сообщение из телеграмма
    :return:
    """
    global game_status, game

    game_status = "начало"
    game = HangmanGame()
    game.start()
    await message.answer("Игра начинается \n"
                        f"Тема игры: {game.theme}\n"
                        f"Отгадайте слово: {game.word}")
    await message.answer("Введите букву или слово целиком:")


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
        await message.answer(game.show_hangman())

    if game.status == "ПОБЕДА":
        await message.answer("Вы выиграли")
        game_over = True
    elif game.status == "проиграли":
        await message.answer("Вы проиграли")
        game_over = True

    if game_over:
        global game_status
        await message.answer("Хотите продолжить? (Введите да, чтобы продолжить)")
        game_status = "перезапуск"



@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    global game, game_status
    try:
        # Send a copy of the received message
        # await message.send_copy(chat_id=message.chat.id)
        if game_status == "начало":
            await process_game(message, game)
        elif game_status == "перезапуск":
            continuation = message.text.lower()
            if continuation == "да":
                await command_start_handler(message)
            else:
                game_status = "запуск"

        else:
            await message.answer(f"Я ничего не понимаю!")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Произошла ошибка!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())