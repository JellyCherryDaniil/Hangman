from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from game_manager import GameManager
from hangman_game import HangmanGame

game_manager = GameManager()


def get_game_and_status(game_id):
    """
    Возвращает объект игры и статус
    :param game_id:
    :return:
    """
    game: HangmanGame = game_manager.get_game(game_id)
    game_status = game.status if game is not None else None
    return game, game_status


def get_game_status(game_id):
    """
    Возвращает статус игры
    :param game_id:
    :return:
    """

    _, game_status = get_game_and_status(game_id)
    return game_status


def return_game_keyboard():
    """
    Возвращает возможность использование кнопок
    :return:
    """
    button_start = [
        [KeyboardButton(text="Стоп")],
        [KeyboardButton(text="Перезапуск")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=button_start)
    return keyboard


async def start_game(message: Message):
    global game_manager
    game = game_manager.create_game(message.from_user.id)
    await message.answer("Игра начинается \n"
                     f"Тема игры: {game.theme}\n"
                     f"Отгадайте слово: {game.word}")
    await message.answer("Введите букву или слово целиком:", reply_markup=return_game_keyboard())


async def stop_game(message: Message):
    global game_manager
    game = game_manager.get_game(message.from_user.id)
    if game is not None:
        game.game_over()
        await message.answer("Игра закончена")
    else:
        await message.answer("Игра не запущена")