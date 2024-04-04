import logging

from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile

from bot_gamemanagement import stop_game, get_game_status, start_game, get_game_and_status
from hangman_game import HangmanGame, STATUS_VICTORY, STATUS_DEFEAT, STATUS_INPROGRESS

router = Router()


async def process_game(message: Message,bot: Bot, game) -> None:
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
        photo = FSInputFile(game.return_hangman_image())

        await bot.send_photo(chat_id=message.chat.id, photo=photo)

    if game.status == STATUS_VICTORY:
        await message.answer("Вы выиграли")
        game_over = True
    elif game.status == STATUS_DEFEAT:
        await message.answer("Вы проиграли")
        game_over = True

    if game_over:
        await message.answer("Хотите продолжить? (Введите да, чтобы продолжить)")


# and_f(F.text.startswith("show"), F.text.endswith("example"))
# or_f(F.text(text="hi"), CommandStart())
# invert_f(IsAdmin())


@router.message(F.text.lower() == "запуск игры")
async def start_message_handler(message: Message):
    if message.text == "Запуск игры":
        await start_game(message)


@router.message(F.text.lower() == "стоп")
async def stop_message_handler(message: Message):
    if get_game_status(message.from_user.id) == STATUS_INPROGRESS:
        await stop_game(message)


@router.message(F.text.lower() == "перезапуск")
async def restart_message_handler(message: Message):
    if get_game_status(message.from_user.id) == STATUS_INPROGRESS:
        await start_game(message)


@router.message(F.text.lower() == "да")
async def continue_message_handler(message: Message):
    if any(get_game_status(message.from_user.id) == st for st in (STATUS_VICTORY, STATUS_DEFEAT)):
        continuation = message.text.lower()
        if continuation == "да":
            await start_game(message)


@router.message()
async def text_handler(message: Message, bot: Bot) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """

    game, game_status = get_game_and_status(message.from_user.id)


    try:
        # Send a copy of the received message
        # await message.send_copy(chat_id=message.chat.id)

        if game_status == STATUS_INPROGRESS:
            await process_game(message, bot, game)
        else:
            logging.info(f"Пользователь ввел неправильную команду: {message.text}")
            await message.answer(f"Я ничего не понимаю!")
    except Exception as exception:
        logging.error(f"Произошла ошибка текстового ввода :{exception}")
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Произошла ошибка!")

