from random import choice
from pathlib import PurePath
from file_processor import read_file, read_data

HANGMAN1_STR = read_file(PurePath("data") / "HANGMAN1.txt")
HANGMAN2_STR = read_file(PurePath("data") / "HANGMAN2.txt")
HANGMAN3_STR = read_file(PurePath("data") / "HANGMAN3.txt")
HANGMAN4_STR = read_file(PurePath("data") / "HANGMAN4.txt")
HANGMAN5_STR = read_file(PurePath("data") / "HANGMAN5.txt")
WORDS_TUPLE = read_data(PurePath("data") / "WORDS_AND_THEMES.txt")


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
        self.status = "подготовка"

    def start(self):
        """
        Запуск игры
        :return:
        """
        self.status = "идет игра"
        self.started = True
        self.health = 5
        question_word = choice(WORDS_TUPLE)
        self.theme = question_word[0].capitalize()
        self.answer = question_word[1].lower()
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
                self.game_over("ПОБЕДА")
            return True
        else:
            self.health -= 1
            if self.health == 0:
                self.game_over("проиграли")
            return False

    def game_over(self, status="подготовка"):
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
