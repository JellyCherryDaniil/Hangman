from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile

from bot_gamemanagement import start_game, stop_game
from hangman_game import STATUS_VICTORY, STATUS_DEFEAT

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    button_start = [
        [KeyboardButton(text="Запуск игры")],
        [KeyboardButton(text="Справка")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=button_start)
    await message.answer("Главное меню", reply_markup=keyboard)


@router.message(Command("start_game"))
async def command_start_game_handler(message: Message) -> None:
    """
    Команда запуска игры
    :param message: Сообщение из телеграмма
    :return:
    """
    await start_game(message)
    

@router.message(Command("stop_game"))
async def command_stop_game_handler(message: Message) -> None:
    """
    Команда остановки игры
    :param message: Сообщение из телеграмма
    :return:
    """
    await stop_game(message)