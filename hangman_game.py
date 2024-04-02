from random import choice
from pathlib import PurePath
from file_processor import read_file, read_data

HANGMAN1_STR = read_file(PurePath("data") / "HANGMAN1.txt")
HANGMAN2_STR = read_file(PurePath("data") / "HANGMAN2.txt")
HANGMAN3_STR = read_file(PurePath("data") / "HANGMAN3.txt")
HANGMAN4_STR = read_file(PurePath("data") / "HANGMAN4.txt")
HANGMAN5_STR = read_file(PurePath("data") / "HANGMAN5.txt")
HANGMAN1_JPEG = PurePath("data") / "HANGMAN1.jpg"
HANGMAN2_JPEG = PurePath("data") / "HANGMAN2.jpg"
HANGMAN3_JPEG = PurePath("data") / "HANGMAN3.jpg"
HANGMAN4_JPEG = PurePath("data") / "HANGMAN4.jpg"
HANGMAN5_JPEG = PurePath("data") / "HANGMAN5.jpg"
WORDS_TUPLE = read_data(PurePath("data") / "WORDS_AND_THEMES.txt")


STATUS_PREPARE = "подготовка"
STATUS_INPROGRESS = "идет игра"
STATUS_VICTORY = "ПОБЕДА"
STATUS_DEFEAT = "проиграли"


class HangmanGame:
    """
    Описывает класс игры виселицы


    attributes:

    health: Здоровье игрока
    word: Текущее слово
    theme: Тема слова
    answer: Загаданное слово
    status: Статус игры: подготовка, идет игра, ПОБЕДА, проиграли
    """
    def __init__(self, difficulty=1, ):
        self.health = 5
        self.started = False
        self.word = ""
        self.theme = ""
        self.answer = ""
        self.status = STATUS_PREPARE

    def start(self):
        """
        Запуск игры
        :return:
        """
        self.status = STATUS_INPROGRESS
        self.started = True
        self.health = 5
        question_word = choice(WORDS_TUPLE)
        self.theme = question_word[0].capitalize()
        self.answer = question_word[1].lower().strip()
        self.word = "#" * len(self.answer)

    def guess(self, symbol) -> bool:
        """
        Метод для угадывания буквы
        :param symbol: буква, которую ввел игрок
        :return: Возвращает истину, если угадал букву, возвразает ложь, если не угадал.
        """
        if symbol in self.answer:
            new_word = list(self.word)
            for index, element in enumerate(self.answer):
                if element == symbol:
                    new_word[index] = symbol
            self.word = "".join(new_word)
            if "#" not in self.word:
                self.game_over(STATUS_VICTORY)
            return True
        self.decrease_health()
        return False

    def guess_word(self, word) -> bool:
        if word == self.answer:
            self.game_over(STATUS_VICTORY)
            return True
        self.decrease_health()
        return False

    def decrease_health(self):
        """
        Уменьшает жизнь игрока
        :return:
        """
        self.health -= 1
        if self.health == 0:
            self.game_over(STATUS_DEFEAT)

    def game_over(self, status=STATUS_PREPARE):
        """
        Метод закачивает игру
        :return:
        """
        self.health = 0
        self.status = status

    def show_hangman(self):
        """
        Отрисовка висельника из символов
        :return:
        """

        match self.health:
            case 4:
                return HANGMAN1_STR
            case 3:
                return HANGMAN2_STR
            case 2:
                return HANGMAN3_STR
            case 1:
                return HANGMAN4_STR
            case 0:
                return HANGMAN5_STR

        return ""

    def return_hangman_image(self):
        """
        Отрисовка висельника из символов
        :return:
        """

        match self.health:
            case 4:
                return HANGMAN1_JPEG
            case 3:
                return HANGMAN2_JPEG
            case 2:
                return HANGMAN3_JPEG
            case 1:
                return HANGMAN4_JPEG
            case 0:
                return HANGMAN5_JPEG

        return ""